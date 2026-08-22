import Zeta23.Research.JensenWedge.PolynomialRootIntervals
import Zeta23.Research.JensenWedge.XiNaturalMultiplierEndpoint

/-!
# Concrete xi multiplier interval certificate

This module turns the concrete multiplier estimate into the exact
`MultiplierIntervalCertificate` consumed by the final root-transfer theorem.
The comparison intervals are constructed from the MMP root list by reversing
it into increasing order and inserting canonical Rolle points.
-/

namespace Zeta23.Research.JensenWedge

open Complex Finset Metric Polynomial Set

noncomputable section

/-- MMP supplies roots in decreasing log-mesh order; sign transfer uses the
same roots in increasing order. -/
def xiNaturalAscendingComparisonRoots
    {n d : ℕ} {L : ℝ} {y : BranchPoint}
    (I : XiNaturalClassicalRootInputs n d L y) : Fin d → ℝ :=
  fun i ↦ I.mmp.roots i.rev

theorem xiNaturalAscendingComparisonRoots_strictMono
    {n d : ℕ} {L : ℝ} {y : BranchPoint}
    (I : XiNaturalClassicalRootInputs n d L y) :
    StrictMono (xiNaturalAscendingComparisonRoots I) := by
  exact I.mmp.strict_log_mesh.strictAnti.comp Fin.rev_strictAnti

theorem xiNaturalAscendingComparisonRoots_pos
    {n d : ℕ} {L : ℝ} {y : BranchPoint}
    (I : XiNaturalClassicalRootInputs n d L y) :
    ∀ i, 0 < xiNaturalAscendingComparisonRoots I i := by
  intro i
  exact I.mmp.strict_log_mesh.positive i.rev

theorem xiNaturalAscendingComparisonRoots_zero
    {n d : ℕ} {L : ℝ} {y : BranchPoint}
    (I : XiNaturalClassicalRootInputs n d L y) :
    ∀ i, (xiNaturalComparisonPolynomial n d L y).eval
      (xiNaturalAscendingComparisonRoots I i) = 0 := by
  intro i
  simpa only [xiNaturalAscendingComparisonRoots,
    xiNaturalComparisonFunction] using I.mmp.roots_are_zeros i.rev

theorem xiNaturalComparisonPolynomial_coeff_zero_of_explicitCutoff
    {n : ℕ} (hn : xiNaturalExplicitCutoffIndex ≤ n) (d : ℕ) :
    (xiNaturalComparisonPolynomial n d (xiNaturalSaddleScale n)
      (exactXiPositiveParameterBranch_of_explicitCutoff hn).parameters).coeff 0 = 1 := by
  rw [← xiNaturalModelLogPolynomial_eq_comparison_of_explicitCutoff hn d,
    coeff_xiNaturalModelLogPolynomial, if_pos (Nat.zero_le d)]
  simp [xiNaturalModelLogCoordinate]

theorem xiNaturalComparisonPolynomial_ne_zero_of_explicitCutoff
    {n : ℕ} (hn : xiNaturalExplicitCutoffIndex ≤ n) (d : ℕ) :
    xiNaturalComparisonPolynomial n d (xiNaturalSaddleScale n)
      (exactXiPositiveParameterBranch_of_explicitCutoff hn).parameters ≠ 0 := by
  intro hp
  have hcoeff := xiNaturalComparisonPolynomial_coeff_zero_of_explicitCutoff hn d
  rw [hp] at hcoeff
  norm_num at hcoeff

theorem xiNaturalActualLogPolynomial_coeff_zero
    (n d : ℕ) (L : ℝ) (y : BranchPoint) :
    (xiNaturalActualLogPolynomial n d L y).coeff 0 = 1 := by
  rw [coeff_xiNaturalActualLogPolynomial, if_pos (Nat.zero_le d)]
  simp [xiNaturalActualLogCoordinate]

