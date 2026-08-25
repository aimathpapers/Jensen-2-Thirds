"""Gate A0: test the manuscript's eq:factor8 against the true xi coefficients.

Manuscript claim:  gamma(n) = 8 * 2^{2n} / (2n)! * int_0^inf omega(e^{2u}) e^u u^{2n} du
with omega(t) = (1/2)(2 t^2 Theta''(t) + 3 t Theta'(t)),  Theta(t) = sum_{m>=1} e^{-pi m^2 t}.
"""
import mpmath as mp
mp.mp.dps = 40

def Theta(t):   return mp.nsum(lambda m: mp.e**(-mp.pi*m**2*t), [1, mp.inf])
def dTheta(t):  return mp.nsum(lambda m: -mp.pi*m**2*mp.e**(-mp.pi*m**2*t), [1, mp.inf])
def d2Theta(t): return mp.nsum(lambda m: (mp.pi*m**2)**2*mp.e**(-mp.pi*m**2*t), [1, mp.inf])
def omega(t):   return (2*t**2*d2Theta(t) + 3*t*dTheta(t)) / 2

def gamma_true(nmax):
    xi = lambda z: mp.mpf(0.5)*(mp.mpf(0.5)+z)*(z-mp.mpf(0.5)) \
        * mp.pi**(-(mp.mpf(0.5)+z)/2) * mp.gamma((mp.mpf(0.5)+z)/2) * mp.zeta(mp.mpf(0.5)+z)
    co = mp.taylor(xi, 0, 2*nmax, method='quad', radius=mp.mpf(1)/2)
    return [co[2*n]*mp.factorial(n) for n in range(nmax+1)]

NODES = [0, mp.mpf(1)/4, mp.mpf(1)/2, 1, 2, 3, 5, 8]

def I_manuscript(n):   # int omega(e^{2u}) e^u u^{2n} du
    return mp.quad(lambda u: omega(mp.e**(2*u))*mp.e**u*u**(2*n), NODES)

def I_half(n):         # int omega(e^{2u}) e^{u/2} u^{2n} du
    return mp.quad(lambda u: omega(mp.e**(2*u))*mp.e**(u/2)*u**(2*n), NODES)

g = gamma_true(5)
print(" n    gamma(n) [true]      manuscript RHS        ratio        alt: 8*n!/(2n)! * I_half   ratio")
for n in range(0, 6):
    tr  = g[n]
    man = 8*mp.mpf(2)**(2*n)/mp.factorial(2*n)*I_manuscript(n)
    alt = 8*mp.factorial(n)/mp.factorial(2*n)*I_half(n)
    print(f"{n:2d}  {mp.nstr(tr,10):>18}  {mp.nstr(man,10):>18}  {mp.nstr(man/tr,8):>12}"
          f"   {mp.nstr(alt,10):>18}  {mp.nstr(alt/tr,8)}")
