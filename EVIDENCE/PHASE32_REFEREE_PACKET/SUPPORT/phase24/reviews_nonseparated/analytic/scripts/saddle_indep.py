"""Independent recomputation of the saddle-main-term derivative tower.

Nothing here reads the packet's frozen JSON artifacts.
"""
import sympy as sp

N, L, r, sig = sp.symbols('N L r sigma', positive=True)

Q = (1 + L) * N - sp.Rational(3, 4) * L**2
G0 = (N + 1) * sp.log(L) + L / 4 - N / L - sp.Rational(1, 2) * sp.log(Q)


def D(expr):
    return sp.diff(expr, N) + (L / Q) * sp.diff(expr, L)


tower = {}
cur = G0
for m in range(1, 7):
    cur = sp.together(sp.simplify(D(cur)))
    tower[m] = cur

# scale: N^{m-1} L * D^m G0, then substitute L = 1/r, N = 1/(r*sigma)
print("=== scaled tower in (r, sigma) ===")
scaled = {}
for m in range(2, 7):
    e = (N ** (m - 1)) * L * tower[m]
    e = e.subs({L: 1 / r, N: 1 / (r * sig)})
    e = sp.simplify(sp.cancel(sp.together(e)))
    scaled[m] = e
    lim0 = sp.simplify(e.subs(sig, 0))
    print(f"m={m}: sigma=0 reduction  =", sp.simplify(sp.cancel(lim0)))
    print(f"      value at r=0,sig=0  =", sp.simplify(sp.limit(lim0, r, 0)))
    print()

# Explicit check of the packet's claimed sigma=0 rational functions
claim5 = -(6*r**6 + 42*r**5 + 126*r**4 + 210*r**3 + 146*r**2 + 47*r + 6)/(1+r)**7
claim4 = (2*r**4 + 10*r**3 + 20*r**2 + 11*r + 2)/(1+r)**5
claim6 = (24*r**8 + 216*r**7 + 864*r**6 + 2016*r**5 + 3024*r**4
          + 2399*r**3 + 1042*r**2 + 242*r + 24)/(1+r)**9

for m, claim in ((4, claim4), (5, claim5), (6, claim6)):
    diff = sp.simplify(sp.cancel(scaled[m].subs(sig, 0) - claim))
    print(f"m={m}: scaled(sigma=0) - packet claim =", diff)

# Is the difference from the sigma=0 value really O(sigma)?
print()
for m in (5, 6):
    e = sp.cancel(sp.together(scaled[m] - scaled[m].subs(sig, 0)))
    num, den = sp.fraction(e)
    num = sp.expand(num)
    print(f"m={m}: numerator divisible by sigma? ->",
          sp.simplify(sp.rem(num, sig, sig)) == 0)
    print(f"      denominator at (r,sig)=(0,0) =", den.subs({r: 0, sig: 0}))
