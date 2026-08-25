"""h^(m)(n) via Cauchy circle integrals of the TRUE Mellin h -- a path
independent of both the symbolic tower and finite differences."""
import mpmath as mp
mp.mp.dps = 90
def L_of(s):
    w = mp.log(s)
    return mp.findroot(lambda L: L*(mp.pi*mp.e**L + mp.mpf(3)/4) - s,
                       w - mp.log(w) - mp.log(mp.pi))
def K_of(s,L): return s*(1/L+1/L**2)-mp.mpf(3)/4
def nodes(s):
    L=mp.re(L_of(s)); K=abs(K_of(s,L_of(s))); w=12/mp.sqrt(K)
    p={mp.mpf(0)}
    for c in range(-8,9):
        q=L+c*w/8
        if q>0: p.add(q)
    p |= {L+4*w, L+20*w, L+60}
    return sorted(p)
def F(s):
    nd=nodes(s)
    return sum(mp.quad(lambda u: mp.exp(s*mp.log(u)+u/4-mp.pi*k**2*mp.e**u), nd)
               for k in range(1,6))
def h(z):
    Mz = mp.mpf(2)**(-2*z-2)*(32*mp.binomial(2*z,2)*F(2*z-2)-F(2*z))
    return mp.log(Mz)
NP=32; R=mp.mpf(1)
print("   n     L_n    m=2      m=3      m=4      m=5      m=6   [claim 2,-2,4,-12,48]")
for n in (400, 1600):
    Ln=L_of(2*n-2)
    vals=[h(mp.mpf(n)+R*mp.exp(2j*mp.pi*j/NP)) for j in range(NP)]
    out=[]
    for m in (2,3,4,5,6):
        acc=sum(vals[j]*mp.exp(-2j*mp.pi*m*j/NP) for j in range(NP))
        dm = mp.factorial(m)*acc/(NP*R**m)
        out.append(float(mp.re(dm)*mp.mpf(n)**(m-1)*Ln))
    print(f" {n:5d} {float(Ln):7.4f} " + " ".join(f"{v:8.3f}" for v in out))
