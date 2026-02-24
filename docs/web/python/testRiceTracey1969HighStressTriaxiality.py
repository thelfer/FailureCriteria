import sys
sys.path.insert(0,'../../src/')
from FailureCriteria import postVTK

output = {'VtkOutput':'true',
          'VtkFormat':'ascii'}

param = {'D1':1.}

model = {'LibraryPath':'../../src/src/libBehaviour.so',
         'Law':'DuctileDamageIndicator_RiceTracey1969HighStressTriaxiality',
         'Hypothesis':'Axisymmetrical'}

data = {'FolderFiles':'../../tests/results/ant10_tensile/',
        'PrefixFiles':'ant10_10_tensile_gauss_points',
        'Components':{'Stress':'SIG','EquivalentPlasticStrain':'P'},
        'DataType':'Points',
        'StressNotation':'Voigt',
        'Timestep':1}
postVTK(model,data,param,output)

data = {'FolderFiles':'../../tests/results/ant10_tensile/',
        'PrefixFiles':'ant10_10_tensile_elements',
        'Components':{'Stress':'SIG','EquivalentPlasticStrain':'P'},
        'DataType':'Cells',
        'StressNotation':'Voigt',
        'Timestep':1}
postVTK(model,data,param,output)

data = {'FolderFiles':'../../tests/results/ant2_tensile/',
        'PrefixFiles':'ant2_10_tensile_gauss_points',
        'Components':{'Stress':'SIG','EquivalentPlasticStrain':'P'},
        'DataType':'Points',
        'StressNotation':'Voigt',
        'Timestep':1}
postVTK(model,data,param,output)

data = {'FolderFiles':'../../tests/results/ant2_tensile/',
        'PrefixFiles':'ant2_10_tensile_elements',
        'Components':{'Stress':'SIG','EquivalentPlasticStrain':'P'},
        'DataType':'Cells',
        'StressNotation':'Voigt',
        'Timestep':1}
postVTK(model,data,param,output)

model = {'LibraryPath':'../../src/src/libBehaviour.so',
         'Law':'DuctileDamageIndicator_RiceTracey1969HighStressTriaxiality',
         'Hypothesis':'PlaneStrain'}

data = {'FolderFiles':'../../tests/results/psnt2_tensile/',
        'PrefixFiles':'psnt2_10_tensile_gauss_points',
        'Components':{'Stress':'SIG','EquivalentPlasticStrain':'P'},
        'DataType':'Points',
        'StressNotation':'Voigt',
        'Timestep':1}
postVTK(model,data,param,output)

data = {'FolderFiles':'../../tests/results/psnt2_tensile/',
        'PrefixFiles':'psnt2_10_tensile_elements',
        'Components':{'Stress':'SIG','EquivalentPlasticStrain':'P'},
        'DataType':'Cells',
        'StressNotation':'Voigt',
        'Timestep':1}
postVTK(model,data,param,output)
    
data = {'FolderFiles':'../../tests/results/psnt2_shear/',
        'PrefixFiles':'psnt2_10_shear_gauss_points',
        'Components':{'Stress':'SIG','EquivalentPlasticStrain':'P'},
        'DataType':'Points',
        'StressNotation':'Voigt',
        'Timestep':1}
postVTK(model,data,param,output)

data = {'FolderFiles':'../../tests/results/psnt2_shear/',
        'PrefixFiles':'psnt2_10_shear_elements',
        'Components':{'Stress':'SIG','EquivalentPlasticStrain':'P'},
        'DataType':'Cells',
        'StressNotation':'Voigt',
        'Timestep':1}
postVTK(model,data,param,output)

data = {'FolderFiles':'../../tests/results/ct20_2d/',
        'PrefixFiles':'ct20_2d_gauss_points',
        'Components':{'Stress':'SIG','EquivalentPlasticStrain':'P'},
        'DataType':'Points',
        'StressNotation':'Voigt',
        'Timestep':1}
postVTK(model,data,param,output)

data = {'FolderFiles':'../../tests/results/ct20_2d/',
        'PrefixFiles':'ct20_2d_elements',
        'Components':{'Stress':'SIG','EquivalentPlasticStrain':'P'},
        'DataType':'Cells',
        'StressNotation':'Voigt',
        'Timestep':1}
postVTK(model,data,param,output)
