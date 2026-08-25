#!/usr/bin/env python3
"""Fail-closed mutations for full-theta and coefficient holomorphy."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/"
    "JensenWedge/FullThetaHolomorphic.lean"
)


class ContractError(RuntimeError):
    """The holomorphic coefficient contract changed."""


def validate(text: str) -> None:
    required = {
        "real Mellin kernel": "def fullThetaMellinKernelReal (u : ℝ)",
        "kernel theta source": "riemannThetaTail (Real.exp u)",
        "infinity decay": "theorem fullThetaMellinKernelReal_isBigO_exp_neg",
        "Hurwitz source": "riemannThetaTail_eq_FNat_zero (Real.exp_pos u)",
        "zero endpoint": "theorem fullThetaMellinKernel_isBigO_zero",
        "exact Mellin bridge": "theorem fullThetaMoment_eq_mellin",
        "contour identity source": "fullThetaContourIntegrand_eq_thetaTail s u",
        "Mellin derivative source": "mellin_hasDerivAt_of_isBigO_rpow",
        "full moment holomorphy": "theorem differentiableAt_fullThetaMoment",
        "coefficient sector open": "theorem isOpen_leanCoefficientSector",
        "paired sector open": "theorem isOpen_leanXiCoefficientSector",
        "actual coefficient holomorphy":
            "theorem differentiableAt_complexXiCoefficientMoment",
        "Gamma quotient source": "hasDerivAt_complexFactorialRatio hMre",
        "main holomorphy": "theorem differentiableAt_complexXiCoefficientMain",
        "saddle main source": "hasDerivAt_saddleMomentMain hNouter",
        "branch source": "hasDerivAt_quantitativeSaddleBranch hNouter",
        "generic error equality":
            "theorem complexXiCoefficientRelativeError_eq_holomorphicRelativeError",
        "exact factorization source": "complexXiCoefficientMoment_factorization hM",
        "error holomorphy":
            "theorem differentiableOn_complexXiCoefficientRelativeError",
        "nonzero divisor source": "complexXiCoefficientMain_ne_zero hM",
        "holomorphic T5 export":
            "theorem complexXiCoefficient_sector_holomorphic_asymptotic",
        "pointwise T5 source": "complexXiCoefficient_sector_asymptotic hM",
    }
    counts = {
        "kernel theta source": 4,
        "nonzero divisor source": 2,
    }
    for label, needle in required.items():
        if text.count(needle) != counts.get(label, 1):
            raise ContractError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS T5 full-theta and coefficient holomorphy source contract")
    mutations = {
        "theta kernel disconnected": (
            "riemannThetaTail (Real.exp u)",
            "uncheckedThetaTail (Real.exp u)",
        ),
        "infinity decay removed": (
            "theorem fullThetaMellinKernelReal_isBigO_exp_neg",
            "theorem uncheckedKernelDecay",
        ),
        "Hurwitz producer disconnected": (
            "riemannThetaTail_eq_FNat_zero (Real.exp_pos u)",
            "uncheckedThetaHurwitzIdentity",
        ),
        "Mellin bridge removed": (
            "theorem fullThetaMoment_eq_mellin",
            "theorem uncheckedFullThetaMellin",
        ),
        "contour producer disconnected": (
            "fullThetaContourIntegrand_eq_thetaTail s u",
            "uncheckedContourThetaIdentity s u",
        ),
        "Mellin differentiation disconnected": (
            "mellin_hasDerivAt_of_isBigO_rpow",
            "uncheckedMellinDifferentiation",
        ),
        "paired sector openness removed": (
            "theorem isOpen_leanXiCoefficientSector",
            "theorem uncheckedPairedSectorOpen",
        ),
        "actual holomorphy removed": (
            "theorem differentiableAt_complexXiCoefficientMoment",
            "theorem uncheckedActualHolomorphy",
        ),
        "Gamma derivative disconnected": (
            "hasDerivAt_complexFactorialRatio hMre",
            "uncheckedGammaDerivative hMre",
        ),
        "saddle-main derivative disconnected": (
            "hasDerivAt_saddleMomentMain hNouter",
            "uncheckedSaddleMainDerivative hNouter",
        ),
        "branch derivative disconnected": (
            "hasDerivAt_quantitativeSaddleBranch hNouter",
            "uncheckedBranchDerivative hNouter",
        ),
        "generic error equality removed": (
            "theorem complexXiCoefficientRelativeError_eq_holomorphicRelativeError",
            "theorem uncheckedRelativeErrorEquality",
        ),
        "exact factorization disconnected": (
            "complexXiCoefficientMoment_factorization hM",
            "uncheckedCoefficientFactorization hM",
        ),
        "error holomorphy removed": (
            "theorem differentiableOn_complexXiCoefficientRelativeError",
            "theorem uncheckedErrorHolomorphy",
        ),
        "nonzero divisor disconnected": (
            "complexXiCoefficientMain_ne_zero hM",
            "uncheckedMainNonzero hM",
        ),
        "holomorphic export removed": (
            "theorem complexXiCoefficient_sector_holomorphic_asymptotic",
            "theorem uncheckedHolomorphicAsymptotic",
        ),
        "pointwise theorem disconnected": (
            "complexXiCoefficient_sector_asymptotic hM",
            "uncheckedPointwiseAsymptotic hM",
        ),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except ContractError:
            print(f"PASS T5 holomorphy mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
