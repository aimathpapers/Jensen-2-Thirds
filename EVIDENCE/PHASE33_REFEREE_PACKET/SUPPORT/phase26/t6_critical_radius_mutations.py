#!/usr/bin/env python3
"""Fail closed on the complete finite critical-radius argument."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean"
    / "Zeta23/Research/JensenWedge/CriticalRadiusRecurrence.lean"
)


class ContractError(RuntimeError):
    """The critical-radius source contract changed."""


REQUIRED = {
    "actual finite supremum": "Finset.exists_mem_eq_sup' hs",
    "maximum contraction": "dominantMaximum_le_one hq",
    "terminal derivative": "terminal : T (d + 1) = 0",
    "positive center": "center_pos : ∀ m, m + 2 ≤ d → 0 < P2 m",
    "genuine four-term recurrence": "recurrence : ∀ m, m + 2 ≤ d →",
    "denominator-free contraction": "coefficient_contraction : ∀ m, m + 2 ≤ d →",
    "terminal case consumed": "rw [hm3eq, C.terminal]",
    "recurrence consumed": "have hrec := C.recurrence m hmRange",
    "coefficient bound consumed": "C.coefficient_contraction m hmRange",
    "complete radius theorem": (
        "theorem FourTermCriticalRadiusCertificate.derivative_radius"
    ),
}


def validate(source: str) -> None:
    for label, needle in REQUIRED.items():
        if needle not in source:
            raise ContractError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS complete finite critical-radius source contract")
    mutations = {
        "finite supremum removed": (
            "Finset.exists_mem_eq_sup' hs",
            "uncheckedMaximumWitness",
        ),
        "maximum contraction bypassed": (
            "dominantMaximum_le_one hq",
            "uncheckedMaximumContraction hq",
        ),
        "terminal derivative hidden": (
            "terminal : T (d + 1) = 0",
            "uncheckedTerminal : T (d + 1) = 0",
        ),
        "center positivity hidden": (
            "center_pos : ∀ m, m + 2 ≤ d → 0 < P2 m",
            "uncheckedCenterPos : ∀ m, m + 2 ≤ d → 0 < P2 m",
        ),
        "recurrence hidden": (
            "recurrence : ∀ m, m + 2 ≤ d →",
            "uncheckedRecurrence : ∀ m, m + 2 ≤ d →",
        ),
        "coefficient contraction hidden": (
            "coefficient_contraction : ∀ m, m + 2 ≤ d →",
            "uncheckedCoefficientContraction : ∀ m, m + 2 ≤ d →",
        ),
        "terminal consumer bypassed": (
            "rw [hm3eq, C.terminal]",
            "rw [hm3eq, uncheckedTerminal]",
        ),
        "recurrence consumer bypassed": (
            "have hrec := C.recurrence m hmRange",
            "have hrec := uncheckedRecurrence m hmRange",
        ),
        "coefficient consumer bypassed": (
            "C.coefficient_contraction m hmRange",
            "uncheckedCoefficientContraction m hmRange",
        ),
        "radius conclusion disconnected": (
            "theorem FourTermCriticalRadiusCertificate.derivative_radius",
            "theorem uncheckedDerivativeRadius",
        ),
    }
    for label, (old, new) in mutations.items():
        if old not in source:
            raise AssertionError(f"mutation target changed: {label}")
        changed = source.replace(old, new)
        try:
            validate(changed)
        except ContractError:
            print(f"PASS critical-radius mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
