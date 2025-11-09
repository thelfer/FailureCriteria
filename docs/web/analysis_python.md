---
title: Analysis of simulation's results exported in VTK with python and MGIS
author: Jérémy Hure, Thomas Helfer
date: 03/11/2026
lang: en-EN
link-citations: true
colorlinks: true
figPrefixTemplate: "$$i$$"
tblPrefixTemplate: "$$i$$"
secPrefixTemplate: "$$i$$"
eqnPrefixTemplate: "($$i$$)"
---

This tutorial shows how to use the failure criteria provided by the
`FailureCriteria` project to analyse the results of a simulation
exported in `VTK` with the failure criterion proposed by Rice and Tracey
[@rice_ductile_1969] using `python` and `MGIS`.

> **Generation of the VTK file**
>
> The `VTK` files analysed in this tutorial have been generated
> from the following [`Cast3M` simulation](https://www-cast3m.cea.fr):
>
> - [`test1.dgibi`](castem/test1.dgibi)
> - [`test1.mfront`](mfront/test1.mfront)
> 
> The `MFront` file can be compiled as follows:
>
> ~~~~{.bash}
> mfront --obuild --interface=castem21 test1.mfront
> ~~~~
>
> The `Cast3M` script can be run as follows:
>
> ~~~~{.bash}
> castem24 test1.dgibi
> ~~~~

The tutorial requires the following files to be run:

- [`test1.py`](python/test1.py)
-
  [`DuctileDamageIndicator_RiceTracey1969.mfront`](https://raw.githubusercontent.com/thelfer/FailureCriteria/refs/heads/master/src/DuctileDamageIndicator_RiceTracey1969.mfront).
  This file is automatically compiled by the `FailureCriteria` project.

This tutorial can be easily adapted to many situations, the key being
the fact that `VTK` data can be exposed as `NumPy`'s arrays and that
`NumPy`'s arrays are directly usable with `MGIS`

# Description of the test case

## Description of the Rice-Tracey failure criterion

The Rice-Tracey failure criterion computes a damage indicator \(d\) as
follows:
\[
d_{i} = \int_{0}^{t}\frac{\dot{p}\,\mathrm{d}t}{D_{1} \, \exp\left(D_{2} \, T_{\sigma}\right)}
\]
where:

- \(\dot{p}\) is the equivalent strain rate,
- \(T_{\sigma}\) is the stress triaxiality, ratio of the hydrostatic pressure and
  von Mises stress,
- \(D_{1}\) and \(D_{2}\) are material properties.

### Description of the `MFront` implementation

The Rice-Tracey failure criterion is implemented in the file
[`DuctileDamageIndicator_RiceTracey1969.mfront`](https://raw.githubusercontent.com/thelfer/FailureCriteria/refs/heads/master/src/DuctileDamageIndicator_RiceTracey1969.mfront).

### Material properties

The implementation declares two material properties that will have to be
defined in the post-processing script:

~~~~{.bash}
$ mfront-query --material-properties src/DuctileDamageIndicator_RiceTracey1969.mfront 
- D1
- D2
~~~~

### External state variables

The implementation declares two external state variables that will have
to be extracted from the results of the simulation in the
post-processing script:

~~~~{.bash}
$ mfront-query --external-state-variables src/DuctileDamageIndicator_RiceTracey1969.mfront 
- EquivalentPlasticStrain (p): the equivalent plastic strain
- Stress (sig): the stress tensor
~~~~

### Internal state variables

The implementation compute an unique state result, named
`DamageIndicator`:

~~~~{.bash}
$ mfront-query --persistent-variables src/DuctileDamageIndicator_RiceTracey1969.mfront 
- DamageIndicator (di)
~~~~

## Description of the results to be analysed

For each time step, a `vtu` file has been generated. In our example, the
names of those files matches the pattern `test1.XXXX.vtu` where `XXXX`
denotes the time step number. Those `vtu` files contains a certain
number of data that will be used for the post-processing.

The `VTK` files contains two fields, stored in two point data: the
Cauchy stress field, named `SIG` and the equivalent plastic strain field
named `P`. Two remarks can be made:

- Those names differ from names of the external state variables expected
  by the `MFront` implementation of the failure criterion.
- The Cauchy stress field exported by `Cast3M` is stored in a 6
  components, but the conventions used by `Cast3M` differ from the one
  used by `MFront` (see [this
  page](https://thelfer.github.io/tfel/web/tensors.html) for details).
  Extra diagonal components must be multiplied by a factor \(\sqrt(2\)
  before passing the values to `MGIS`.

# Implementation in `python`

The main implementation follows the following main steps:

1. Create a `VTK` reader and list all the `vtu` files,
2. Load the post-processing as an `MGIS`'s model,
3. Create a `MaterialDataManager` to store the internal state variables
  of the post-processing and integrating the post-processing over each
  time steps,
4. Initialize the material properties used by the post-processing
5. Create a `NumPy` array named `res` to store the maximum value of the
  damage indicator over all integration points for all time steps.
6. Iterate over all the results files, extract the external state
  variables used by the post-processing, convert the stress field to
  match `MFront`'s conventions, and integrate the post-processing to
  compute the damage indicator. The `res` array is then updated. On
  demand, the damage indicator is saved in a dedicated `vtu` file.
7. The `res` array is saved in a `txt` file.

## Importing `python` modules

The following `python` modules will be useful:

- the standard `os` and `glob` modules. The first is used to see if a
  file exists while the second allows to list all the `vtu` files in
  the current directory.
- The `numpy` module is used for array manipulation and data transfer
  from `vtk` to `MGIS`.
- The `vtk` module is used to read the `vtu` files and optionally write
  the damage indicator on output. The `vtk_to_numpy` function is
  imported from the `vtk.util.numpy_support` modules as well as the
  `dataset_adapter` class from `vtk.numpy_interface`
- Finally the `mgis.behaviour` and `mgis.model` are imported.

All those modules are imported as follows:

~~~~{.python}
import os
import glob
import numpy as np
import vtk
from vtk.util.numpy_support import vtk_to_numpy
from vtk.numpy_interface import dataset_adapter as dsa
import mgis.behaviour as mgis_bv
import mgis.model
~~~~

## Main parameters defining the post-processing

In order to highlight the main end-user parameters of the
post-processing script, four dictionaries are defined.

The `model` dictionary describes the failure criterion to be used:

~~~~{.python}
model = {
    "LibraryPath": "libFailureCriteriaModels-generic.so",
    "Law": "DuctileDamageIndicator_RiceTracey1969",
    "Hypothesis": "Tridimensional",
}
~~~~

> **Note**
>
> The values indicated in the `model` dictionary are consistent with
> an installation using the `FailureCriteria` project. This means that
> `libFailureCriteriaModels-generic.so` shall be installed in a repository
> listed by the `LD_LIBRARY_PATH` variable (or in a system-wide directory,
> which is not recommended).

The values of the material properties `D1` and `D2` are stored in the
`material_properties` dictorionary.

~~~~{.python}
material_properties = {"D1": 1, "D2": 1.5}
~~~~

The `output` dictionary indicates the name of the state variable to be
post-processed, and some parameters related to `VTK` output.

~~~~{.python}
output = {"OutputData": "DamageIndicator", "VtkOutput": "true", "VtkFormat": "ascii"}
~~~~

Finally, the `data` dictionary contains information about the `VTK`
files to be post-processed:

~~~~{.python}
data = {
    "PrefixFiles": "Results",
    "Components": {"Stress": "SIG", "EquivalentPlasticStrain": "P"},
    "StressNotation": "Mandel",
    "Timestep": 1,
}
~~~~

The `Components` entry maps the name of the `VTK` data set to the name
of the external state variable expected by the model.

The `StressNotation` entry indicates the king of the transformation to
be applied to the stress field to match `MFront`'s conventions.

The `Timestep` entry provides the value of the time step. This value is
required but has no impact of the results of the post-processing.

## Creation of the VTK reader and listing results files

The following line constructs the reader used to parse the `vtu` files

~~~~{.python}
r = vtk.vtkXMLUnstructuredGridReader()
~~~~

The following lines gather the names of all the `vtu` files:

~~~~{.python}
f = sorted(glob.glob(data["PrefixFiles"] + "*vtu"))
if not f:
    raise FileNotFoundError("vtu files not found")
~~~~

## Creation of `res` array

The following line create an array that will contains the maximum of the
damage indicator for each time step:

~~~~{.python}
res = np.zeros([len(f), 1])
~~~~

## Loading the post-processing

The following line create a suitable hypothesis variable:

~~~~{.python}
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
~~~~

The following lines loads the post-processing:

~~~~{.python}
if not os.path.exists(model["LibraryPath"]):
    raise FileNotFoundError("Library file not found")

mm = mgis.model.load(model["LibraryPath"], model["Law"], h)
~~~~

We then get the offset of the damage indicator:

~~~~{.python}
o = mgis_bv.getVariableOffset(mm.isvs, output["OutputData"], h)
~~~~

The user may refer to the [`MGIS`
documentation](https://thelfer.github.io/mgis/web/bindings-cxx.html) for
more details.

## Creation of the material data manager

In order to create a `MaterialDataManager`, an `MGIS` data structure for
all the integration points to be post-processed, the first `vtu` file is
read to get the number of integration points:

~~~~{.python}
r.SetFileName(f[0])
r.Update()
m = mgis_bv.MaterialDataManager(mm, r.GetOutput().GetNumberOfPoints())
~~~~

The user may refer to the [`MGIS`
documentation](https://thelfer.github.io/mgis/web/bindings-cxx.html) for
more details.

## Initialization of the material properties

The following line assigns the material properties to the material
state:

~~~~{.python}
for pname, pval in material_properties.items():
    mgis.behaviour.setMaterialProperty(m.s0, pname, pval)
    mgis.behaviour.setMaterialProperty(m.s1, pname, pval)
~~~~

## Integration of the post-processing over all time steps

The following line begins the loop over all time steps:

~~~~{.python}
for ifile, file in enumerate(f):
~~~~

For each time step, the data are read from the associated `vtu` file:

~~~~{.python}
    r.SetFileName(file)
    r.Update()
~~~~

We then extract the data required by the post-processing. A special care
is taken when converting the stress or when treating the first time step
to initialize the initial state properly:

~~~~{.python}
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
~~~~

The post-processing is then called as follows:

~~~~{.python}
    mgis_bv.integrate(
        m,
        mgis_bv.IntegrationType.IntegrationWithoutTangentOperator,
        data["Timestep"],
        0,
        m.n,
    )
~~~~

We then extract the damage indicator at the end of the time step and
compute its maximum value over all integration points:

~~~~{.python}
    d = m.s1.internal_state_variables[:, o]
    res[ifile] = np.max(d)
~~~~

If requested, the damage indicator is saved in a dedicated `vtu` file:

~~~~{.python}
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
~~~~

## Saving the results

Finally, the `res` array is saved in a `txt` file:

~~~~{.python}
np.savetxt(data["PrefixFiles"] + "_post.txt", res)
~~~~

# References {.unnumbered}