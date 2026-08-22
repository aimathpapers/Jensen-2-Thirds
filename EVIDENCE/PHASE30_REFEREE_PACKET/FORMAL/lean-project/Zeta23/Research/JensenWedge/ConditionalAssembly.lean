import Zeta23.Research.JensenWedge.MultiplierStability

/-!
# Conditional assembly of the two-thirds Jensen wedge

This module is the proof firewall between the analytic/special-function
inputs and the advertised root conclusion.  A `JensenWedgeCertificate`
contains only concrete comparison, relative-error, interval, continuity, and
scaling data.  From those data Lean proves that the target Jensen polynomial
has the required number of distinct negative roots.

The module deliberately does not assert that the Riemann-xi coefficients
supply such a certificate.  The sectorial saddle estimate, exact parameter
branch, finite-free positivity, and residual bound must be proved separately
and then used to construct the certificate.
-/

namespace Zeta23.Research.JensenWedge

/-- The proposed sixth-order wedge, written without hiding its coercions. -/
def TwoThirdsWedge (K : ℝ) (n d : ℕ) : Prop :=
  K * (d : ℝ) ^ 3 ≤ (n : ℝ) ^ 2 * Real.log (n + 2 : ℝ)

/-- Exact data sufficient for the final Holland-style sign transfer and the
positive-to-negative Jensen change of variables. -/
structure JensenWedgeCertificate (J : ℝ → ℝ) (d : ℕ) where
  comparison : ℝ → ℝ
  transformed : ℝ → ℝ
  intervals : MultiplierIntervalCertificate comparison transformed d
  transformed_continuous : Continuous transformed
  scale : ℝ
  normalization : ℝ
  scale_pos : 0 < scale
  normalization_ne_zero : normalization ≠ 0
  identify : ∀ y,
    transformed y = J (-y / scale) / normalization

theorem JensenWedgeCertificate.transformed_hasDistinctPositiveRoots
    {J : ℝ → ℝ} {d : ℕ} (C : JensenWedgeCertificate J d) :
    HasDistinctPositiveRoots C.transformed d :=
  C.intervals.actual_hasDistinctPositiveRoots C.transformed_continuous

/-- The conditional certificate implies exactly the `d` distinct negative
root conclusion used in the paper. -/
theorem JensenWedgeCertificate.target_hasDistinctNegativeRoots
    {J : ℝ → ℝ} {d : ℕ} (C : JensenWedgeCertificate J d) :
    HasDistinctNegativeRoots J d := by
  rcases C.transformed_hasDistinctPositiveRoots with ⟨x, hxinj, hx⟩
  let z : Fin d → ℝ := fun i => -x i / C.scale
  refine ⟨z, ?_, ?_⟩
  · intro i j hij
    apply hxinj
    dsimp [z] at hij
    have hscale : C.scale ≠ 0 := ne_of_gt C.scale_pos
    field_simp [hscale] at hij
    linarith
  · intro i
    have hxpos := (hx i).1
    have hxzero := (hx i).2
    constructor
    · dsimp [z]
      exact div_neg_of_neg_of_pos (neg_neg_of_pos hxpos) C.scale_pos
    · have hquot : J (-x i / C.scale) / C.normalization = 0 := by
        rw [← C.identify, hxzero]
      have hJ : J (-x i / C.scale) = 0 := by
        rcases (div_eq_zero_iff.mp hquot) with hJ | hnormalization
        · exact hJ
        · exact (C.normalization_ne_zero hnormalization).elim
      simpa [z] using hJ

/-- End-to-end conditional theorem.  Every analytic obligation is concentrated
in the construction of `certificate`; no global assumption declaration or hidden source claim
is introduced into the Lean environment. -/
theorem conditionalTwoThirdsWedge
    (J : ℕ → ℕ → ℝ → ℝ) (K : ℝ)
    (certificate : ∀ n d, TwoThirdsWedge K n d →
      JensenWedgeCertificate (J n d) d) :
    ∀ n d, TwoThirdsWedge K n d → HasDistinctNegativeRoots (J n d) d := by
  intro n d hnd
  exact (certificate n d hnd).target_hasDistinctNegativeRoots

end Zeta23.Research.JensenWedge
