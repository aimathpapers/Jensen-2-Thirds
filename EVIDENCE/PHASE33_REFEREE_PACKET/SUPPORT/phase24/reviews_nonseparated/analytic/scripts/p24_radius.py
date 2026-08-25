"""Compare the manuscript's printed radius statement (eq:radius) with the
statement the multiplier lemma actually consumes, on a concrete p_F."""
import mpmath as mp
mp.mp.dps = 60

# parameters from the numerically solved branch at n = 4000 (see earlier run)
n = 4000
A = mp.mpf('103773.4'); B = mp.mpf('9370.0')
C = mp.mpf('6664.7');   D = mp.mpf('4309.6')
d = 16
lam = D/(A*C)

# p_F(y) = 3F2(-d, A, C; B, D; lam y), ascending, constant term 1
coef = [mp.mpf(1)]
for j in range(d):
    coef.append(coef[-1] * (j - d) * (A + j) * (C + j)
                / ((B + j) * (D + j) * (j + 1)) * lam)
def p(y):   return sum(coef[j]*y**j for j in range(d+1))
def dp(k, y):
    return sum(coef[j]*mp.factorial(j)/mp.factorial(j-k)*y**(j-k)
               for j in range(k, d+1))

roots = mp.polyroots([coef[d-j] for j in range(d+1)], maxsteps=200, extraprec=200)
roots = sorted(mp.re(r) for r in roots)
print(f"  d={d}  B={float(B):.1f}  sqrt(Bd)={float(mp.sqrt(B*d)):.2f}")
print(f"  roots in [{float(roots[0]):.1f}, {float(roots[-1]):.1f}]"
      f"   |y-B| max = {float(max(abs(r-B) for r in roots)):.1f}"
      f"   C_loc needed = {float(max(abs(r-B) for r in roots)/mp.sqrt(B*d)):.3f}")
print(f"  all roots positive & distinct: {all(r>0 for r in roots)}, "
      f"{len(set(map(lambda z: mp.nstr(z,20), roots)))==d}")

crit = []
for i in range(d-1):
    crit.append(mp.findroot(lambda y: dp(1, y), (roots[i]+roots[i+1])/2))
print()
print("  At each critical point:  max_k |y^k p^(k)/p|^(1/k)   vs   max_k |p^(k)/(k! p)|^(1/k)")
print("   (the first is the hypothesis of the multiplier lemma; rho = K_r sqrt(Bd))")
mx1 = mx2 = mp.mpf(0)
for y in crit:
    py = p(y)
    t = max(abs(y**k*dp(k, y)/py)**(mp.mpf(1)/k) for k in range(1, d+1))
    s = max(abs(dp(k, y)/(mp.factorial(k)*py))**(mp.mpf(1)/k) for k in range(1, d+1))
    mx1 = max(mx1, t); mx2 = max(mx2, s)
print(f"    max over critical points of  |y^k p^(k)/p|^(1/k)      = {float(mx1):12.4f}"
      f"   -> K_r = {float(mx1/mp.sqrt(B*d)):.4f}")
print(f"    max over critical points of  |p^(k)/(k! p)|^(1/k)     = {float(mx2):12.8f}"
      f"   -> ratio to sqrt(Bd) = {float(mx2/mp.sqrt(B*d)):.3e}")
print(f"    the two differ by a factor ~ {float(mx1/mx2):.3e}   (~ y ~ B = {float(B):.0f})")
