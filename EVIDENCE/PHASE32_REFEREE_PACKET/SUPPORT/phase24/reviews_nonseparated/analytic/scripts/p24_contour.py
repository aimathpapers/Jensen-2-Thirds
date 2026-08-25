import mpmath as mp
mp.mp.dps = 60
def L_of(s):
    w = mp.log(s)
    return mp.findroot(lambda L: L*(mp.pi*mp.e**L + mp.mpf(3)/4) - s,
                       w - mp.log(w) - mp.log(mp.pi))
def K_of(s,L): return s*(1/L + 1/L**2) - mp.mpf(3)/4
def A_main(s):
    L=L_of(s); K=K_of(s,L)
    return mp.sqrt(2*mp.pi/K)*mp.exp(s*mp.log(L)+L/4-s/L+mp.mpf(3)/4)
def h_s(s,u): return s*mp.log(u)+u/4-mp.pi*mp.e**u
def nodes(s):
    L=mp.re(L_of(s)); K=abs(K_of(s,L_of(s))); w=12/mp.sqrt(K)
    p={mp.mpf(0)}
    for c in range(-8,9):
        q=L+c*w/8
        if q>0: p.add(q)
    p |= {L+4*w, L+20*w, L+60}
    return sorted(p)
print("  |s|      arg s     Im L_s      |arg K|    contour relerr   |E1|*|K|")
for mod in (3200, 51200):
    for arg in (mp.mpf(1)/200, mp.mpf(1)/400):
        s = mod*mp.exp(1j*arg)
        L=L_of(s); K=K_of(s,L); b=mp.im(L)
        nd=nodes(s)
        ray = mp.quad(lambda u: mp.exp(h_s(s,u)), nd)
        endpt = (mp.quad(lambda x: mp.exp(h_s(s,x)), [0,1])
                 + 1j*mp.quad(lambda y: mp.exp(h_s(s,1+1j*y)), [0,b]))
        nd1=[x for x in nd if x>=1]
        shifted = endpt + mp.quad(lambda x: mp.exp(h_s(s,x+1j*b)), [1]+nd1)
        E1 = ray/A_main(s)-1
        print(f"  {mod:7d}  {float(arg):.5f}  {float(b):+.7f}  {float(abs(mp.arg(K))):.7f}"
              f"   {float(abs(ray/shifted-1)):.2e}      {float(abs(E1*K)):.4f}")
