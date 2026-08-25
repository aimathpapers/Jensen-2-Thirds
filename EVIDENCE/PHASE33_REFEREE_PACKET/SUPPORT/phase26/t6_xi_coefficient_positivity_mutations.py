#!/usr/bin/env python3
"""Fail closed on mutations of the direct xi-coefficient positivity proof."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/JensenWedge/XiCoefficientPositivity.lean"

REQUIRED = {
    "mode formula": ("riemannOmegaMode n t", 2),
    "pi source": ("Real.pi_gt_three", 1),
    "mode summability sources": ("summable_thetaTailD2_terms", 1),
    "mode summability first": ("summable_thetaTailD1_terms", 1),
    "omega sum identity": ("riemannOmega_eq_tsum", 1),
    "omega positivity": ("theorem riemannOmega_pos_of_one_le", 1),
    "amplitude positivity": ("theorem omegaLogAmplitude_pos", 1),
    "integrability source": ("integrableOn_pow_mul_omegaLogAmplitude", 1),
    "positive integral": ("setIntegral_pos_iff_support_of_nonneg_ae", 1),
    "coefficient positivity": ("theorem riemannXiCoefficientReal_pos", 1),
}


def validate(text: str) -> None:
    for label, (needle, count) in REQUIRED.items():
        if text.count(needle) != count:
            raise RuntimeError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS xi coefficient positivity source contract")
    mutations = {
        "pi lower bound disconnected": ("Real.pi_gt_three", "uncheckedPiBound"),
        "second-mode summability disconnected":
            ("summable_thetaTailD2_terms", "uncheckedSecondModeSummability"),
        "first-mode summability disconnected":
            ("summable_thetaTailD1_terms", "uncheckedFirstModeSummability"),
        "omega sum disconnected": ("riemannOmega_eq_tsum", "uncheckedOmegaSum"),
        "omega positivity disconnected":
            ("theorem riemannOmega_pos_of_one_le", "theorem uncheckedOmegaPos"),
        "amplitude positivity disconnected":
            ("theorem omegaLogAmplitude_pos", "theorem uncheckedAmplitudePos"),
        "integrability disconnected":
            ("integrableOn_pow_mul_omegaLogAmplitude", "uncheckedIntegrability"),
        "positive integral disconnected":
            ("setIntegral_pos_iff_support_of_nonneg_ae", "uncheckedIntegralPos"),
        "coefficient positivity disconnected":
            ("theorem riemannXiCoefficientReal_pos", "theorem uncheckedCoefficientPos"),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except RuntimeError:
            print(f"PASS xi coefficient positivity mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
