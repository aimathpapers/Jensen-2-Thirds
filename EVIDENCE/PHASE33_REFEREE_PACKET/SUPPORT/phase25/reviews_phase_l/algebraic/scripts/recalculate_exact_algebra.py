#!/usr/bin/env python3
"""Definition-first exact recalculation for Phase-L gates B1--B5.

The program uses only integers and ``fractions.Fraction``.  It does not read
the candidate packet, JSON ledgers, result files, or any frozen expected
value.  Every test input and every comparison quantity is constructed below
from the displayed mathematical definitions.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q
from math import comb, factorial


@dataclass(frozen=True)
class Dual:
    """A rational value with a four-coordinate forward derivative."""

    value: Q
    grad: tuple[Q, Q, Q, Q]

    @staticmethod
    def constant(value: Q | int) -> "Dual":
        return Dual(Q(value), (Q(0),) * 4)

    def __add__(self, other: "Dual | Q | int") -> "Dual":
        rhs = other if isinstance(other, Dual) else Dual.constant(other)
        return Dual(self.value + rhs.value, tuple(a + b for a, b in zip(self.grad, rhs.grad)))

    __radd__ = __add__

    def __neg__(self) -> "Dual":
        return Dual(-self.value, tuple(-a for a in self.grad))

    def __sub__(self, other: "Dual | Q | int") -> "Dual":
        return self + (-other if isinstance(other, Dual) else -Q(other))

    def __rsub__(self, other: "Dual | Q | int") -> "Dual":
        return (-self) + other

    def __mul__(self, other: "Dual | Q | int") -> "Dual":
        rhs = other if isinstance(other, Dual) else Dual.constant(other)
        return Dual(
            self.value * rhs.value,
            tuple(self.value * b + rhs.value * a for a, b in zip(self.grad, rhs.grad)),
        )

    __rmul__ = __mul__

    def reciprocal(self) -> "Dual":
        if self.value == 0:
            raise ZeroDivisionError
        return Dual(1 / self.value, tuple(-a / self.value**2 for a in self.grad))

    def __truediv__(self, other: "Dual | Q | int") -> "Dual":
        rhs = other if isinstance(other, Dual) else Dual.constant(other)
        return self * rhs.reciprocal()

    def __rtruediv__(self, other: "Dual | Q | int") -> "Dual":
        return Dual.constant(other) / self

    def __pow__(self, exponent: int) -> "Dual":
        if exponent < 0:
            return (self.reciprocal()) ** (-exponent)
        if exponent == 0:
            return Dual.constant(1)
        return Dual(
            self.value**exponent,
            tuple(Q(exponent) * self.value ** (exponent - 1) * a for a in self.grad),
        )


def inverse_and_determinant(matrix: list[list[Q]]) -> tuple[list[list[Q]], Q]:
    n = len(matrix)
    work = [row[:] + [Q(i == j) for j in range(n)] for i, row in enumerate(matrix)]
    determinant = Q(1)
    for col in range(n):
        pivot = next(row for row in range(col, n) if work[row][col])
        if pivot != col:
            work[col], work[pivot] = work[pivot], work[col]
            determinant = -determinant
        pivot_value = work[col][col]
        determinant *= pivot_value
        work[col] = [entry / pivot_value for entry in work[col]]
        for row in range(n):
            if row == col:
                continue
            multiplier = work[row][col]
            work[row] = [a - multiplier * b for a, b in zip(work[row], work[col])]
    return [row[n:] for row in work], determinant


def matmul(a: list[list[Q]], b: list[list[Q]]) -> list[list[Q]]:
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
            for i in range(len(a))]


def leading_map(alpha: Dual, t: Dual, w: Dual, delta: Dual) -> tuple[Dual, ...]:
    return (
        1 / alpha + w / t**2 + delta - 2,
        w / t**3 + delta - 1,
        3 * w / t**4 + 3 * delta - 2,
        4 * w / t**5 + 4 * delta - 2,
    )


def check_b1() -> None:
    values = (Q(3), Q(2), Q(16, 3), Q(1, 3))
    variables = tuple(Dual(v, tuple(Q(i == j) for j in range(4))) for i, v in enumerate(values))
    outputs = leading_map(*variables)
    assert all(item.value == 0 for item in outputs)
    jacobian = [list(item.grad) for item in outputs]
    inverse, determinant = inverse_and_determinant(jacobian)
    identity = [[Q(i == j) for j in range(4)] for i in range(4)]
    assert matmul(jacobian, inverse) == identity
    assert matmul(inverse, jacobian) == identity
    inverse_norm = max(sum(abs(entry) for entry in row) for row in inverse)

    # Reconstruct uniqueness from the last three defining equations.
    # 3*F1-F2 gives 3*w*(t-1)=t^4; (4/3)*F2-F3 gives
    # 6*w*(t-1)=t^5.  Positivity then forces t=2.
    t, w, delta = Q(2), Q(16, 3), Q(1, 3)
    f1 = w / t**3 + delta - 1
    f2 = 3 * w / t**4 + 3 * delta - 2
    f3 = 4 * w / t**5 + 4 * delta - 2
    assert 3 * f1 - f2 == 3 * w * (t - 1) / t**4 - 1 == 0
    assert Q(4, 3) * f2 - f3 == 4 * w * (t - 1) / t**5 - Q(2, 3) == 0

    # The manuscript's displayed label "3 t F2 - F3" is not the claimed
    # algebraic identity.  Demonstrate this at a definition-built off-zero point.
    t, w, delta = Q(3), Q(5), Q(1, 4)
    f2 = 3 * w / t**4 + 3 * delta - 2
    f3 = 4 * w / t**5 + 4 * delta - 2
    claimed_left = 3 * t * f2 - f3
    claimed_right = 3 * w * (t - 1) - t**4
    assert claimed_left != claimed_right
    print(f"B1 exact: det={determinant}, inverse_inf_norm={inverse_norm}; "
          "published elimination label falsified")


def second_difference(values: list[Q], k: int) -> Q:
    return values[k + 2] - 2 * values[k + 1] + values[k]


def check_b2() -> None:
    source = [Q(2), Q(-1, 3), Q(7, 5), Q(11, 7), Q(-13, 9), Q(17, 11)]
    rebuilt = [source[0], source[1]]
    for k in range(4):
        rebuilt.append(second_difference(source, k) + 2 * rebuilt[k + 1] - rebuilt[k])
    assert rebuilt == source
    # Exponentiation is injective on real logarithms; quotient equality plus
    # the first two normalizations therefore fixes all six coefficients.
    print("B2 exact: four second differences plus two initial values rebuild all six entries")


def pochhammer(x: Q, k: int) -> Q:
    result = Q(1)
    for j in range(k):
        result *= x + j
    return result


def coefficients(d: int, a: Q, b: Q, c: Q, lower_d: Q, lam: Q) -> list[Q]:
    return [pochhammer(Q(-d), k) * pochhammer(a, k) * pochhammer(c, k) * lam**k /
            (pochhammer(b, k) * pochhammer(lower_d, k) * factorial(k))
            for k in range(d + 1)]


def polynomial_derivative(coeffs: list[Q], m: int) -> list[Q]:
    result = coeffs[:]
    for _ in range(m):
        result = [Q(k + 1) * result[k + 1] for k in range(len(result) - 1)]
    return result


def eval_poly(coeffs: list[Q], y: Q) -> Q:
    result = Q(0)
    for coefficient in reversed(coeffs):
        result = result * y + coefficient
    return result


def direct_coefficients(a: Q, b: Q, c: Q, lower_d: Q, y: Q, d: int, m: int) -> tuple[Q, ...]:
    epsilon = (c - lower_d) / c
    rec_a = 1 - y / a

    def rec_b(index: int) -> Q:
        return b + index - y + Q(d - 1 - 2 * index) * y / a

    def rec_c(index: int) -> Q:
        return Q(d - index) * (1 + Q(index) / a) * y

    beta = a * (2 * m + 1 - d) - d * (2 * m + 1) + 3 * m**2 + 3 * m + 1
    gamma = Q(m) * (m - d) * (m + a)
    return (
        rec_a + epsilon * y / a,
        rec_b(m + 1) + (lower_d + m) * rec_a + epsilon * y / a * (a - d + 3 + 3 * m),
        rec_c(m + 1) + (lower_d + m) * rec_b(m) + epsilon * y / a * beta,
        (lower_d + m) * rec_c(m) + epsilon * y / a * gamma,
    )


def ode_coefficients(a: Q, b: Q, c: Q, lower_d: Q, lam: Q, y: Q,
                     d: int, m: int) -> tuple[Q, ...]:
    roots = (Q(m - d), a + m, c + m)
    e1 = sum(roots)
    e2 = roots[0] * roots[1] + roots[0] * roots[2] + roots[1] * roots[2]
    e3 = roots[0] * roots[1] * roots[2]
    return (
        1 - lam * y,
        b + m + lower_d + m + 1 - lam * y * (3 + e1),
        (b + m) * (lower_d + m) - lam * y * (1 + e1 + e2),
        -lam * y * e3,
    )


def check_b3_b4() -> None:
    cases = (
        (5, Q(37), Q(19), Q(23), Q(11), Q(17, 5)),
        (7, Q(61, 2), Q(17), Q(29), Q(13), Q(31, 7)),
        (9, Q(53), Q(31), Q(41, 2), Q(15), Q(47, 9)),
    )
    count = 0
    for d, a, b, c, lower_d, y in cases:
        lam = lower_d / (a * c)
        base = coefficients(d, a, b, c, lower_d, lam)
        # The definition itself terminates: the next coefficient has (-d)_d+1=0.
        assert pochhammer(Q(-d), d + 1) == 0
        for m in range(d + 1):
            shifted = coefficients(d - m, a + m, b + m, c + m, lower_d + m, lam)
            derivative = polynomial_derivative(base, m)
            prefactor = Q(factorial(m)) * base[m]
            assert derivative == [prefactor * value for value in shifted]
            count += len(shifted)
            for k in range(d - m):
                lhs = shifted[k + 1] * (b + m + k) * (lower_d + m + k) * (k + 1)
                rhs = shifted[k] * lam * (k + m - d) * (a + m + k) * (c + m + k)
                assert lhs == rhs
                count += 1
            ode = ode_coefficients(a, b, c, lower_d, lam, y, d, m)
            direct = direct_coefficients(a, b, c, lower_d, y, d, m)
            assert ode == direct
            jets = [y**j * eval_poly(polynomial_derivative(shifted, j), y) for j in range(4)]
            assert sum(ode[3 - j] * jets[j] for j in range(4)) == 0
            count += 5
    print(f"B3/B4 exact: {count} independently generated termination, shift, ODE, and recurrence identities")


def finite_free_ascending(d: int, p: list[Q], q: list[Q]) -> list[Q]:
    return [Q((-1) ** k) * p[k] * q[k] / comb(d, k) for k in range(d + 1)]


def finite_free_descending(d: int, p: list[Q], q: list[Q]) -> list[Q]:
    return [Q((-1) ** (d - k)) * p[k] * q[k] / comb(d, k) for k in range(d + 1)]


def check_b5() -> None:
    checks = 0
    for d in range(1, 10):
        p = [Q((k + 2) * (d + 5), 2 * k + 1) for k in range(d + 1)]
        q = [Q((3 * k + 1) * (d + 7), k + 2) for k in range(d + 1)]
        reverse = lambda values: list(reversed(values))
        assert reverse(finite_free_ascending(d, p, q)) == finite_free_descending(
            d, reverse(p), reverse(q)
        )
        checks += d + 1

        a, b, c, lower_d = Q(20 * d + 7), Q(10 * d + 3), Q(14 * d + 5), Q(8 * d + 1)
        first = coefficients(d, a, b, Q(1), Q(1), 1 / a)
        second = coefficients(d, c, lower_d, Q(1), Q(1), lower_d / c)
        model = coefficients(d, a, b, c, lower_d, lower_d / (a * c))
        assert finite_free_ascending(d, first, second) == model
        assert model[0] == 1
        checks += d + 2
    print(f"B5 exact: {checks} convention/reflection/factorization coefficient checks")


def main() -> None:
    check_b1()
    check_b2()
    check_b3_b4()
    check_b5()
    print("PASS definition-first exact algebra recalculation")


if __name__ == "__main__":
    main()
