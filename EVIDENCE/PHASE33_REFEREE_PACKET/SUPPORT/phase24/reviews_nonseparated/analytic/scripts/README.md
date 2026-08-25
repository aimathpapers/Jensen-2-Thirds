# Phase-24 analytic pre-review — independent verification scripts

Python 3.12, `sympy==1.14.0`, `mpmath==1.3.0`. Written from the mathematical
definitions during the review; no packet JSON, producer script, or Lean artifact
is used as an input.

| Script | Gate | Result |
|---|---|---|
| `p24_factor8.py` | A0 | Manuscript eq. (1) fails: RHS/gamma(n) = 1.09, 4.74, 9.94, 13.7, 14.1, 11.6 for n=0..5. **Finding 1.** |
| `p24_factor8b.py` | A0 | Corrected identity `gamma(n) = 8 n!/(2n)! * int omega(e^{2u}) e^{u/2} u^{2n} du` verified to 40+ digits, n=0..6. |
| `p24_contour.py` | A2, A3 | Contour identity to working precision at complex s, arg s = 1/200 and 1/400; \|Im L\| and \|arg K\| ~ 0.004; \|E1\|\*\|K\| = 0.1275 / 0.1128. |
| `p24_cauchy.py` | A4 | h^(m)(n) n^(m-1) L_n via Cauchy circle integrals of the true Mellin h: (1.593, -1.832, 3.960, -12.544, 52.318) at n=400. Third independent path. |
| `p24_radius.py` | A10 | Manuscript eq:radius vs the statement the multiplier lemma needs, on a concrete p_F (n=4000, d=16): 340.83 (K_r=0.880) vs 0.02321. Factor 1.47e4. **Finding 2.** |
| `h6denom_indep.py` | A5 | (4+4r-3s)^12 denominator, 82 terms, degree 13, exact majorant 9140.8458 < 1e4. |
| `saddle_indep.py` | A4 | Exact rational derivative tower D^m G_0, m=2..6, from scratch. |

Lemma S (A1), C_loc (Finding 5), and Hermite-Genocchi 1/720 (A9) were checked in
inline one-off runs; the arithmetic is reproduced in the report.
