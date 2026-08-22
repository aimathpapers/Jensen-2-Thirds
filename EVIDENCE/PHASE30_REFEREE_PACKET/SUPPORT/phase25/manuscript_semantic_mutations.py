#!/usr/bin/env python3
"""Source-connected mutations for the paper's repaired proof interfaces."""

from __future__ import annotations

from manuscript_release_checks import (
    APPENDICES,
    MAIN,
    SUPPLEMENT,
    check_load_bearing_text,
)


def rejected(name: str, mutated: str) -> None:
    try:
        check_load_bearing_text(mutated)
    except AssertionError:
        print(f"PASS manuscript semantic mutation rejected: {name}")
        return
    raise AssertionError(f"manuscript semantic mutation survived: {name}")


def replace_all(source: str, old: str, new: str) -> str:
    if old not in source:
        raise AssertionError(f"mutation anchor missing for {old!r}")
    return source.replace(old, new)


def main() -> None:
    source = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (MAIN, APPENDICES, SUPPLEMENT)
    )
    cases = (
        (
            "factor eight changed to four",
            r"8\int_0^\infty\omega(e^{2u})e^{u/2}u^{2n}",
            r"4\int_0^\infty\omega(e^{2u})e^{u/2}u^{2n}",
        ),
        ("horizontal contour made vertical", r"u=L_s+r", r"u=L_s+iv"),
        (
            "legal shifted ray changed to a full line",
            r"r\ge1-\Re L_s",
            r"r\in\R",
        ),
        (
            "phase absorbs the Jacobian and loses the saddle",
            r"\Phi_s(u)=s\operatorname{Log}u-\frac34u-\pi e^u",
            r"\Phi_s(u)=s\operatorname{Log}u+\frac14u-\pi e^u",
        ),
        (
            "leading contour alias is disconnected",
            r"I_1(s):=F_1(s):=\int_0^\infty g_s(u)\,\dd u",
            r"I_1(s):=\int_0^\infty g_s(u)\,\dd u",
        ),
        ("auxiliary moment changed to gamma", r"h(z):=\log M_z", r"h(x)=\log\gamma(x)"),
        (
            "global maximum changed to first failure",
            r"\mathcal M=\max_{0\le j\le d}",
            r"\mathcal M=\text{first-failure induction}",
        ),
        (
            "leading-system elimination transposed",
            r"3F_1-F_2=\frac{3w(t-1)}{t^4}-1",
            r"3tF_2-F_3=3w(t-1)-t^4",
        ),
        (
            "branch evidence overclaimed",
            "does not purport to compute",
            "does compute",
        ),
        (
            "gamma-factor subtraction omitted",
            "subtracting the explicit gamma factors",
            "using the coefficient main term directly",
        ),
        ("horizontal tail variable made stale", r"|r|=1", r"|v|=1"),
        (
            "expanded recurrence gains an extra m",
            r"P_{2,m}&=B+D+2m+1",
            r"P_{2,m}&=B+D+3m+1",
        ),
        (
            "effectivity threshold name made undefined",
            r"N_0=\max\{N_{\rm analytic},N_{\rm explicit}\}",
            r"N_0=\max\{N_{\rm analytic},N_{\rm elementary}\}",
        ),
        (
            "complete axiom audit changed to incomplete predecessor",
            r"Phase26Axioms.lean",
            "Phase-20 axiom report",
        ),
    )
    for name, old, new in cases:
        rejected(name, replace_all(source, old, new))
    print("PASS all manuscript semantic mutations fail on production source")


if __name__ == "__main__":
    main()
