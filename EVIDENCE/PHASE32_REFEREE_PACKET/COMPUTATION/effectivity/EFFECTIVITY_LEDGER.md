# Phase H constant and threshold ledger

The machine-readable source is `EFFECTIVITY_LEDGER.json`, regenerated from
exact arithmetic by `effectivity_ledger.py`. Its dependency order is acyclic.

The fully numerical chain is:

1. `C_J=8`;
2. `C_loc=12+8 sqrt(6)<32`;
3. `K_pre=256`, then `K_0=256*32^2=262144`;
4. `C_0=48`, `C_1<96`, then the explicit safe choice `K_r=4096`;
5. exact caps for the constant and vanishing recurrence neighbors, Jacobi
   localization, and `d+2 rho<=eta n`;
6. `x_admissible`, the minimum of those exact `d/n` caps;
7. `K_geometry=ceil(x_admissible^(-3))+1`, using
   `log(n+2)<=n` for `n>=2`.

This gives a fully explicit—extremely non-optimal—constant for the finite
geometry, recurrence, radius, and domain-containment parts. It does not give a
fully numerical theorem constant.

Two quantities remain symbolic:

- `C_B6`, the absolute constant in the assembled uniform complex
  sixth-derivative estimate;
- `N_analytic`, the maximum threshold required by the sectorial saddle error,
  branch `C^1` convergence, and analytic assembly.

All other paper-level analytic constants have been consolidated into those
two disclosed inputs. Put

```text
N_0 = max(N_explicit, N_analytic)
K_finite = N_0^2 (N_0+2) + 1
K_final = max(K_geometry, C_multiplier_factor*C_B6, K_finite).
```

The polynomial `K_finite` safely dominates
`n^2 log(n+2)` below `N_0`; it avoids pretending that the unknown threshold
has a numerical logarithm. The exact multiplier factor includes the
`1/720` simplex mass, the conservative six Newton factors, `B<=3n`, the
chosen `K_r`, and the elementary `|exp(E)-1|<=2|E|` step.

Accordingly the theorem is effective in principle, but no useful or fully
numerical `K` is claimed. The empirical `10.7/L_n` contraction diagnostic and
the illustrative `10^1887` scale are not dependencies of `K_final`.
