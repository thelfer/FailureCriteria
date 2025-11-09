---
title: The FailureCriteria project
author: Jérémy Hure, Thomas Helfer
date: 08/11/2026
lang: en-EN
link-citations: true
colorlinks: true
figPrefixTemplate: "$$i$$"
tblPrefixTemplate: "$$i$$"
secPrefixTemplate: "$$i$$"
eqnPrefixTemplate: "($$i$$)"
---
\newcommand{\Frac}[2]{{{\displaystyle \frac{\displaystyle #1}{\displaystyle #2}}}}

The project `FailureCriteria` provides `MFront` implementations of
various criteria to predict brittle and ductile failure.
Those implementations can be used in uncoupled analyses, in the
post-processing of the computations, or coupled analyses where the criteria are for example used along with an element deletion strategy.

Available criteria
==================

Brittle failure
---------------

# Probabilistic brittle failure

Various models have been proposed to predict the failure probability of metal alloys at the local scale $p_f$. The global failure probability $P_f$ is then obtained considering the weakest link assumption:

$$ P_f = 1 - \Pi_{i}(1 - p_f^i) \approx 1 - \exp{ \left(  - \int_V p_f \Frac{dV}{V_0} \right)} $${#eq:mfront:failurecriteria:brittle_failure:global_fracture_probability}

where $V_0$ is a normalization volume.

> **Note n°1**
> `MFront` only computes the local failure probability $p_f$ defined at each Gauss point. The user should then compute the global failure probability $P_f$ according to the Equation @eq:mfront:failurecriteria:brittle_failure:global_fracture_probability which requires the volume associated with each Gauss point.

> **Note n°2**
> From a physical point of view, the local failure probability should be a monotonic function, which is enforced in the numerical implementations by considering $\max{(p_f^{new},p_f^{old})}$

The models available in `MFront` for the local failure probability $p_f$ are:

## Beremin (1983)
	
$$p_f = \max{\left[   \left(\Frac{\sigma_I}{\sigma_u}\right)^m   ,0   \right] } $$

where $\sigma_I$ is the largest principal stress.

* **Input**: Cauchy Stress tensor $\bm{\sigma}$
* **Parameters**: reference stress $\sigma_u$, exponent $m$
	
## Ruggieri and Dodds (2015)
	
$$p_f = \left[ 1 - \exp{\left( - \Frac{\varepsilon_{eq}}{\varepsilon_{eq}^{ref}}  \right) }    \right]  \max{\left[   \left(\Frac{\sigma_I}{\sigma_u}\right)^m   ,0   \right] }   $$

where $\sigma_I$ is the largest principal stress, and $\varepsilon_{eq}$ the equivalent plastic strain. 

* **Input**: Cauchy Stress tensor $\bm{\sigma}$, equivalent plastic strain $\varepsilon_{eq}$
* **Parameters**: reference stress $\sigma_u$, exponent $m$, reference equivalent plastic strain $\varepsilon_{eq}^{ref}$

## Forget, Marini and Vincent (2016)
	
$$p_f   =   n_c V_0 \int_0^{+\infty}  \Frac{2 \alpha_r}{\beta_r}  \left( \Frac{2 r - \gamma_r}{\beta_r}   \right)^{\alpha_r - 1}  \exp{\left( -  \left[ \Frac{2 r - \gamma_r}{\beta_r}   \right]^{\alpha_r}    \right) }    \exp{\left( -  \left[  \sqrt{\Frac{E \pi \gamma_f}{2 (1-\nu^2) r}}  \Frac{1}{k_H  \max{\left(\sigma_I, 0 \right) }}   \right]^{m_H}    \right) }     dr   $$

where $\sigma_I$ is the largest principal stress, and $r$ the carbide size. 

* **Input**: Cauchy Stress tensor $\bm{\sigma}$
* **Parameters**: carbide size distribution ($\alpha_r$, $\beta_r$, $\gamma_r$), carbide Young modulus $E$, carbide fracture energy $\gamma_f$, carbide volume density $n_c$, heterogeneity ($m_H$, $k_H$) 

Ductile failure
---------------

# Strain based ductile failure indicator

Various models have been proposed to predict the equivalent plastic strain $\varepsilon_{eq}$ at the onset of ductile failure $\varepsilon_{eq}^c$. A general framework relies on the definition of a damage indicator $D$ such as $D=1$ corresponds to failure:

$$ D = \int \Frac{d \varepsilon_{eq} }{\varepsilon_{eq}^c} $${#eq:mfront:failurecriteria:ductile_failure:damage_indicator}

> **Note**
> In practice, Equation @eq:mfront:failurecriteria:ductile_failure:damage_indicator is integrated using the midpoint rule. 

The models available in `MFront` are:

## Freudenthal (1950)
	
$$ \varepsilon_{eq}^c = \Frac{D_1}{\sigma_{eq}^{vM}} $$	
	
where $\sigma_{eq}^{vM}$ is the von Mises equivalent stress tensor.

* **Input**: Cauchy Stress tensor $\bm{\sigma}$
* **Parameters**: $D_1$
	
## Cockcroft and Latham (1968)
   
 $$ \varepsilon_{eq}^c = \Frac{D_1}{\max{(\sigma_{I},0)}} $$
 
 where $\sigma_I$ is the largest principal stress.
 
* **Input**: Cauchy Stress tensor $\bm{\sigma}$
* **Parameters**: $D_1$
   
## Rice and Tracey (1969)
	
 $$ \varepsilon_{eq}^c = D_1 \exp{\left( D_2  \Frac{\sigma_{eq}^{vM}}{\sigma_{H}}      \right)  }  $$
 
 where $\sigma_{eq}^{vM}$ is the von Mises equivalent stress tensor, and $\sigma_H$ the hydrostatic stress.
 
* **Input**: Cauchy Stress tensor $\bm{\sigma}$
* **Parameters**: $D_1$, $D_2$
	
## Hancock and McKenzie (1976)
	
 $$ \varepsilon_{eq}^c = D_1 + D_2 \exp{\left( D_3  \Frac{\sigma_{eq}^{vM}}{\sigma_{H}}      \right)  }  $$
 
 where $\sigma_{eq}^{vM}$ is the von Mises equivalent stress tensor, and $\sigma_H$ the hydrostatic stress.
 
* **Input**: Cauchy Stress tensor $\bm{\sigma}$
* **Parameters**: $D_1$, $D_2$, $D_3$
	
## Johnson and Cook (1985)
	
 $$ \varepsilon_{eq}^c = \left[ D_1 + D_2 \exp{\left( D_3  \Frac{\sigma_{eq}^{vM}}{\sigma_{H}}      \right)  }  \right]   \left[ 1 +  D_4 \log{\left( \Frac{\dot{\varepsilon}_{eq}}{\dot{\varepsilon}_{eq}^{ref}}    \right)  }\right]  \left[ 1 +  D_5 \Frac{T - T_{ref}}{T_{fus} - T_{ref}} \right]  $$
 
 where $\sigma_{eq}^{vM}$ is the von Mises equivalent stress tensor, $\sigma_H$ the hydrostatic stress.
 
* **Input**: Cauchy Stress tensor $\bm{\sigma}$, Temperature $T$
* **Parameters**: $D_1$, $D_2$, $D_3$, $D_4$, $D_5$, reference equivalent plastic strain rate $\dot{\varepsilon}_{eq}^{ref}$, reference temperature $T_{ref}$, fusion temperature $T_{fus}$

## Huang (1991)
	
 $$ \varepsilon_{eq}^c = D_1  \left[ \min{\left( \Frac{\sigma_{eq}^{vM}}{\sigma_{H}}   , 1 \right)   }  \right]^{1/4}      \exp{\left( D_2  \Frac{\sigma_{eq}^{vM}}{\sigma_{H}}      \right)  }  $$
 
 where $\sigma_{eq}^{vM}$ is the von Mises equivalent stress tensor, and $\sigma_H$ the hydrostatic stress.
 
* **Input**: Cauchy Stress tensor $\bm{\sigma}$
* **Parameters**: $D_1$, $D_2$
		
## Bai and Wierzbicki (2010)

# References {.unnumbered}
