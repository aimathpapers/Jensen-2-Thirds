#!/usr/bin/env python3
"""High-precision regression for Phase-21 Lemma 21A.

The script integrates the normalized shifted-u contour.  It corroborates, but
does not prove, the sectorial contour and error estimate.
"""

import mpmath as mp


mp.mp.dps = 45


def saddle(s: mp.mpc) -> mp.mpc:
    guess = mp.log(s) - mp.log(mp.log(s)) - mp.log(mp.pi)
    return mp.findroot(lambda ell: ell * (mp.pi * mp.exp(ell) + mp.mpf(3) / 4) - s, guess)


def check_one(radius: int, angle: str) -> tuple[mp.mpf, mp.mpf]:
    theta = mp.mpf(angle)
    s = mp.mpf(radius) * mp.exp(1j * theta)
    ell = saddle(s)
    alpha = mp.re(ell)
    beta = mp.im(ell)
    kappa = s * (1 / ell + 1 / ell**2) - mp.mpf(3) / 4

    def phase(u: mp.mpc) -> mp.mpc:
        return s * mp.log(u) + u / 4 - mp.pi * mp.exp(u)

    center = phase(ell)

    def normalized(u: mp.mpc) -> mp.mpc:
        return mp.exp(phase(u) - center)

    # The endpoint and vertical connector are exponentially below the saddle
    # and underflow at the tested precision.  The regression targets the
    # nontrivial horizontal localization; their exact inclusion is proved in
    # the paper note rather than inferred numerically.
    horizontal = mp.quad(
        lambda x: normalized(x + 1j * beta),
        [1, alpha - 1, alpha, alpha + 1, alpha + 6],
    )

    gaussian = mp.sqrt(2 * mp.pi / kappa)
    ratio = horizontal / gaussian
    error = abs(ratio - 1)
    scaled = error * abs(kappa)

    print(
        "radius={} angle={} ImL={} |K|={} ratio={} |ratio-1|={} scaled={}".format(
            radius,
            angle,
            mp.nstr(beta, 10),
            mp.nstr(abs(kappa), 12),
            mp.nstr(ratio, 18),
            mp.nstr(error, 10),
            mp.nstr(scaled, 10),
        )
    )
    return error, scaled


def main() -> None:
    theorem_results = [
        check_one(200, "0.0"),
        check_one(200, "0.005"),
        check_one(200, "0.01"),
        check_one(800, "0.0"),
        check_one(800, "0.005"),
        check_one(800, "0.01"),
    ]
    small = [result[0] for result in theorem_results[:3]]
    large = [result[0] for result in theorem_results[3:]]
    if not max(large) < max(small):
        raise SystemExit("FAIL: contour error did not decrease with radius")
    if not max(result[1] for result in theorem_results) < 5:
        raise SystemExit("FAIL: |K|-scaled contour error exceeded regression gate")
    print("PASS: leading contour ratios converge with bounded |K|-scaled error")

    # This deliberately reaches far beyond the proved |arg s| <= 1/100 sector.
    # It is a robustness diagnostic only and does not enlarge the theorem.
    robustness_results = [
        check_one(200, "0.1"),
        check_one(200, "0.3"),
        check_one(200, "0.6"),
        check_one(200, "1.0"),
        check_one(200, "1.4"),
        check_one(800, "1.4"),
        check_one(3200, "1.4"),
    ]
    if not max(result[1] for result in robustness_results) < 8:
        raise SystemExit("FAIL: wide-angle robustness diagnostic exceeded gate")
    print("PASS: wide-angle contour robustness diagnostic through 1.4 radians")

    ell = mp.mpf(12)
    m12 = ell - mp.log(ell + 1) - mp.log(mp.pi) - 1
    imag_bound = (mp.mpf("0.01") + mp.mpf("0.0002")) / (1 - 1 / m12)
    if not imag_bound < mp.mpf("0.012"):
        raise SystemExit("FAIL: direct Im(L) bootstrap did not close")
    print("PASS: direct Im(L) bootstrap is below 0.012 at log|s| = 12")


if __name__ == "__main__":
    main()
