---
title: Analysis of simulation's results exported in VTK with python and MGIS
author: Jérémy Hure, Thomas Helfer
date: 24/02/2026
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
exported in `VTK` with `python`.

> **`python` module requirements**
>
> The following modules are required:
>
> - os
> - glob
> - numpy
> - vtk
> - mgis 

Test cases and sets of `VTK` files are described and available [here](https://thelfer.github.io/FailureCriteria/web/tests.html).

>  `VTK` files can correspond to unstructured grids (output of FEM solvers) with a mandatory file extension `.vtu`, or structured grids (output of FFT solvers) with a mandatory file extension `.vts`.

# Quick start

A typical script allowing post-processing a set of `VTK` files is:

~~~~{.python}
from FailureCriteria import postVTK

# define the model to be used 
model = {
	# path to the library (see Note n°1)
	'LibraryPath':'libFailureCriteriaModels-generic.so',
	# fracture criterion
	'Law':'DuctileDamageIndicator_RiceTracey1969',
	# modelling hypothesis (Tridimensional, GeneralisedPlaneStrain, PlaneStrain, Axisymmetrical, AxisymmetricalGeneralisedPlaneStrain)
	'Hypothesis':'Axisymmetrical'
}

# define the data to be post-processed
data = {
	# folder containing the VTK files
	'FolderFiles':'results/ant10_tensile/',
	# prefix of the VTK files
    'PrefixFiles':'ant10_10_tensile_gauss_points',
	# Dictionnary to relate variables needed for post-processing to vtk files variables (see Note n°2) 
	'Components':{'Stress':'SIG','EquivalentPlasticStrain':'P','Strain':'ETO'},
	# vtk data type (Points / Cells)
	'DataType':'Points',
	# Ordering of stress components in vtk files (Voigt, ReverseVoigt, Mandel, ReverseMandel) see Note n°3
	'StressNotation':'Voigt',
	# timestep
	'Timestep':1
	# For probabilistic fracture models (see Note n°4): variable of the vtk file containing the volume associated with each point/cell data $V_i$
	# 'Volume':'VOLU'
	# For probabilistic fracture models (see Note n°4): reference volume $V_0$
	# 'ReferenceVolume':0.001
}

# define the model parameters (see Note n°5)
param = {'D1':0.1}

# define the output of the post processing
output= {
	# generate vtk files with the failure indicator (true / false)
	'VtkOutput':'true',
	# format of the VTU files (ascii / binary)
	'VtkFormat':'ascii'
}

# post-process 		
postVTK(model,data,param,output)
~~~~

The results will be saved in a folder named `post` located in the `FolderFiles`, *i.e.*, the `VTK` files containing the failure indicator, as well as a csv file containing the maximal damage value for ductile criteria or global fracture probability for probabilistic brittle criteria. If a csv file containing simulation output is present in `FolderFiles`, a column will be added.

> **Note n°1**
>
> The values indicated in the `model` dictionary are consistent with
> an installation using the `FailureCriteria` project. This means that
> `libFailureCriteriaModels-generic.so` shall be installed in a repository
> listed by the `LD_LIBRARY_PATH` variable (or in a system-wide directory,
> which is not recommended).

> **Note n°2**
>
> The name of the variables needed for the model can be obtained by running:
>
>~~~~{.bash}
>$ mfront-query --external-state-variables src/DuctileDamageIndicator_RiceTracey1969.mfront 
>- EquivalentPlasticStrain (p): the equivalent plastic strain
>- Stress (sig): the stress tensor
>~~~~

> **Note n°3**
>
> The notation used to store the stress components in the vtk file variable should be given. In 3D:
>
> - Voigt: $\{\sigma_{11},\sigma_{22},\sigma_{33},\sigma_{23},\sigma_{13},\sigma_{12} \}$
> - ReverseVoigt: $\{\sigma_{11},\sigma_{22},\sigma_{33},\sigma_{12},\sigma_{13},\sigma_{23} \}$
> - Mandel: $\{\sigma_{11},\sigma_{22},\sigma_{33},\sqrt{2}\sigma_{23},\sqrt{2}\sigma_{13},\sqrt{2}\sigma_{12} \}$
> - ReverseMandel: $\{\sigma_{11},\sigma_{22},\sigma_{33},\sqrt{2}\sigma_{12},\sqrt{2}\sigma_{13},\sqrt{2}\sigma_{23} \}$

> **Note n°4**
>
> For probabilistic brittle criteria, the ratio $V_i / V_0$ is needed to compute the global fracture probability. 

> **Note n°5**
>
> The name of the parameters needed for the model can be obtained by running:
>
>~~~~{.bash}
>$ mfront-query --material-properties src/DuctileDamageIndicator_RiceTracey1969.mfront 
>- D1
>~~~~

# Full description of the `python` post-processing

The script defined in the postVTK function is fully described in this section. The main implementation follows the main steps:

1. Create a `VTK` reader and list all the `VTK` files,
2. Load the post-processing as an `MGIS`'s model,
3. Create a `MaterialDataManager` to store the internal state variables
  of the post-processing and integrating the post-processing over each
  time step,
4. Initialize the material properties used by the post-processing,
5. Create a `NumPy` array named `res` to store the maximum value of the
  damage indicator (for ductile fracture criteria) or global fracture 
  probability (for probabilistic brittle fracture criteria) over all integration points 
  for all time steps,
6. Iterate over all the results files, extract the external state
  variables used by the post-processing, convert the stress field to
  match `MFront`'s conventions, and integrate the post-processing to
  compute the indicator or probability. The `res` array is then updated. On
  demand, the damage indicator or local fracture probability is saved 
  in a dedicated `VTK` file,
7. The `res` array is saved in a `csv` file.

## Importing `python` modules

The following `python` modules will be useful:

- the standard `os` and `glob` modules. The first is used to see if a
  file exists while the second allows to list all the `VTK` files in
  the current directory.
- The `numpy` module is used for array manipulation and data transfer
  from `VTK` to `MGIS`.
- The `vtk` module is used to read the `vtu` or `vts` files and optionally write
  the outputs. The `vtk_to_numpy` function is
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

## Listing results files and creating VTK reader / writer 

An output folder is created if needed:

~~~~{.python}
if not (os.path.exists(data['FolderFiles'] + '/post/')):
    os.makedirs(data['FolderFiles'] + '/post/')
~~~~

The following lines gather the names of all the `vtu` and `vts` files:

~~~~{.python}
fvtu = sorted(glob.glob(data['FolderFiles'] + '/' + data['PrefixFiles'] + '*vtu'))
fvts = sorted(glob.glob(data['FolderFiles'] + '/' + data['PrefixFiles'] + '*vts'))
~~~~

The following lines construct the appropriate reader and writer for the `VTK` files

~~~~{.python}
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
~~~~

## Loading the post-processing

The following lines create a suitable hypothesis variable:

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

The following lines load the post-processing and check if a ductile or brittle criterion is used:

~~~~{.python}
if not os.path.exists(model['LibraryPath']):
	raise FileNotFoundError("Library file not found")
else:
	mm = mgis.model.load(model['LibraryPath'], model['Law'], h)
	if ('DuctileDamageIndicator' in model['Law']):
		OutputData = 'DamageIndicator'
	if ('BrittleFractureProbability' in model['Law']):
		OutputData = 'LocalFractureProbability'
~~~~

We then get the offset of the indicator:

~~~~{.python}
o = mgis_bv.getVariableOffset(mm.isvs, output["OutputData"], h)
~~~~

The user may refer to the [`MGIS`
documentation](https://thelfer.github.io/mgis/web/bindings-cxx.html) for
more details.

## Creation of the material data manager

In order to create a `MaterialDataManager`, an `MGIS` data structure for
all the integration points to be post-processed, the first `VTK` file is
read to get the number of integration points:

~~~~{.python}
r.SetFileName(f[0])
r.Update()
if (data['DataType'] == 'Points'):
	m = mgis_bv.MaterialDataManager(mm, r.GetOutput().GetNumberOfPoints())
else:
	m = mgis_bv.MaterialDataManager(mm, r.GetOutput().GetNumberOfCells())
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

## Creation of `res` array

The following line create an array that will contains the output for each time step:

~~~~{.python}
res = np.zeros([len(f), 1])
~~~~

## Integration of the post-processing over all time steps

The following line begins the loop over all time steps:

~~~~{.python}
for ifile, file in enumerate(f):
~~~~

For each time step, the data are read from the associated `VTK` file:

~~~~{.python}
    r.SetFileName(file)
    r.Update()
~~~~

We then extract the data required by the post-processing. A special care
is taken when converting the stress or when treating the first time step
to initialize the initial state properly:

~~~~{.python}
for cm, cvtk in data['Components'].items():
	if (data['DataType'] == 'Points'):
		d = r.GetOutput().GetPointData().GetArray(cvtk)
	else:
		d = r.GetOutput().GetCellData().GetArray(cvtk)
	d = vtk_to_numpy(d)
	if ((cm == 'Stress') and (not (model['Hypothesis']=='AxisymmetricalGeneralisedPlaneStrain'))):
		if ((data['StressNotation'] == 'Voigt') or (data['StressNotation'] == 'ReverseVoigt')):
			d[:,3:] *= np.sqrt(2)
		if ((model['Hypothesis'] == 'Tridimensional') and ((data['StressNotation'] == 'Voigt') or (data['StressNotation'] == 'Mandel'))):
			d[:,[3,4,5]] = d[:,[5,4,3]]
	if (ifile == 0):
		mgis_bv.setExternalStateVariable(m.s0, cm, 0*d.reshape(d.size), mgis_bv.MaterialStateManagerStorageMode.LocalStorage)
	mgis_bv.setExternalStateVariable(m.s1, cm, d.reshape(d.size), mgis_bv.MaterialStateManagerStorageMode.LocalStorage)
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

We then extract the outputs at the end of the time step and
compute: maximal value for ductile criteria or global fracture probability for 
probabilistic brittle fracture criteria:

~~~~{.python}
d = m.s1.internal_state_variables[:,o]
if (OutputData == 'DamageIndicator'):
	res[ifile] = np.max(d)
if (OutputData == 'LocalFractureProbability'):
	if (data['DataType'] == 'Points'):
		volu = r.GetOutput().GetPointData().GetArray(data['Volume'])
	else:
		volu = r.GetOutput().GetCellData().GetArray(data['Volume'])
	volu = vtk_to_numpy(volu)
	res[ifile] = 1 - np.prod(np.power(np.maximum(1 - d,0), volu / data['ReferenceVolume']))
~~~~

If requested, the results are saved in a dedicated `VTK` file:

~~~~{.python}
if output['VtkOutput']: 
	meshNew = dsa.WrapDataObject(r.GetOutput())
	if (data['DataType'] == 'Points'):
		meshNew.PointData.append(d, OutputData)
	else:
		meshNew.CellData.append(d, OutputData)
	w.SetFileName(data['FolderFiles'] + '/post/' + model['Law'] + '_' + data['PrefixFiles'] + file.split(data['PrefixFiles'])[1])
	w.SetInputData(meshNew.VTKObject)
	if (output['VtkFormat'] == 'ascii'):                                    
		w.SetDataModeToAscii()
	w.Write()
~~~~

The beginning of next time step is set as the end of current time step.

~~~~{.python}
mgis_bv.update(m)
~~~~

## Saving the results

Finally, the `res` array is concatenated with the simulations results if any, and saved in a `csv` file:

~~~~{.python}
f = glob.glob(data['FolderFiles'] + '/' + '*csv')
if f:
	numcsv = np.loadtxt(f[0],max_rows=np.shape(res)[0])
	res = np.hstack((numcsv,res))
np.savetxt(data['FolderFiles'] + '/post/' + model['Law'] + '_' + data['PrefixFiles'] + '.csv',res)
~~~~

# References {.unnumbered}
