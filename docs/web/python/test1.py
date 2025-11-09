import os
import glob
import vtk
import numpy as np
from vtk.util.numpy_support import vtk_to_numpy
from vtk.numpy_interface import dataset_adapter as dsa
import mgis.behaviour as mgis_bv
import mgis.model

model = {
    "LibraryPath": "src/libBehaviour.so",
    "Law": "DuctileDamageIndicator_RiceTracey1969",
    "Hypothesis": "Tridimensional",
}

material_properties = {"D1": 1, "D2": 1}

output = {"OutputData": "DamageIndicator", "VtkOutput": "true", "VtkFormat": "ascii"}

data = {
    "PrefixFiles": "Results",
    "Components": {"Stress": "SIG", "EquivalentPlasticStrain": "P"},
    "StressNotation": "Mandel",
    "Timestep": 1,
}

# Load VTK reader
r = vtk.vtkXMLUnstructuredGridReader()

# Get vtu files
f = sorted(glob.glob(data["PrefixFiles"] + "*vtu"))
if not f:
    raise FileNotFoundError("vtu files not found")

# Set mgis model
match model["Hypothesis"]:
    case "Tridimensional":
        h = mgis_bv.Hypothesis.Tridimensional
    case "GeneralisedPlaneStrain":
        h = mgis_bv.Hypothesis.GeneralisedPlaneStrain
    case "PlaneStrain":
        h = mgis_bv.Hypothesis.PlaneStrain
    case "Axisymmetrical":
        h = mgis_bv.Hypothesis.Axisymmetrical
    case "AxisymmetricalGeneralisedPlaneStrain":
        h = mgis_bv.Hypothesis.AxisymmetricalGeneralisedPlaneStrain
    case _:
        raise ValueError("Bad hypothesis")

# Get model
if not os.path.exists(model["LibraryPath"]):
    raise FileNotFoundError("Library file not found")

mm = mgis.model.load(model["LibraryPath"], model["Law"], h)

o = mgis_bv.getVariableOffset(mm.isvs, output["OutputData"], h)

# Get Material data manager
r.SetFileName(f[0])
r.Update()
m = mgis_bv.MaterialDataManager(mm, r.GetOutput().GetNumberOfPoints())

# Output data list
res = np.zeros([len(f), 1])

# Set Material Properties
for pname, pval in material_properties.items():
    mgis.behaviour.setMaterialProperty(m.s0, pname, pval)
    mgis.behaviour.setMaterialProperty(m.s1, pname, pval)

# Loop on the vtu files
for ifile, file in enumerate(f):
    # Load file
    r.SetFileName(file)
    r.Update()
    # Loop on the input data of the model
    for cm, cvtk in data["Components"].items():
        # Get data
        d = r.GetOutput().GetPointData().GetArray(cvtk)
        # Convert to numpy
        d = vtk_to_numpy(d)
        # MFront type stress components
        if (cm == "Stress") and (
            not (model["Hypothesis"] == "AxisymmetricalGeneralisedPlaneStrain")
        ):
            if (data["StressNotation"] == "Voigt") or (
                data["StressNotation"] == "ReverseVoigt"
            ):
                d[:, 3:] *= np.sqrt(2)
            if (model["Hypothesis"] == "Tridimensional") and (
                (data["StressNotation"] == "Voigt")
                or (data["StressNotation"] == "Mandel")
            ):
                d[:, [3, 4, 5]] = d[:, [5, 4, 3]]
        # first iteration: set initial values (m.s0) equal to zero
        if ifile == 0:
            mgis_bv.setExternalStateVariable(
                m.s0,
                cm,
                0 * d.reshape(d.size),
                mgis_bv.MaterialStateManagerStorageMode.LocalStorage,
            )
        # Set end of step values (m.s1)
        mgis_bv.setExternalStateVariable(
            m.s1,
            cm,
            d.reshape(d.size),
            mgis_bv.MaterialStateManagerStorageMode.LocalStorage,
        )
    # Integrate the model
    mgis_bv.integrate(
        m,
        mgis_bv.IntegrationType.IntegrationWithoutTangentOperator,
        data["Timestep"],
        0,
        m.n,
    )
    # Get damage value
    d = m.s1.internal_state_variables[:, o]
    # Get maximum damage
    res[ifile] = np.max(d)
    # Output vtu with damage value
    if output["VtkOutput"]:
        # Set mesh and writer
        meshNew = dsa.WrapDataObject(r.GetOutput())
        meshNew.PointData.append(d, output["OutputData"])
        w = vtk.vtkXMLUnstructuredGridWriter()
        # Set output file name
        w.SetFileName(
            data["PrefixFiles"] + "_post" + file.split(data["PrefixFiles"])[1]
        )
        w.SetInputData(meshNew.VTKObject)
        if output["VtkFormat"] == "ascii":
            w.SetDataModeToAscii()
        w.Write()

np.savetxt(data["PrefixFiles"] + "_post.txt", res)