theorem xiNaturalComparisonPolynomial_natDegree_eq_of_explicitCutoff
    {n : ℕ} (hn : xiNaturalExplicitCutoffIndex ≤ n) (d : ℕ) :
    (xiNaturalComparisonPolynomial n d (xiNaturalSaddleScale n)
      (exactXiPositiveParameterBranch_of_explicitCutoff hn).parameters).natDegree = d := by
  apply Polynomial.natDegree_eq_of_le_of_coeff_ne_zero
    (terminating3F2Polynomial_natDegree_le d _ _ _ _ _)
  change (xiNaturalComparisonPolynomial n d (xiNaturalSaddleScale n)
    (exactXiPositiveParameterBranch_of_explicitCutoff hn).parameters).coeff d ≠ 0
  rw [← xiNaturalModelLogPolynomial_eq_comparison_of_explicitCutoff hn d,
    coeff_xiNaturalModelLogPolynomial, if_pos le_rfl]
  simp only [Nat.choose_self, Nat.cast_one, one_mul]
  exact mul_ne_zero
    (mul_ne_zero (neg_one_pow_ne_zero d) (by norm_num))
    (Real.exp_ne_zero _)

theorem xiNaturalActualLogPolynomial_natDegree_eq_of_explicitCutoff
    {n : ℕ} (hn : xiNaturalExplicitCutoffIndex ≤ n) (d : ℕ) :
    (xiNaturalActualLogPolynomial n d (xiNaturalSaddleScale n)
      (exactXiPositiveParameterBranch_of_explicitCutoff hn).parameters).natDegree = d := by
  apply Polynomial.natDegree_eq_of_le_of_coeff_ne_zero
  · rw [Polynomial.natDegree_le_iff_coeff_eq_zero]
    intro j hdj
    rw [coeff_xiNaturalActualLogPolynomial, if_neg (Nat.not_le_of_lt hdj)]
  · rw [coeff_xiNaturalActualLogPolynomial, if_pos le_rfl]
    exact mul_ne_zero
      (mul_ne_zero (neg_one_pow_ne_zero d) (by norm_num))
      (Real.exp_ne_zero _)

theorem xiNaturalConcreteRealMultiplier_top_error_lt_one
    {K : ℝ} (hK : xiNaturalConcreteWedgeConstant ≤ K)
    {n d : ℕ} (hn : xiNaturalExplicitCutoffIndex ≤ n)
    (hW : TwoThirdsWedge K n d) (hd : 6 ≤ d) :
    |xiNaturalConcreteRealMultiplier n (xiNaturalSaddleScale n)
        (exactXiPositiveParameterBranch_of_explicitCutoff hn).parameters d - 1| < 1 := by
  let c := xiNaturalConcreteMultiplier n (xiNaturalSaddleScale n)
    (exactXiPositiveParameterBranch_of_explicitCutoff hn).parameters
  have htube : (d : ℂ) ∈ xiNaturalMultiplierTube n d
      (xiNaturalSaddleScale n)
      (exactXiPositiveParameterBranch_of_explicitCutoff hn).parameters := by
    refine ⟨d, ⟨Nat.cast_nonneg d, le_rfl⟩, ?_⟩
    change ‖(d : ℂ) - (d : ℂ)‖ ≤ 8192 *
      Real.sqrt (residualParameterB
        (exactXiPositiveParameterBranch_of_explicitCutoff hn).parameters n
        (1 / xiNaturalSaddleScale n) * d)
    rw [sub_self, norm_zero]
    positivity
  have hcomplex := xiNaturalConcreteMultiplier_sub_one_norm_lt_one_on_tube
    hK hn hW hd htube
  have hre : |(c (d : ℂ) - 1).re| ≤ ‖c (d : ℂ) - 1‖ := abs_re_le_norm _
  change |(c (d : ℂ)).re - 1| < 1
  exact hre.trans_lt hcomplex

