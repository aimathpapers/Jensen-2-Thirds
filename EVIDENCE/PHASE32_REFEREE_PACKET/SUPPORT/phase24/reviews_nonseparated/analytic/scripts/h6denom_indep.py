"""Independent check of H_6's reduced denominator, term count, and the
coefficientwise majorant bound on the bidisc |r|,|sigma| <= 7/50."""
import sympy as sp

N, L, r, sig = sp.symbols('N L r sigma')

Q = (1 + L) * N - sp.Rational(3, 4) * L**2
G0 = (N + 1) * sp.log(L) + L / 4 - N / L - sp.Rational(1, 2) * sp.log(Q)


def D(e):
    return sp.diff(e, N) + (L / Q) * sp.diff(e, L)


cur = G0
for _ in range(6):
    cur = sp.together(sp.cancel(D(cur)))

H6 = (N ** 5) * L * cur
H6 = H6.subs({L: 1 / r, N: 1 / (r * sig)})
H6 = sp.cancel(sp.together(sp.simplify(H6)))

num, den = sp.fraction(sp.cancel(H6))
num = sp.expand(num)
den = sp.expand(den)

print("denominator factored:", sp.factor(den))
print("claimed (4+4r-3sigma)^12 matches:",
      sp.simplify(sp.expand(den - (4 + 4 * r - 3 * sig) ** 12)) == 0)

P = sp.Poly(num, r, sig)
terms = P.terms()
print("numerator: #terms =", len(terms), " total degree =", P.total_degree())

# coefficientwise majorant on |r|,|sigma| <= 7/50
b = sp.Rational(7, 50)
maj = sum(abs(c) * b ** (a1 + a2) for (a1, a2), c in terms)
denom_low = (sp.Rational(151, 50)) ** 12
bound = sp.nsimplify(maj / denom_low)
print("majorant/denominator =", bound)
print("as float:", float(bound))
print("< 10^4 :", bound < 10 ** 4)

# the packet's displayed exact value
packet = sp.Rational(6422139805764931584036533551104,
                     702576099728137594188684005)
print("equals packet's displayed rational:", sp.simplify(bound - packet) == 0)
print("packet value as float:", float(packet))

# sigma = 0 slice
print("H6(r,0) =", sp.cancel(sp.simplify(H6.subs(sig, 0))))
