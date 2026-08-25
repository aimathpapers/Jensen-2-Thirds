# Phase 9 decision checkpoint

Date: 2026-08-15  
Disposition: signed saddle gate passes internally; advance to model-side
uniform derivative bounds and combined `C^1` assembly

Exact differentiation of Holland's full saddle main term confirms the
normalized fifth coefficient `-6`.  The `N=2x-2` chain rule converts this to
the required coefficient `-12` for `h^(5)`.  Holland's already published
order-five sectorial remainder estimate and the elementary explicit
normalization terms are strictly smaller, yielding the desired signed
asymptotic at paper level.

The result has not yet received an independent hostile review and is not
Lean-formalized.  Its exact rational main-term calculation is reproducible
under a pinned symbolic environment, and the known fourth coefficient is
recovered as a regression.

The parameter campaign therefore continues.  The next bounded task is to
prove the elementary two-Jacobi map and all parameter derivatives have
uniform error `O(1/L_n+L_n/n)` on an explicit compact box, then combine them
with the signed xi finite differences.  The later `h^(6)` and root-stability
problems remain separate release blockers.
