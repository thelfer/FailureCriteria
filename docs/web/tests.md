---
title: Test 
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

Finite element [`Cast3M`](https://www-cast3m.cea.fr) simulations have been performed on various meshes to generate vtu files and test failure criteria. 

The `Cast3M` scripts can be run as follows:

~~~~{.bash}
castem25 *.dgibi
~~~~

The mesh associated with the different samples are available in med files usable with other finite element solvers for benchmark.

All simulations have been performed using constitutive equations corresponding to:

- Isotropic elasticity, with a Young's modulus $E=200000$ and Poisson ratio $\nu=0.3$
- von Mises plasticity with isotropic hardening $R(p) = 500 + 300[1-\exp{(-10p)}]$
- Hencky finite strain framework

The corresponding `mfront` file ([ldc.mfront](mfront/ldc.mfront)) should be compiled before running the `Cast3M` script as follows:

~~~~{.bash}
mfront --obuild --interface=castem21 *.mfront
~~~~

The following mechanical quantities have been computed per timestep:

- SIG: stress components in Voigt notation
- ETO: strain components in Voigt notation
- P: cumulated plastic strain
- VOLU: local volume

All simulations have been postprocessed to generate two vtu files per timestep:

- PointData: all mechanical quantities are stored at Gauss points
- CellData: all mechanical quantities are averaged per elements

and analysed using all available fracture criteria:

- BrittleFractureProbability_BakkerKoers1991 ([testBakkerKoers1991.py](python/testBakkerKoers1991.py))
- BrittleFractureProbability_Beremin1983 ([testBeremin1983.py](python/testBeremin1983.py))
- BrittleFractureProbability_BordetKarstensenKnowlesWiesner2005 ([testBordetKarstensenKnowlesWiesner2005.py](python/testBordetKarstensenKnowlesWiesner2005.py))
- BrittleFractureProbability_ForgetMariniVincent2016 ([testForgetMariniVincent2016.py](python/testForgetMariniVincent2016.py))
- BrittleFractureProbability_HoheHardenackeLuckowSiegele2010ExponentialLaw ([testHoheHardenackeLuckowSiegele2010ExponentialLaw.py](python/testHoheHardenackeLuckowSiegele2010ExponentialLaw.py))
- BrittleFractureProbability_HoheHardenackeLuckowSiegele2010PowerLaw ([testHoheHardenackeLuckowSiegele2010PowerLaw.py](python/testHoheHardenackeLuckowSiegele2010PowerLaw.py))
- BrittleFractureProbability_KroonFaleskog2002 ([testKroonFaleskog2002.py](python/testKroonFaleskog2002.py))
- BrittleFractureProbability_RuggieriDodds2015 ([testRuggieriDodds2015.py](python/testRuggieriDodds2015.py))
- DuctileDamageIndicator_Freudenthal1950 ([testFreudenthal1950.py](python/testFreudenthal1950.py))
- DuctileDamageIndicator_CockcroftLatham1968 ([testCockcroftLatham1968.py](python/testCockcroftLatham1968.py))
- DuctileDamageIndicator_RiceTracey1969HighStressTriaxiality ([testRiceTracey1969HighStressTriaxiality.py](python/testRiceTracey1969HighStressTriaxiality.py))
- DuctileDamageIndicator_RiceTracey1969 ([testRiceTracey1969.py](python/testRiceTracey1969.py))
- DuctileDamageIndicator_GeneralizedRiceTracey ([testGeneralizedRiceTracey.py](python/testGeneralizedRiceTracey.py))
- DuctileDamageIndicator_HancockMcKenzie1976 ([testHancockMcKenzie1976.py](python/testHancockMcKenzie1976.py))
- DuctileDamageIndicator_GeneralizedHancockMcKenzie ([testGeneralizedHancockMcKenzie.py](python/testGeneralizedHancockMcKenzie.py))
- DuctileDamageIndicator_JohnsonCook1985 ([testJohnsonCook1985.py](python/testJohnsonCook1985.py))
- DuctileDamageIndicator_Huang1991 ([testHuang1991.py](python/testHuang1991.py))
- DuctileDamageIndicator_GeneralizedHuang ([testGeneralizedHuang.py](python/testGeneralizedHuang.py))

# Test n°1: Axisymmetric smooth notched tensile

- Mesh file: [ant10_10.med](castem/ant10_10.med)
- Simulation file: [ant10_tensile.dgibi](castem/ant10_tensile.dgibi)
- Results files: [ant10_tensile.tar.gz](castem/ant10_tensile.tar.gz)

![Mesh](img/ant10.png){width=50%}

![Load - displacement curve](img/ant10_gra1.pdf){width=50%}

![Maximal damage - displacement curve](img/ant10_gra2.pdf){width=50%}

![Global fracture probability - displacement curve](img/ant10_gra3.pdf){width=50%}

# Test n°2: Axisymmetric deep notched tensile

- Mesh file: [ant2_10.med](castem/ant2_10.med)
- Simulation file: [ant2_tensile.dgibi](castem/ant2_tensile.dgibi)
- Results files: [ant2_tensile.tar.gz](castem/ant2_tensile.tar.gz)

![Mesh](img/ant2.png){width=50%}

![Load - displacement curve](img/ant2_gra1.pdf){width=50%}

![Maximal damage - displacement curve](img/ant2_gra2.pdf){width=50%}

![Global fracture probability - displacement curve](img/ant2_gra3.pdf){width=50%}

# Test n°3: Plane strain notched sample under tensile loading

- Mesh file: [nt2_10.med](castem/nt2_10.med)
- Simulation file: [psnt2_tensile.dgibi](castem/psnt2_tensile.dgibi)
- Results files: [psnt2_tensile.tar.gz](castem/psnt2_tensile.tar.gz)

![Mesh](img/psnt2.png){width=50%}

![Load - displacement curve](img/psnt2_tensile_gra1.pdf){width=50%}

![Maximal damage - displacement curve](img/psnt2_tensile_gra2.pdf){width=50%}

![Global fracture probability - displacement curve](img/psnt2_tensile_gra3.pdf){width=50%}

# Test n°4: Plane strain notched sample under shear loading

- Mesh file: [nt2_10.med](castem/nt2_10.med)
- Simulation file: [psnt2_shear.dgibi](castem/psnt2_shear.dgibi)
- Results files: [psnt2_shear.tar.gz](castem/psnt2_shear.tar.gz)

![Mesh](img/psnt2.png){width=50%}

![Load - displacement curve](img/psnt2_shear_gra1.pdf){width=50%}

![Maximal damage - displacement curve](img/psnt2_shear_gra2.pdf){width=50%}

![Global fracture probability - displacement curve](img/psnt2_shear_gra3.pdf){width=50%}

# Test n°5: Compact Tension sample

- Mesh file: [ct20_2d.med](castem/ct20_2d.med)
- Simulation file: [ct20_2d.dgibi](castem/ct20_2d.dgibi)
- Results files: [ct20_2d.tar.gz](castem/ct20_2d.tar.gz)

![Mesh](img/ct20_2d.png){width=50%}

![Load - displacement curve](img/ct20_2d_gra1.pdf){width=50%}

![Maximal damage - displacement curve](img/ct20_2d_gra2.pdf){width=50%}

![Global fracture probability - displacement curve](img/ct20_2d_gra3.pdf){width=50%}

# References {.unnumbered}
