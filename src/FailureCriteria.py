# Import modules
import os
import glob
import vtk
import numpy as np
from vtk.util.numpy_support import vtk_to_numpy
from vtk.numpy_interface import dataset_adapter as dsa
import mgis.behaviour as mgis_bv
import mgis.model

def postVTK(model,data,param,output):	
    
    # Create output folder if needed
    if not (os.path.exists(data['FolderFiles'] + '/post/')):
        os.makedirs(data['FolderFiles'] + '/post/')

    # Get VTK files (vtu or vts)
    fvtu = sorted(glob.glob(data['FolderFiles'] + '/' + data['PrefixFiles'] + '*vtu'))
    fvts = sorted(glob.glob(data['FolderFiles'] + '/' + data['PrefixFiles'] + '*vts'))

    # Check if files are unstructured or structured vtk files
    if ((not fvtu) and (not fvts)):
        raise FileNotFoundError("vtk files not found")
    elif (fvtu and fvts):
        raise FileNotFoundError("both vtu and vts files are present")
    elif fvtu:
        f = fvtu
        r = vtk.vtkXMLUnstructuredGridReader()
        w = vtk.vtkXMLUnstructuredGridWriter()
    else:
        f = fvts
        r = vtk.vtkXMLStructuredGridReader()
        w = vtk.vtkXMLStructuredGridWriter()

    # Set mgis model
    match model['Hypothesis']:
        case 'Tridimensional':
            h = mgis_bv.Hypothesis.Tridimensional
        case 'GeneralisedPlaneStrain':
            h = mgis_bv.Hypothesis.GeneralisedPlaneStrain
        case 'PlaneStrain':
            h = mgis_bv.Hypothesis.PlaneStrain
        case 'Axisymmetrical':
            h = mgis_bv.Hypothesis.Axisymmetrical
        case 'AxisymmetricalGeneralisedPlaneStrain':
            h = mgis_bv.Hypothesis.AxisymmetricalGeneralisedPlaneStrain
        case _:
            raise ValueError("Bad hypothesis")

    # Get model 
    if not os.path.exists(model['LibraryPath']):
        raise FileNotFoundError("Library file not found")
    else:
        mm = mgis.model.load(model['LibraryPath'], model['Law'], h)
        if ('DuctileDamageIndicator' in model['Law']):
            OutputData = 'DamageIndicator'
        if ('BrittleFractureProbability' in model['Law']):
            OutputData = 'LocalFractureProbability'
    o = mgis_bv.getVariableOffset(mm.isvs, OutputData, h)
    # Get Material data manager 
    r.SetFileName(f[0])
    r.Update()
    if (data['DataType'] == 'Points'):
        m = mgis_bv.MaterialDataManager(mm, r.GetOutput().GetNumberOfPoints())
    else:
        m = mgis_bv.MaterialDataManager(mm, r.GetOutput().GetNumberOfCells())

    # Set Material Properties
    for pname,pval in param.items():
        mgis.behaviour.setMaterialProperty(m.s0, pname, pval)
        mgis.behaviour.setMaterialProperty(m.s1, pname, pval)
    # Output data list
    res = np.zeros([len(f),1])
    # Loop on the vtu files  
    for ifile,file in enumerate(f):
        # Load file
        r.SetFileName(file)
        r.Update()	
        # Loop on the input data of the model
        for cm, cvtk in data['Components'].items():
            # Get data
            if (data['DataType'] == 'Points'):
                d = r.GetOutput().GetPointData().GetArray(cvtk)
            else:
                d = r.GetOutput().GetCellData().GetArray(cvtk)
            # Convert to numpy
            d = vtk_to_numpy(d)
            # MFront type stress components
            if ((cm == 'Stress') and (not (model['Hypothesis']=='AxisymmetricalGeneralisedPlaneStrain'))):
                if ((data['StressNotation'] == 'Voigt') or (data['StressNotation'] == 'ReverseVoigt')):
                    d[:,3:] *= np.sqrt(2)
                if ((model['Hypothesis'] == 'Tridimensional') and ((data['StressNotation'] == 'Voigt') or (data['StressNotation'] == 'Mandel'))):
                    d[:,[3,4,5]] = d[:,[5,4,3]]
            # first iteration: set initial values (m.s0) equal to zero
            if (ifile == 0):
                mgis_bv.setExternalStateVariable(m.s0, cm, 0*d.reshape(d.size), mgis_bv.MaterialStateManagerStorageMode.LocalStorage)
            # Set end of step values (m.s1)
            mgis_bv.setExternalStateVariable(m.s1, cm, d.reshape(d.size), mgis_bv.MaterialStateManagerStorageMode.LocalStorage)        
        # Integrate the model
        mgis_bv.integrate(m, mgis_bv.IntegrationType.IntegrationWithoutTangentOperator, data['Timestep'], 0, m.n)
        # Get output value
        d = m.s1.internal_state_variables[:,o]
        # Compute global output 
        if (OutputData == 'DamageIndicator'):
            res[ifile] = np.max(d)
        if (OutputData == 'LocalFractureProbability'):
            if (data['DataType'] == 'Points'):
                volu = r.GetOutput().GetPointData().GetArray(data['Volume'])
            else:
                volu = r.GetOutput().GetCellData().GetArray(data['Volume'])
            # Convert to numpy
            volu = vtk_to_numpy(volu)
            # Compute global fracture probability
            res[ifile] = 1 - np.prod(np.power(np.maximum(1 - d,0), volu / data['ReferenceVolume']))
        # Output vtk with damage value
        if output['VtkOutput']:
            # Set mesh and writer
            meshNew = dsa.WrapDataObject(r.GetOutput())
            if (data['DataType'] == 'Points'):
                meshNew.PointData.append(d, OutputData)
            else:
                meshNew.CellData.append(d, OutputData)
            # Set output file name
            w.SetFileName(data['FolderFiles'] + '/post/' + model['Law'] + '_' + data['PrefixFiles'] + file.split(data['PrefixFiles'])[1])
            w.SetInputData(meshNew.VTKObject)
            if (output['VtkFormat'] == 'ascii'):                                    
                w.SetDataModeToAscii()
            w.Write()
        mgis_bv.update(m)

    f = glob.glob(data['FolderFiles'] + '/' + '*csv')
    if f:
        numcsv = np.loadtxt(f[0],max_rows=np.shape(res)[0])
        res = np.hstack((numcsv,res))
    np.savetxt(data['FolderFiles'] + '/post/' + model['Law'] + '_' + data['PrefixFiles'] + '.csv',res)
                


