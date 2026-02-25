---
title: The FailureCriteria project
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

\newcommand{\bm}[1]{\underline{\boldsymbol{#1}}}
\newcommand{\Frac}[2]{{{\displaystyle \frac{\displaystyle #1}{\displaystyle #2}}}}

The project `FailureCriteria` provides `MFront` implementations of
various criteria to predict brittle and ductile failure.
Those implementations can be used in uncoupled analyses, in the
post-processing of the computations, or coupled analyses where the criteria are for example used along with an element deletion strategy.

> The project is very young, please do no hesitate to report mistakes and bugs

The criteria depends on the Cauchy stress tensor $\bm{\sigma}$ and strain tensor $\bm{\varepsilon}$, as well as on equivalent stress $\sigma_{eq}$ and associated cumulated plastic strain $\varepsilon_{eq}$.

# Probabilistic brittle fracture

Various models have been proposed to predict the brittle fracture probability of metal alloys  $p_f^i$ associated to an elementary volume $V_i$. The global fracture probability $P_f$ is then obtained considering the weakest link assumption [@beremin_local_1983]:

$$\displaystyle{ 1 - P_f = \Pi_{i}(1 - p_f^i)^{V_i / V_0}} $${#eq:mfront:fracturecriteria:brittle_fracture:global_fracture_probability}

where $V_0$ is a normalization volume, stating that the global survival probability is the product of all local survival probability. 

> **Note n°1**
> `MFront` only computes the local fracture probability $p_f^i$. The user should then compute the global fracture probability $P_f$ according to the Equation @eq:mfront:fracturecriteria:brittle_fracture:global_fracture_probability which requires the volume associated with $p_f^i$.

> **Note n°2**
> Assuming $p_f^i \ll 1$, Equation @eq:mfront:fracturecriteria:brittle_fracture:global_fracture_probability is usually rewriten in the literature as:
>$$\displaystyle{ \log{\left(1 - P_f\right)} = \sum_i - p_f^i} \Frac{V_i}{V_0} $$


> **Note n°3**
> Models are either *direct*, providing $p_f^i$, or *incremental*, providing $\dot{p}_f^i$. In the former case, the local fracture probability is computed at the end of the time step, and monotonicity is enforced by considering $\max{(p_f^{i,new},p_f^{i,old})}$. In the latter case, the local fracture probability is integrated using the midpoint rule.

Various models proposed in the literature for the local fracture probability $p_f^i$ are available in `MFront`:

## Beremin1983 [@beremin_local_1983]

* **Input**: stress tensor $\bm{\sigma}$, strain tensor $\bm{\varepsilon}$
* **Parameters**: reference stress $\sigma_u$, exponent $m$

The Beremin group considered that microcracks appear at the onset of plasticity and a power law distribution for microcracks size along with the Griffith criterion to estimate the local fracture probability. In addition, an effect of strain is incorporated on fracture stress. The final expression is:
	
$$p_f^i =  \left[ \Frac{\sigma_I}{\sigma_u} \exp{\left(-\Frac{\varepsilon_I}{2}    \right)}\right]^m  \quad \mathrm{for} \quad \{\varepsilon_{eq} > 0, \sigma_I > 0\}  $$

where $\sigma_I$ is the largest principal stress and $\varepsilon_I$ the associated strain.

## BakkerKoers1991 [@bakker_koers_1991]

* **Input**: stress tensor $\bm{\sigma}$, strain tensor $\bm{\varepsilon}$
* **Parameters**: reference stress $\sigma_u$, exponent $m$, threshold stress $\sigma_{th}$

Bakker & Koers proposed to modify Beremin1983 model to account for a threshold stress:
	
$$p_f^i =   \left[\Frac{\sigma_I - \sigma_{th}}{\sigma_u} \exp{\left(-\Frac{\varepsilon_I}{2}    \right)}\right]^m  \quad \mathrm{for} \quad \{\varepsilon_{eq} > 0, \sigma_I > \sigma_{th}\}  $$

## KroonFaleskog2002 [@kroon_faleskog_2002]

* **Input**: stress tensor $\bm{\sigma}$
* **Parameters**: reference stress $\sigma_u$, threshold stress $\sigma_{th}$, nucleation parameter $\alpha_p$

Kroon & Faleskog considered an exponential distribution for microcracks size along with a threshold stress, as well as a refined modelling of microcracks nucleation leading to a linear dependence of fracture probability to plastic strain:
	
$$p_f^i = \alpha_p\, \varepsilon_{eq}\,\left[ \exp{\left(-\left( \Frac{\sigma_u}{\sigma_I} \right)^2 \right) }  - \exp{\left(-\left( \Frac{\sigma_u}{\sigma_{th}} \right)^2  \right)} \right]  \quad \mathrm{for} \quad \sigma_I > \sigma_{th}  $$
	
Note that Kroon & Faleskog also proposed to compute a non-local value for $\sigma_I$.

## BordetKarstensenKnowlesWiesner2005 [@bordet_2005]

* **Input**: stress tensor $\bm{\sigma}$
* **Parameters**: reference stress $\sigma_u$, exponent $m$, threshold stress $\sigma_{th}$, nucleation parameters $\alpha_p$, $\beta_p$

Bordet *et al.* refined Beremin analysis for the nucleation of microcracks while keeping the same approach for microcracks propagation. An incremental formulation is obtained for the local fracture probability:

$$dp_f^i = \alpha_p \left[ \left( \Frac{\sigma_I}{\sigma_u} \right)^m  - \left(\Frac{\sigma_{th}}{\sigma_u} \right)^m  ,0   \right]   \exp{\left( -\beta_p \varepsilon_{eq}   \right)} d\varepsilon_{eq}  \quad \mathrm{for} \quad \sigma_I > \sigma_{th} $$

where $\alpha_p = \sigma_Y / \sigma_Y^{ref}$ is the ratio of yield stress at the temperature of interest to a reference yield stress, and $\beta_p=\alpha_p \varepsilon_{eq}^0$ where $\varepsilon_{eq}^0$ is a reference plastic strain.

## HoheHardenackeLuckowSiegele2010PowerLaw [@hohe_2010]

* **Input**: stress tensor $\bm{\sigma}$
* **Parameters**: reference stress $\sigma_u$, exponent $m$, threshold stress $\sigma_{th}$, nucleation parameters $\alpha_p$, $\beta_p$

Hohe *et al.* also refined Beremin and Kroon & Flaeskog analysis for the nucleation of microcracks that depends on stress triaxiality. An incremental formulation is obtained for the local fracture probability:

$$dp_f^i = \beta_p   \Frac{\exp{\left(- \alpha_p\eta   \right)}}{\sqrt{1+\alpha_p^2 \varepsilon_{eq}^2}} \max{\left(d\varepsilon_{eq} - \alpha_p\varepsilon_{eq} d\eta ,0      \right)}  \left[ \left( \Frac{\sigma_I}{\sigma_u} \right)^m  - \left(\Frac{\sigma_{th}}{\sigma_u} \right)^m   \right]  \quad \mathrm{for} \quad \{\varepsilon_{eq} > 0, \sigma_I > \sigma_{th}\}    $$

where $\eta$ is the stress triaxiality.

## HoheHardenackeLuckowSiegele2010ExponentialLaw [@hohe_2010]

* **Input**: stress tensor $\bm{\sigma}$
* **Parameters**: reference stress $\sigma_u$, exponent $m$, threshold stress $\sigma_{th}$, nucleation parameters $\alpha_p$, $\beta_p$

$$dp_f^i = \beta_p   \Frac{\exp{\left(- \alpha_p\eta   \right)}}{\sqrt{1+\alpha_p^2 \varepsilon_{eq}^2}} \max{\left(d\varepsilon_{eq} - \alpha_p\varepsilon_{eq} d\eta ,0      \right)} \left[ \exp{\left(-\left( \Frac{\sigma_u}{\sigma_I} \right)^2 \right) }  - \exp{\left(-\left( \Frac{\sigma_u}{\sigma_{th}} \right)^2  \right)}   \right]   \quad \mathrm{for} \quad \{\varepsilon_{eq} > 0, \sigma_I > \sigma_{th}\}    $$

## RuggieriDodds2015 [@ruggieri_dodds_2015]

* **Input**: stress tensor $\bm{\sigma}$
* **Parameters**: reference stress $\sigma_u$, exponent $m$, threshold stress $\sigma_{th}$, nucleation parameter $\alpha_p$

Ruggieri & Doods also proposed modifications of the Beremin model to account for microcrack nucleation:

$$p_f^i = \left[ 1 - \exp{\left( - \alpha_p \varepsilon_{eq}  \right) }    \right]    \left(\Frac{\sigma_I}{\sigma_u}\right)^m    \quad \mathrm{for} \quad \sigma_I > 0   $$

## ForgetMariniVincent2016 [@forget_application_2016]

* **Input**: stress tensor $\bm{\sigma}$
* **Parameters**: carbide size distribution parameters ($\alpha_r$, $\beta_r$, $\gamma_r$), carbide Young modulus $E$, carbide Poisson ratio $\nu$, carbide fracture energy $\gamma_f$, stress heterogeneity parameters ($m_H$, $k_H$) 	

Forget, Marini & Vincent refined Beremin analysis for microcracks propagation by including a realistic carbide size distribution as well as by accounting for heterogeneous stress distribution at the microstrutural scale:

$$p_f^i   = \int_0^{+\infty}  \Frac{2 \alpha_r}{\beta_r}  \left( \Frac{2 r - \gamma_r}{\beta_r}   \right)^{\alpha_r - 1}  \exp{\left( -  \left[ \Frac{2 r - \gamma_r}{\beta_r}   \right]^{\alpha_r}    \right) }    \exp{\left( -  \left[  \sqrt{\Frac{E \pi \gamma_f}{2 (1-\nu^2) r}}  \Frac{1}{k_H  \max{\left(\sigma_I, 0 \right) }}   \right]^{m_H}    \right) }     dr    \quad \mathrm{for} \quad \varepsilon_{eq} > 0   $$

Ductile fracture
---------------

# Strain based ductile fracture indicator

Various models have been proposed to predict the equivalent plastic strain at the onset of ductile fracture $\varepsilon_{eq}^c$. As proposed by Johnson and Cook [@johnson_cook_1985], a general framework relies on the definition of a damage indicator $D$:

$$ D = \int \Frac{d \varepsilon_{eq} }{\varepsilon_{eq}^c} $${#eq:mfront:fracturecriteria:ductile_fracture:damage_indicator}

such as $D=1$ corresponds to fracture. This formulation allows to extend models for critical quivalent plastic strain, mostly derived for proportional loading conditions, to non-proportional loading conditions.

> **Note n°1**
> In practice, Equation @eq:mfront:fracturecriteria:ductile_fracture:damage_indicator is integrated using the midpoint rule. 

> **Note n°2**
> $\varepsilon_{eq}^c$ should be strictly positive. Otherwise (such as bad choices of material parameters), the increment of damage is set to zero.

> **Note n°3**
> Von Mises equivalent plastic strain $\varepsilon_{eq}$ and stress $\sigma_{eq}$ are considred in the following. A potential extension could be to consider other equivalent stresses (and associated equivalent strain) such as Hill, Hosford, ... 

Various models proposed in the literature for the critical quivalent plastic strain $\varepsilon_{eq}^c$ are available in `MFront`:

## Freudenthal1950 [@freudenthal_alfredm_inelastic_1950]

* **Inputs**: stress tensor $\bm{\sigma}$, Equivalent plastic strain $\varepsilon_{eq}$
* **Parameter**: $D_1$

Freudenthal stated that "for conditions of vanishing volumetric strain the fracture condition and the work-hardening function have the same form" *,i.e.,* that fracture criterion is related to dissipated energy. The rate of the latter can be written as $\sigma_{eq} \dot{\varepsilon}_{eq}$, hence the associated fracture criterion corresponds to consider:
	
$$ \varepsilon_{eq}^c = \Frac{D_1}{\sigma_{eq}} $$	

in Equation @eq:mfront:fracturecriteria:ductile_fracture:damage_indicator.

## CockcroftLatham1968 [@cockcroft_latham_1968]

* **Inputs**: stress tensor $\bm{\sigma}$, Equivalent plastic strain $\varepsilon_{eq}$
* **Parameter**: $D_1$
   
Cockroft and Latham argued that a ductile fracture criterion based on the total plastic work, like Freudenthal's, can not capture the effect of stress triaxiality, like the one observed during a tensile test at necking. They proposed to consider that the fracture criterion is related to $\sigma_I^+ \dot{\varepsilon}_{eq}$, where $\sigma_I^+$ is the positive part of the maximal principal stress, corresponding to consider:
   
 $$ \varepsilon_{eq}^c = \Frac{D_1}{\max{(\sigma_{I},0)}} $$
 
in Equation @eq:mfront:fracturecriteria:ductile_fracture:damage_indicator.
 
## RiceTracey1969 [@rice_tracey_1969]

* **Input**: stress tensor $\bm{\sigma}$, Equivalent plastic strain $\varepsilon_{eq}$, strain rate tensor $\dot{\bm{\varepsilon}}$
* **Parameters**: $D_1$

Rice and Tracey derived approximate expressions for the growth of a spherical void of radius $R$ in an infinite matrix material following von Mises plasticity. More precisely, the expressions given are of the form:

$$\Frac{\dot{R}}{R} = \mathcal{F}(\bm{\sigma}) \dot{\varepsilon}_{eq}$$

For proportional loadings, integration leads to $\ln{(R/R_0)} = \mathcal{F}(\bm{\sigma}) \varepsilon_{eq}$, which provide a fracture strain assuming that fracture occurs for a critical void enlargement.
	
Combining results for positive and negative mean stresses, Rice and Tracey results lead to:

 $$ \varepsilon_{eq}^c = \Frac{D_1}{0.558 \sinh{\left( \Frac{3}{2} \Frac{\sigma_{H}}{\sigma_{eq}}  \right) } + 0.008 \nu \cosh{\left( \Frac{3}{2} \Frac{\sigma_{H}}{\sigma_{eq}}  \right) }}  \quad \mathrm{with} \quad \nu = -3\Frac{\dot{\varepsilon}_{II}}{\dot{\varepsilon}_{I} - \dot{\varepsilon}_{III}} $$ 
 
 where $\sigma_H$ the hydrostatic stress, $\varepsilon_{I} \geq \varepsilon_{II} \geq \varepsilon_{III}$  the principal components of the strain rate tensor.
 
## RiceTracey1969HighStressTriaxiality [@rice_tracey_1969]
	
* **Input**: stress tensor $\bm{\sigma}$, Equivalent plastic strain $\varepsilon_{eq}$
* **Parameters**: $D_1$

For large positive mean stress, Rice and Tracey model reduces to:	
 $$ \varepsilon_{eq}^c = \Frac{D_1}{0.279} \exp{\left(-\Frac{3}{2} \Frac{\sigma_{H}}{\sigma_{eq}}      \right)  }  $$
 
## GeneralizedRiceTracey

* **Input**: stress tensor $\bm{\sigma}$, Equivalent plastic strain $\varepsilon_{eq}$
* **Parameters**: $D_1$, $D_2$

A generalized version of the RiceTracey1969 high stress triaxiality model consists in considering the $3/2$ prefactor as a material parameter:

 $$ \varepsilon_{eq}^c = \Frac{D_1}{0.279} \exp{\left(-D_2 \Frac{\sigma_{H}}{\sigma_{eq}}      \right)  }  $$
 	
## HancockMcKenzie1976 [@hancock_mckenzie_1976]

* **Input**: stress tensor $\bm{\sigma}$, Equivalent plastic strain $\varepsilon_{eq}$
* **Parameters**: $D_1$, $D_2$

Hancock and McKenzie extended the Rice and Tracey high stress triaxiality criterion by considering that voids nucleate after a given equivalent plastic strain, leading to:
	
 $$ \varepsilon_{eq}^c = D_1 + D_2 \exp{\left( -\Frac{3}{2}  \Frac{\sigma_{H}}{\sigma_{eq}}      \right)  }  $$
 
## GeneralizedHancockMcKenzie

* **Input**: stress tensor $\bm{\sigma}$, Equivalent plastic strain $\varepsilon_{eq}$
* **Parameters**: $D_1$, $D_2$, $D_3$

A generalized version of the HancockMcKenzie1976 consists in considering the $3/2$ prefactor as a material parameter:
	
 $$ \varepsilon_{eq}^c = D_1 + D_2 \exp{\left( -D_3  \Frac{\sigma_{H}}{\sigma_{eq}}      \right)  }  $$
 
## JohnsonCook1985 [@johnson_cook_1985]

* **Input**: stress tensor $\bm{\sigma}$,  Equivalent plastic strain $\varepsilon_{eq}$, Temperature $T$
* **Parameters**: $D_1$, $D_2$, $D_3$, $D_4$, $D_5$, reference equivalent plastic strain rate $\dot{\varepsilon}_{eq}^{ref}$, reference temperature $T_{ref}$, fusion temperature $T_{fus}$

Johnson & Cook extended phenomenologically the Hancock & McKenzie criterion by adding strain rate and temperature effects: 
	
 $$ \varepsilon_{eq}^c = \left[ D_1 + D_2 \exp{\left( - D_3  \Frac{\sigma_{H}}{\sigma_{eq}}      \right)  }  \right]   \left[ 1 +  D_4 \log{\left( \Frac{\dot{\varepsilon}_{eq}}{\dot{\varepsilon}_{eq}^{ref}}    \right)  }\right]  \left[ 1 +  D_5 \Frac{T - T_{ref}}{T_{fus} - T_{ref}} \right]  $$
  
## Huang1991 [@huang_1991]
	
* **Input**: stress tensor $\bm{\sigma}$, Equivalent plastic strain $\varepsilon_{eq}$
* **Parameters**: $D_1$

Huang refined the Rice & Tracey analysis to provide an expression of void growth rate valid for small and large stress triaxialities, leading to:
		
 $$ \varepsilon_{eq}^c = \Frac{D_1}{0.43} \left[ \min{\left(\Frac{\sigma_{H}}{\sigma_{eq}} ,1 \right)}   \right]^{-1/4} \exp{\left(-\Frac{3}{2} \Frac{\sigma_{H}}{\sigma_{eq}}      \right)  }  $$

## GeneralizedHuang

* **Input**: stress tensor $\bm{\sigma}$, Equivalent plastic strain $\varepsilon_{eq}$
* **Parameters**: $D_1$, $D_2$

A generalized version of the Huang1991 consists in considering the $3/2$ prefactor as a material parameter:

 $$ \varepsilon_{eq}^c = \Frac{D_1}{0.43} \left[ \max{\left(\Frac{\sigma_{H}}{\sigma_{eq}} ,1 \right)}   \right]^{-1/4} \exp{\left(-D_2 \Frac{\sigma_{H}}{\sigma_{eq}}      \right)  }  $$
 
# References {.unnumbered}
