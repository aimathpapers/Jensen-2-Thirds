import mpmath as mp
mp.mp.dps = 50
def dTheta(t):  return mp.nsum(lambda m: -mp.pi*m**2*mp.e**(-mp.pi*m**2*t), [1, mp.inf])
def d2Theta(t): return mp.nsum(lambda m: (mp.pi*m**2)**2*mp.e**(-mp.pi*m**2*t), [1, mp.inf])
def omega(t):   return (2*t**2*d2Theta(t) + 3*t*dTheta(t)) / 2
def gamma_true(nmax):
    xi = lambda z: mp.mpf(0.5)*(mp.mpf(0.5)+z)*(z-mp.mpf(0.5)) \
        * mp.pi**(-(mp.mpf(0.5)+z)/2) * mp.gamma((mp.mpf(0.5)+z)/2) * mp.zeta(mp.mpf(0.5)+z)
    co = mp.taylor(xi, 0, 2*nmax, method='quad', radius=mp.mpf(1)/2)
    return [co[2*n]*mp.factorial(n) for n in range(nmax+1)]
NODES=[0,mp.mpf(1)/8,mp.mpf(1)/4,mp.mpf(1)/2,1,2,3,5,8,12]
g = gamma_true(6)
print("corrected identity:  gamma(n) = 8 n!/(2n)! * int_0^inf omega(e^{2u}) e^{u/2} u^{2n} du")
for n in range(7):
    I = mp.quad(lambda u: omega(mp.e**(2*u))*mp.e**(u/2)*u**(2*n), NODES)
    val = 8*mp.factorial(n)/mp.factorial(2*n)*I
    print(f"  n={n}: rel.diff from true gamma(n) = {mp.nstr(abs(val/g[n]-1),6)}")