theorem xiNatural_leadingCoeff_ratio_error_lt_one
    {K : ℝ} (hK : xiNaturalConcreteWedgeConstant ≤ K)
    {n d : ℕ} (hn : xiNaturalExplicitCutoffIndex ≤ n)
    (hW : TwoThirdsWedge K n d) (hd : 6 ≤ d) :
    let y := (exactXiPositiveParameterBranch_of_explicitCutoff hn).parameters
    let L := xiNaturalSaddleScale n
    let p := xiNaturalComparisonPolynomial n d L y
    let P := xiNaturalActualLogPolynomial n d L y
    |P.leadingCoeff / p.leadingCoeff - 1| < 1 := by
  let y := (exactXiPositiveParameterBranch_of_explicitCutoff hn).parameters
  let L := xiNaturalSaddleScale n
  let p := xiNaturalComparisonPolynomial n d L y
  let P := xiNaturalActualLogPolynomial n d L y
  let c := xiNaturalConcreteRealMultiplier n L y
  have hpdeg : p.natDegree = d :=
    xiNaturalComparisonPolynomial_natDegree_eq_of_explicitCutoff hn d
  have hPdeg : P.natDegree = d :=
    xiNaturalActualLogPolynomial_natDegree_eq_of_explicitCutoff hn d
  have htransform : P = coefficientMultiplierTransform p c :=
    xiNaturalActualLogPolynomial_eq_comparisonMultiplierTransform_of_explicitCutoff hn d
  have hcoeff := congrArg (fun q : ℝ[X] ↦ q.coeff d) htransform
  rw [coeff_coefficientMultiplierTransform] at hcoeff
  have hplead : p.leadingCoeff = p.coeff d := by
    rw [← hpdeg, Polynomial.coeff_natDegree]
  have hPlead : P.leadingCoeff = P.coeff d := by
    rw [← hPdeg, Polynomial.coeff_natDegree]
  change |P.leadingCoeff / p.leadingCoeff - 1| < 1
  rw [hPlead, hplead, hcoeff]
  have hpcoeff : p.coeff d ≠ 0 := by
    rw [← hplead]
    exact Polynomial.leadingCoeff_ne_zero.mpr
      (xiNaturalComparisonPolynomial_ne_zero_of_explicitCutoff hn d)
  rw [mul_div_cancel_left₀ (c d) hpcoeff]
  exact xiNaturalConcreteRealMultiplier_top_error_lt_one hK hn hW hd

/-- The fully concrete interval certificate for degree `k+2`.  Its only
external argument is the typed Jacobi/MSS/MMP record `I`; the multiplier,
Rolle endpoints, right endpoint, and every relative-error field are produced
inside Lean. -/
def xiNatural_multiplierIntervalCertificate
    {K : ℝ} (hK : xiNaturalMultiplierEndpointWedgeConstant ≤ K)
    {n k : ℕ} (hn : xiNaturalExplicitCutoffIndex ≤ n)
    (hW : TwoThirdsWedge K n (k + 2)) (hk : 4 ≤ k)
    (I : XiNaturalClassicalRootInputs n (k + 2) (xiNaturalSaddleScale n)
      (exactXiPositiveParameterBranch_of_explicitCutoff hn).parameters) :
    MultiplierIntervalCertificate
      (xiNaturalComparisonPolynomial n (k + 2) (xiNaturalSaddleScale n)
        (exactXiPositiveParameterBranch_of_explicitCutoff hn).parameters).eval
      (xiNaturalActualLogPolynomial n (k + 2) (xiNaturalSaddleScale n)
        (exactXiPositiveParameterBranch_of_explicitCutoff hn).parameters).eval
      (k + 2) := by
  let y := (exactXiPositiveParameterBranch_of_explicitCutoff hn).parameters
  let L := xiNaturalSaddleScale n
  let d := k + 2
  let p := xiNaturalComparisonPolynomial n d L y
  let P := xiNaturalActualLogPolynomial n d L y
  let roots : Fin (k + 2) → ℝ := xiNaturalAscendingComparisonRoots I
  have hd : 6 ≤ d := by dsimp only [d]; omega
  have hmono : StrictMono roots :=
    xiNaturalAscendingComparisonRoots_strictMono I
  have hpos : ∀ i, 0 < roots i := xiNaturalAscendingComparisonRoots_pos I
  have hzeros : ∀ i, p.eval (roots i) = 0 :=
    xiNaturalAscendingComparisonRoots_zero I
  have hpdegree : p.natDegree ≤ k + 2 := by
    exact terminating3F2Polynomial_natDegree_le (k + 2) _ _ _ _ _
  have hp : p ≠ 0 :=
    xiNaturalComparisonPolynomial_ne_zero_of_explicitCutoff hn d
  have hpdeg : p.natDegree = d :=
    xiNaturalComparisonPolynomial_natDegree_eq_of_explicitCutoff hn d
  have hPdeg : P.natDegree = d :=
    xiNaturalActualLogPolynomial_natDegree_eq_of_explicitCutoff hn d
  have hP : P ≠ 0 := by
    intro hzero
    rw [hzero] at hPdeg
    simp only [Polynomial.natDegree_zero] at hPdeg
    omega
  have hdegreeEq : P.degree = p.degree := by
    rw [Polynomial.degree_eq_natDegree hP, Polynomial.degree_eq_natDegree hp,
      hPdeg, hpdeg]
  have hlead : |P.leadingCoeff / p.leadingCoeff - 1| < 1 :=
    xiNatural_leadingCoeff_ratio_error_lt_one
      (xiNaturalMultiplierEndpoint_ge_concrete.trans hK) hn hW hd
  have hexists := exists_right_relativeError_lt_one hdegreeEq hlead
    (roots (Fin.last (k + 1)))
  let right : ℝ := Classical.choose hexists
  have hright : roots (Fin.last (k + 1)) < right :=
    (Classical.choose_spec hexists).1
  have hrelright : |P.eval right / p.eval right - 1| < 1 :=
    (Classical.choose_spec hexists).2
  apply multiplierIntervalCertificate_of_complete_roots hmono hpos hzeros
    hpdegree hp hright
  · have hp0 : p.eval 0 = 1 := by
      rw [← Polynomial.coeff_zero_eq_eval_zero]
      exact xiNaturalComparisonPolynomial_coeff_zero_of_explicitCutoff hn d
    have hP0 : P.eval 0 = 1 := by
      rw [← Polynomial.coeff_zero_eq_eval_zero]
      exact xiNaturalActualLogPolynomial_coeff_zero n d L y
    rw [hp0, hP0]
    norm_num
  · intro i
    apply xiNaturalActualComparison_relativeError_lt_one_at_critical
      hK hn hW hd I
    · exact polynomialRollePoint_eval_ne_zero hmono hzeros hpdegree hp i
    · exact polynomialRollePoint_derivative hmono hzeros i
  · exact hrelright

