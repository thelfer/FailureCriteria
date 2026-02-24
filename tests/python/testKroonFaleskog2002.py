import sys
sys.path.insert(0,'../../src/')
from FailureCriteria import postVTK

output = {'VtkOutput':'true',
          'VtkFormat':'ascii'}

param = {'sigma_u':2000.,'sigma_th':200.,'alpha_p':0.1}

model = {'LibraryPath':'../../src/src/libBehaviour.so',
         'Law':'BrittleFractureProbability_KroonFaleskog2002',
         'Hypothesis':'Axisymmetrical'}

data = {'FolderFiles':'../../tests/results/ant10_tensile/',
        'PrefixFiles':'ant10_10_tensile_gauss_points',
        'Components':{'Stress':'SIG','EquivalentPlasticStrain':'P'},
        'DataType':'Points',
        'Volume':'VOLU',
        'ReferenceVolume':0.001,
        'StressNotation':'Voigt',
        'Timestep':1}
postVTK(model,data,param,output)

data = {'FolderFiles':'../../tests/results/ant10_tensile/',
        'PrefixFiles':'ant10_10_tensile_elements',
        'Components':{'Stress':'SIG','EquivalentPlasticStrain':'P'},
        'DataType':'Cells',
        'Volume':'VOLU',
        'ReferenceVolume':0.001,
        'StressNotation':'Voigt',
        'Timestep':1}
postVTK(model,data,param,output)

data = {'FolderFiles':'../../tests/results/ant2_tensile/',
        'PrefixFiles':'ant2_10_tensile_gauss_points',
        'Components':{'Stress':'SIG','EquivalentPlasticStrain':'P'},
        'DataType':'Points',
        'Volume':'VOLU',
        'ReferenceVolume':0.001,
        'StressNotation':'Voigt',
        'Timestep':1}
postVTK(model,data,param,output)

data = {'FolderFiles':'../../tests/results/ant2_tensile/',
        'PrefixFiles':'ant2_10_tensile_elements',
        'Components':{'Stress':'SIG','EquivalentPlasticStrain':'P'},
        'DataType':'Cells',
        'Volume':'VOLU',
        'ReferenceVolume':0.001,
        'StressNotation':'Voigt',
        'Timestep':1}
postVTK(model,data,param,output)

model = {'LibraryPath':'../../src/src/libBehaviour.so',
         'Law':'BrittleFractureProbability_KroonFaleskog2002',
         'Hypothesis':'PlaneStrain'}

data = {'FolderFiles':'../../tests/results/psnt2_tensile/',
        'PrefixFiles':'psnt2_10_tensile_gauss_points',
        'Components':{'Stress':'SIG','EquivalentPlasticStrain':'P'},
        'DataType':'Points',
        'Volume':'VOLU',
        'ReferenceVolume':0.0001,
        'StressNotation':'Voigt',
        'Timestep':1}
postVTK(model,data,param,output)

data = {'FolderFiles':'../../tests/results/psnt2_tensile/',
        'PrefixFiles':'psnt2_10_tensile_elements',
        'Components':{'Stress':'SIG','EquivalentPlasticStrain':'P'},
        'DataType':'Cells',
        'Volume':'VOLU',
        'ReferenceVolume':0.0001,
        'StressNotation':'Voigt',
        'Timestep':1}
postVTK(model,data,param,output)
    
data = {'FolderFiles':'../../tests/results/psnt2_shear/',
        'PrefixFiles':'psnt2_10_shear_gauss_points',
        'Components':{'Stress':'SIG','EquivalentPlasticStrain':'P'},
        'DataType':'Points',
        'Volume':'VOLU',
        'ReferenceVolume':0.0001,
        'StressNotation':'Voigt',
        'Timestep':1}
postVTK(model,data,param,output)

data = {'FolderFiles':'../../tests/results/psnt2_shear/',
        'PrefixFiles':'psnt2_10_shear_elements',
        'Components':{'Stress':'SIG','EquivalentPlasticStrain':'P'},
        'DataType':'Cells',
        'Volume':'VOLU',
        'ReferenceVolume':0.0001,
        'StressNotation':'Voigt',
        'Timestep':1}
postVTK(model,data,param,output)

data = {'FolderFiles':'../../tests/results/ct20_2d/',
        'PrefixFiles':'ct20_2d_gauss_points',
        'Components':{'Stress':'SIG','EquivalentPlasticStrain':'P'},
        'DataType':'Points',
        'Volume':'VOLU',
        'ReferenceVolume':0.0001,
        'StressNotation':'Voigt',
        'Timestep':1}
postVTK(model,data,param,output)

data = {'FolderFiles':'../../tests/results/ct20_2d/',
        'PrefixFiles':'ct20_2d_elements',
        'Components':{'Stress':'SIG','EquivalentPlasticStrain':'P'},
        'DataType':'Cells',
        'Volume':'VOLU',
        'ReferenceVolume':0.0001,
        'StressNotation':'Voigt',
        'Timestep':1}
postVTK(model,data,param,output)
