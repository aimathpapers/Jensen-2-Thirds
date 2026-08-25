# Candidate two-thirds Jensen wedge: proof-support status

Date: 2026-08-16
Classification: internal candidate theorem; not release-certified

## Executive verdict

The project does **not** yet contain a release-certified proof that may be
advertised as an established theorem.  It does contain a serious,
well-firewalled candidate proof with substantial exact, symbolic, numerical,
and Lean support.  Phase 21 now proves the previously open sector-uniform
holomorphic xi-coefficient asymptotic directly from the xi/Mellin integral.
The decisive unresolved item is fresh end-to-end adversarial review of that
new analytic chain and all transported downstream interfaces on one immutable
revision.

The exact candidate is: there exists an absolute `K>0` such that

```text
n^2 log(n+2) >= K d^3
```

implies that the degree-`d` Jensen polynomial of the xi coefficients has `d`
distinct negative real roots.  This is an asymptotic Jensen-hyperbolicity
claim, not a proof of RH and not a new zero-location theorem.

## Support matrix

| Proof interface | Present support | Lean status | Remaining obligation |
|---|---|---|---|
| Four-equation leading system and positive solution | Exact rational proof and independent recalculation | Kernel checked, `leanchecker` and standard-axiom audit pass | None for the finite algebra |
| Forward-difference/triangular normalization | Exact algebra and frozen symbolic producers | Kernel checked | None for the finite algebra |
| Elementary/gamma `C^1` map | Self-contained cube-integral paper proof plus numerical regression | Selected weights and signs checked; uniform calculus not formalized | Fresh end-to-end analytic review of the final text; optional formalization |
| Exact positive parameter branch | Fixed-inverse contraction paper proof; high-precision diagnostics | Finite inverse and uniqueness algebra checked | Depends on the paper `C^1` estimates and fifth saddle asymptotic |
| Sectorial saddle variable `L_N` (Lemma S) | Direct Rouche proof with explicit constants; endpoint and symbolic regressions | Not formalized | Conventional proof review; full Lean treatment would be substantial |
| GORTTW complex saddle asymptotic | New self-contained Phase-21 proof: exact reduction, shifted-ray localization, higher-theta suppression, moment ratio, and sectorial Stirling assembly | Not formalized | **Internally discharged, not release-cleared:** fresh hostile analytic review, P0/P1 repair, and downstream replay are required |
| Fifth/sixth logarithmic moment derivatives | Theorem 21B plus proportional-disk Cauchy transport, exact rational derivative identities, coefficientwise bidisc bound, and high-precision moment checks | Exact downstream finite algebra only | Internally discharged at paper level; fresh review of complex Cauchy geometry and normalization remains required |
| Jacobi roots, finite-free comparison, localization | Direct paper derivation, published MMP inputs, independent algebraic recalculation | Recurrence closed forms and maximum implication checked | Final-source review of the transported analytic/special-function hypotheses |
| Multiplier stability and sign transfer | Self-contained paper proof with exact threshold `16` | Geometric tail, relative signs, disjoint roots, scaling, and conditional assembly checked | Requires the concrete analytic certificate |
| Candidate theorem | Complete paper architecture and a conditional Lean theorem | **Conditional only**; no analytic claim is installed as an axiom | Discharge all analytic premises and instantiate the certificate |

## What the current Lean development proves

Lean proves the fragile finite portions: the leading-system solution and
uniqueness, matrix inverses, forward-difference identities, recurrence
coefficients, a dominant-maximum implication, the multiplier tail, sign
preservation, distinct interval roots, positive-to-negative scaling, and the
final implication from an explicit analytic certificate.  The selected axiom
audits contain only `propext`, `Classical.choice`, and `Quot.sound`.

Lean does **not** presently prove Lemma S, the GORTTW saddle asymptotic, the
uniform `C^1` convergence theorem, the complex polygamma and
Hermite--Genocchi estimates, or the source finite-free theorems.  The Python
programs reproduce algebra and provide regressions; they do not convert those
analytic statements into machine proofs.

Formalizing Lemma S is realistic in principle but is not a quick closure: it
requires explicit complex logarithm domains, Rouche on a moving disc,
holomorphic implicit patching, and all endpoint inequalities.  Formalizing it
would improve assurance but would not replace adversarial review of the
complete Phase-21 contour and coefficient-assembly chain.

## Review status

The analytic and algebraic reports are disclosed Claude Fable/Claude Opus AI
technical audits.  Their second rounds found no P0/P1 in the revisions they
reviewed, and all listed corrections have been incorporated.  Those reports
predate the Phase-21 direct saddle proof and do not review it.  Fresh separated
AI pre-review passes are being requested on the frozen candidate.  No human or
peer review is claimed.

## Minimum path to a defensible theorem

1. Run a fresh end-to-end hostile analytic and algebraic review against one
   frozen commit.  If only AI review is available, disclose that limitation
   prominently and avoid the words peer reviewed or independently certified.
2. Resolve every resulting P0/P1 and freeze one manuscript, evidence manifest,
   and reproducible verification command.
3. Optionally formalize Lemma S and then the elementary `C^1`/complex adapter
   layers.  Keep the existing conditional Lean firewall until each analytic
   certificate is constructed rather than assumed.

Until the fresh review and defect-resolution loop is complete, the honest
classification is **internally complete paper-proof candidate, not a
release-certified or peer-reviewed theorem**.