/-- The concrete interval certificate together with the already proved xi
normalization is a full `JensenWedgeCertificate`. -/
def xiNatural_jensenWedgeCertificate
    {K : ℝ} (hK : xiNaturalMultiplierEndpointWedgeConstant ≤ K)
    {n k : ℕ} (hn : xiNaturalExplicitCutoffIndex ≤ n)
    (hW : TwoThirdsWedge K n (k + 2)) (hk : 4 ≤ k)
    (I : XiNaturalClassicalRootInputs n (k + 2) (xiNaturalSaddleScale n)
      (exactXiPositiveParameterBranch_of_explicitCutoff hn).parameters) :
    JensenWedgeCertificate (riemannXiJensenPolynomial n (k + 2)) (k + 2) := by
  let y := (exactXiPositiveParameterBranch_of_explicitCutoff hn).parameters
  let L := xiNaturalSaddleScale n
  let p := xiNaturalComparisonPolynomial n (k + 2) L y
  let P := xiNaturalActualLogPolynomial n (k + 2) L y
  let C := xiNaturalSaddleIntervalConditions_of_explicitCutoff hn
  let B := exactXiPositiveParameterBranch_of_explicitCutoff hn
  exact {
    comparison := p.eval
    transformed := P.eval
    intervals := xiNatural_multiplierIntervalCertificate hK hn hW hk I
    transformed_continuous := P.continuous
    scale := xiNaturalJensenScale n L y
    normalization := riemannXiCoefficientReal n
    scale_pos := xiNaturalJensenScale_pos C.n_pos C.saddleScale_pos B.in_outer_box
    normalization_ne_zero := (riemannXiCoefficientReal_pos n).ne'
    identify := by
      intro X
      rw [eval_xiNaturalActualLogPolynomial C.n_pos (k + 2)
        C.saddleScale_pos B.in_outer_box X]
      rfl
  }

