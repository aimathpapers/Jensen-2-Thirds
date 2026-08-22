# Phase 24 Mathematica M1--M4 verification record

Date: 2026-08-17

Classification: user-executed exact Mathematica verification using cells
supplied interactively by Codex; second-CAS evidence, not human or peer review

## Environment and provenance

- Mathematica: `15.0.1 for Mac OS X ARM (64-bit) (July 2, 2026)`
- System: `Mac OS X ARM (64-bit)`
- Processor: `ARM64`
- Recorded execution time: `2026-08-17T16:43:24`
- The user entered and executed the cells in Mathematica.
- No repository JSON, Python, SymPy, Lean-generated expression, or frozen
  numerator was imported by the notebook.
- The cells were supplied interactively by Codex, so this run breaks the
  SymPy-versus-Mathematica CAS common mode but is not independent human
  mathematical review.

## Exact results

| Gate | Result | Exact evidence |
|---|---|---|
| M1, saddle derivative tower | `MATCH` | Implicit derivative check `0`; post-chain constants `(2,-2,4,-12,48)`; fifth reduction matches; sixth denominator `(4+4r-3sigma)^12` |
| M2, shifted hypergeometric ODE | `MATCH` | Cross-multiplied coefficient recurrence `0`; four coefficient differences `(0,0,0,0)`; exact polynomial tests pass for every derivative order at degrees 5, 8, and 11 |
| M3, leading system | `MATCH` | Unique positive solution `(3,2,16/3,1/3)`; determinant `-1/144` in `(alpha,t,w,delta)` order; inverse infinity norm `304/3` |
| M4, sixth-order majorant | `MATCH` | 82-term degree-13 numerator; exact majorant `6422139805764931584036533551104/702576099728137594188684005 < 10000` |

Every mathematical result in the ledger is exact: the notebook's final
`ExactResultsContainNoMachineReals` field is `True`.

## Frozen artifacts

| Artifact | SHA-256 |
|---|---|
| `C48_Mathematica_CleanRoom_2.nb` | `f79359ce48fe5e5015bceb88b5de82b87145da22e235688dfe3989526772dc7a` |
| `C48_Mathematica_CleanRoom.pdf` | `f2e428bdd5d1caf03243b81dbc65794950abc2c8a4c13195395eca415d7a373c` |
| `C48_Mathematica_Result_Ledger.txt` | `1faea5fcb35b504b5d0aad9391999a99e530373dce36addb496eabb133fb04cc` |

`SHA256SUMS.txt` is the user-generated checksum ledger. The notebook and
plain-text result ledger are canonical. The frozen 13-page Mathematica PDF
was visually inspected; its inputs and compact outputs are legible, while
some long `InputForm` lines are clipped by Mathematica's print margins. No
mathematical value is taken from a clipped line: every full exact expression
is preserved in the notebook and result ledger.

## Scope

This evidence discharges the planned M1--M4 second-CAS reconstruction. It
does not construct the analytic xi certificate in Lean, formalize the paper
complex-analysis steps, or constitute human or peer review.
