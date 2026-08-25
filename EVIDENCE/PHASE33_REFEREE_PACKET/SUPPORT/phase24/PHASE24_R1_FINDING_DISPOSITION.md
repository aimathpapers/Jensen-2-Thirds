# Phase 24 correlated AI re-review finding disposition

Date: 2026-08-17
Reviewed source commit: `7bb179ef62f979d58f2587db87a19d0c1f77b28d`
Reports: correlated Claude Opus 5 AI re-reviews; not separated first passes;
not human or peer review

## Verdict intake

The actual analytic and algebraic Phase-24 reports both returned `R1`, with
the same two manuscript-only P1 findings and no P0. The constant-32 algebraic
paragraph supplied alongside the comments was an older report; its threshold
finding was already repaired before commit `7bb179e` and is not a current
finding.

## Disposition

| Finding | Severity | Disposition |
|---|---:|---|
| False `eq:factor8` prefactor and kernel weight | P1 | Accepted. The manuscript now states `8 n!/(2n)!` and `e^{u/2}`, derives the convention from the Riemann kernel, and has an independent high-precision xi/integral regression. |
| False `eq:radius` display | P1 | Accepted. The manuscript now states the `y^k p_F^(k)/p_F` bound for `1<=k<=d` and records `T_0=1`; a fixed legal comparison polynomial regression distinguishes it from the stale formula. |
| Multiplier-stability lemma omitted | P2 | Accepted. The complete degree, holomorphy, reality, match, endpoint, error, and critical-point hypotheses and the Newton/Cauchy sign proof are now in the manuscript. |
| Two-thirds exponent arithmetic omitted | P2 | Accepted. The manuscript displays `rho^6 << n^3 d^3` and the resulting `d^3/(n^2 log(n+2))` defect, with `rho>=d`. |
| Localization constant disconnected from derivation | P2 | Accepted as an assurance/exposition issue, not a correctness defect. The proof now uses the derived `C_loc=12+8 sqrt(6)<32`; the exact ledger reconstructs `B/D<=6`, `d/D<=1/256`, positivity threshold 256, cross term 4, and `K_0=262144`. |
| Gaussian step cited only nonvanishing | P2 | Accepted. The manuscript now states the `Im L_s`, `arg K_s`, and right-half-plane estimates that control the Gaussian. |
| Undefined `M(ell)` and inconsistent saddle bound | P3 | Accepted. `m(ell)` and `M_theta(ell)` are defined, used consistently, and the lower bound `|L_N|>=ell/2` is promoted into Lemma S. |
| Endpoint connectors said to vanish; concavity hypotheses compressed | P3 | Accepted. The exponential connector estimate and the fixed angle/imaginary-saddle hypotheses are stated. |
| Radius maximum included undefined `k=0` root | P3 | Accepted with the P1 radius correction. |
| Release gates could not detect false displays | P3 | Accepted. Structural mutation gates now cover both corrected equations, and `manuscript_equation_regression.py` independently checks the factor-eight identity and a legal critical-point radius fixture. |
| Primary citations not retrieved by the reviewers | P3 / unchecked | Not a source defect. `PRIMARY_SOURCE_AUDIT.md` remains the direct AI-assisted source audit; new reviewers must record which primary PDFs they independently retrieve and check. |

## Review separation consequence

These reports cannot close the Phase-24 review gate because the same model
retained its prior-review context. They are retained as valuable repair
evidence only. The repaired source must be re-frozen and sent to reviewers
with no prior reports, responses, dispositions, or provider/session memory.