/-- Root transfer from the exact actual-log polynomial to the untransformed
Riemann-xi Jensen polynomial. -/
theorem xiNaturalActualLogPolynomial_roots_to_riemannXi
    {n d : ℕ} {L : ℝ} {y : BranchPoint}
    (hn : 0 < n) (hL : 0 < L) (hy : InOuterParameterBox y)
    (H : HasDistinctPositiveRoots
      (xiNaturalActualLogPolynomial n d L y).eval d) :
    HasDistinctNegativeRoots (riemannXiJensenPolynomial n d) d := by
  rcases H with ⟨x, hxinj, hx⟩
  let scale := xiNaturalJensenScale n L y
  have hscale : 0 < scale := xiNaturalJensenScale_pos hn hL hy
  let z : Fin d → ℝ := fun i ↦ -x i / scale
  refine ⟨z, ?_, ?_⟩
  · intro i j hij
    apply hxinj
    dsimp only [z] at hij
    field_simp [hscale.ne'] at hij
    linarith
  · intro i
    constructor
    · exact div_neg_of_neg_of_pos (neg_neg_of_pos (hx i).1) hscale
    · have heval := eval_xiNaturalActualLogPolynomial hn d hL hy (x i)
      have hzero : (xiNaturalActualLogPolynomial n d L y).eval (x i) = 0 :=
        (hx i).2
      have htrans : xiNaturalTransformedPolynomial n d L y (x i) = 0 := by
        rw [← heval]
        exact hzero
      have hquot : riemannXiJensenPolynomial n d (-x i / scale) /
          riemannXiCoefficientReal n = 0 := by
        simpa only [xiNaturalTransformedPolynomial, scale] using htrans
      have hJ : riemannXiJensenPolynomial n d (-x i / scale) = 0 := by
        exact (div_eq_zero_iff.mp hquot).resolve_right
          (riemannXiCoefficientReal_pos n).ne'
      simpa only [z] using hJ

/-- Degrees zero through five are exact, because the six multiplier nodes are
identically one. -/
theorem riemannXiJensen_twoThirds_low_degree
    {n d : ℕ} (hn : xiNaturalExplicitCutoffIndex ≤ n) (hd : d ≤ 5)
    (I : XiNaturalClassicalRootInputs n d (xiNaturalSaddleScale n)
      (exactXiPositiveParameterBranch_of_explicitCutoff hn).parameters) :
    HasDistinctNegativeRoots (riemannXiJensenPolynomial n d) d := by
  let C := xiNaturalSaddleIntervalConditions_of_explicitCutoff hn
  let B := exactXiPositiveParameterBranch_of_explicitCutoff hn
  have heq : xiNaturalActualLogPolynomial n d (xiNaturalSaddleScale n) B.parameters =
      xiNaturalComparisonPolynomial n d (xiNaturalSaddleScale n) B.parameters := by
    rw [xiNaturalLogPolynomials_eq_of_degree_le_five C.n_pos hd
      C.saddleScale_pos B.in_outer_box B.equation]
    exact xiNaturalModelLogPolynomial_eq_comparison_of_explicitCutoff hn d
  have H : HasDistinctPositiveRoots
      (xiNaturalActualLogPolynomial n d (xiNaturalSaddleScale n) B.parameters).eval d := by
    rw [heq]
    exact I.mmp.hasDistinctPositiveRoots
  exact xiNaturalActualLogPolynomial_roots_to_riemannXi
    C.n_pos C.saddleScale_pos B.in_outer_box H

/-- Concrete headline theorem.  Apart from the explicit wedge and cutoff,
the sole hypotheses are the named typed Jacobi root/matrix, MSS finite-free
interval, and MMP strict-log-mesh inputs bundled in `I`.  The xi-specific
sixth multiplier, interval certificate, and target identification are all
constructed in Lean. -/
theorem riemannXiJensen_twoThirds_headline
    {K : ℝ} (hK : xiNaturalMultiplierEndpointWedgeConstant ≤ K)
    {n d : ℕ} (hn : xiNaturalExplicitCutoffIndex ≤ n)
    (hW : TwoThirdsWedge K n d)
    (I : XiNaturalClassicalRootInputs n d (xiNaturalSaddleScale n)
      (exactXiPositiveParameterBranch_of_explicitCutoff hn).parameters) :
    HasDistinctNegativeRoots (riemannXiJensenPolynomial n d) d := by
  by_cases hd : d ≤ 5
  · exact riemannXiJensen_twoThirds_low_degree hn hd I
  · have hd6 : 6 ≤ d := by omega
    obtain ⟨k, hk⟩ : ∃ k, d = k + 2 := by
      exact ⟨d - 2, by omega⟩
    subst d
    have hk4 : 4 ≤ k := by omega
    exact (xiNatural_jensenWedgeCertificate hK hn hW hk4 I).target_hasDistinctNegativeRoots

end

end Zeta23.Research.JensenWedge
