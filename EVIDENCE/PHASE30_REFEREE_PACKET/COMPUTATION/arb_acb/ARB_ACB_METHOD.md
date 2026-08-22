# Phase G Arb/ACB verification method

`arb_acb_verification.py` uses `python-flint 0.6.0` with one thread and fixed
precision. Its committed JSON is regenerated twice and compared byte for byte
by `verify_phase25.sh`.

The coefficient check has three paths. The first expands
`xi(s)=s(s-1) pi^(-s/2) Gamma(s/2) zeta(s)/2` at `s=1/2` directly. The second
integrates the positive `omega` kernel. The third separately integrates the
two Mellin `F` moments in the Phase-21 coefficient combination. The latter two
use six theta modes on `0<=u<=4`; all omitted modes and the complete `u>4`
tail are bounded analytically using `exp(2u)>=1+2u`. Thus these coefficient
comparisons are not quadrature-with-an-unchecked-cutoff.

For each saddle sample box, a high-precision value supplies only an untrusted
center. Arb verifies a strict Rouché inequality with a quadratic remainder,
derivative nonvanishing, and a positive lower bound for `|Q|`. Those claims
hold for every parameter in the displayed small box. The contour, connector,
central-window, and higher-mode calculations are directed enclosures at three
points only. They do not prove uniformity on the full sector.

The derivative calculation solves the implicit saddle equation in the ACB
power-series ring and extracts orders two through six without importing the
SymPy or Mathematica derivative formulas. The Jensen checks form the actual
polynomials from direct completed-zeta coefficient balls and require isolated,
pairwise-disjoint negative-real root boxes.

The clean-room Mathematica notebook remains the independent decisive-symbolic
algebra channel. Phase G verifies its frozen hashes and exact M1--M4 ledger; it
does not reimplement that symbolic algebra in another CAS.

These checks materially strengthen confidence but are not human or peer
review, and finite grids are not presented as proof of the two-thirds wedge.
