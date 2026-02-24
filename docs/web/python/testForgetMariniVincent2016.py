import sys
sys.path.insert(0,'../../src/')
from FailureCriteria import postVTK

output = {'VtkOutput':'true',
          'VtkFormat':'ascii'}

param = {'E':200000.,'nu':0.3, 'alpha_r':1.6, 'beta_r':1.5e-4, 'gamma_r':1.e-5, 'gamma_f':5.e-3, 'mh':7.0, 'kh':1.1}

model = {'LibraryPath':'../../src/src/libBehaviour.so',
         'Law':'BrittleFractureProbability_ForgetMariniVincent2016',
         'Hypothesis':'Axisymmetrical'}

data = {'FolderFiles':'../../tests/results/ant10_tensile/',
        'PrefixFiles':'ant10_10_tensile_gauss_points',
        'Components':{'Stress':'SIG','EquivalentPlasticStrain':'P'},
        'DataType':'Points',
        'Volume':'VOLU',
        'ReferenceVolume':1.e-9,
        'StressNotation':'Voigt',
        'Timestep':1}
postVTK(model,data,param,output)

data = {'FolderFiles':'../../tests/results/ant10_tensile/',
        'PrefixFiles':'ant10_10_tensile_elements',
        'Components':{'Stress':'SIG','EquivalentPlasticStrain':'P'},
        'DataType':'Cells',
        'Volume':'VOLU',
        'ReferenceVolume':1.e-9,
        'StressNotation':'Voigt',
        'Timestep':1}
postVTK(model,data,param,output)

data = {'FolderFiles':'../../tests/results/ant2_tensile/',
        'PrefixFiles':'ant2_10_tensile_gauss_points',
        'Components':{'Stress':'SIG','EquivalentPlasticStrain':'P'},
        'DataType':'Points',
        'Volume':'VOLU',
        'ReferenceVolume':1.e-9,
        'StressNotation':'Voigt',
        'Timestep':1}
postVTK(model,data,param,output)

data = {'FolderFiles':'../../tests/results/ant2_tensile/',
        'PrefixFiles':'ant2_10_tensile_elements',
        'Components':{'Stress':'SIG','EquivalentPlasticStrain':'P'},
        'DataType':'Cells',
        'Volume':'VOLU',
        'ReferenceVolume':1.e-9,
        'StressNotation':'Voigt',
        'Timestep':1}
postVTK(model,data,param,output)

model = {'LibraryPath':'../../src/src/libBehaviour.so',
         'Law':'BrittleFractureProbability_ForgetMariniVincent2016',
         'Hypothesis':'PlaneStrain'}

data = {'FolderFiles':'../../tests/results/psnt2_tensile/',
        'PrefixFiles':'psnt2_10_tensile_gauss_points',
        'Components':{'Stress':'SIG','EquivalentPlasticStrain':'P'},
        'DataType':'Points',
        'Volume':'VOLU',
        'ReferenceVolume':1.e-8,
        'StressNotation':'Voigt',
        'Timestep':1}
postVTK(model,data,param,output)

data = {'FolderFiles':'../../tests/results/psnt2_tensile/',
        'PrefixFiles':'psnt2_10_tensile_elements',
        'Components':{'Stress':'SIG','EquivalentPlasticStrain':'P'},
        'DataType':'Cells',
        'Volume':'VOLU',
        'ReferenceVolume':1.e-8,
        'StressNotation':'Voigt',
        'Timestep':1}
postVTK(model,data,param,output)
    
data = {'FolderFiles':'../../tests/results/psnt2_shear/',
        'PrefixFiles':'psnt2_10_shear_gauss_points',
        'Components':{'Stress':'SIG','EquivalentPlasticStrain':'P'},
        'DataType':'Points',
        'Volume':'VOLU',
        'ReferenceVolume':1.e-8,
        'StressNotation':'Voigt',
        'Timestep':1}
postVTK(model,data,param,output)

data = {'FolderFiles':'../../tests/results/psnt2_shear/',
        'PrefixFiles':'psnt2_10_shear_elements',
        'Components':{'Stress':'SIG','EquivalentPlasticStrain':'P'},
        'DataType':'Cells',
        'Volume':'VOLU',
        'ReferenceVolume':1.e-8,
        'StressNotation':'Voigt',
        'Timestep':1}
postVTK(model,data,param,output)

data = {'FolderFiles':'../../tests/results/ct20_2d/',
        'PrefixFiles':'ct20_2d_gauss_points',
        'Components':{'Stress':'SIG','EquivalentPlasticStrain':'P'},
        'DataType':'Points',
        'Volume':'VOLU',
        'ReferenceVolume':1.e-8,
        'StressNotation':'Voigt',
        'Timestep':1}
postVTK(model,data,param,output)

data = {'FolderFiles':'../../tests/results/ct20_2d/',
        'PrefixFiles':'ct20_2d_elements',
        'Components':{'Stress':'SIG','EquivalentPlasticStrain':'P'},
        'DataType':'Cells',
        'Volume':'VOLU',
        'ReferenceVolume':1.e-8,
        'StressNotation':'Voigt',
        'Timestep':1}
postVTK(model,data,param,output)
