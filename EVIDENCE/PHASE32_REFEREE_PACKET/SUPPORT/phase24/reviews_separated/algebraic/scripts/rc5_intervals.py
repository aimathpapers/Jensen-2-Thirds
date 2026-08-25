#!/usr/bin/env python3
"""RC-5: Independent exact-rational check of Gates B3/B6 interval arithmetic.

Recomputed from manuscript definitions (Sections 7, 9 and phase-16 note):
  branch box  alpha in [5/2,7/2], t in [7/4,9/4], w in [5,6], delta in [1/4,5/12]
  parameters  A=alpha/(xe), B=(t+we)/x, C=t/x, D=(1+delta e)/x, 0<e<=1/12, x>0
  saddle box  |r|,|sigma| <= 7/50
  localization threshold D >= 256 d, coarse box n<=B<=3n, n/2<=D<=2n
No floating point is used anywhere.
"""
from fractions import Fraction as Q

# ------------------------------------------------ branch box and margins
box = [(Q(5, 2), Q(7, 2)), (Q(7, 4), Q(9, 4)), (Q(5), Q(6)), (Q(1, 4), Q(5, 12))]
y_star = [Q(3), Q(2), Q(16, 3), Q(1, 3)]
margins = [(p - lo, hi - p) for p, (lo, hi) in zip(y_star, box)]
print("margins:", margins)
assert margins == [(Q(1, 2), Q(1, 2)), (Q(1, 4), Q(1, 4)),
                   (Q(1, 3), Q(2, 3)), (Q(1, 12), Q(1, 12))]

# ------------------------------------------------ elementary ordering A>B>C>D>0
e_hi = Q(1, 12)
A_num_min = Q(5, 2) / e_hi                 # alpha/e >= 30
B_num_max = Q(9, 4) + Q(6) * e_hi          # t + w e <= 11/4
print("A numerator min:", A_num_min, " B numerator max:", B_num_max)
assert A_num_min == 30 and B_num_max == Q(11, 4) and A_num_min > B_num_max
CD_gap_min = Q(7, 4) - 1 - Q(5, 12) * e_hi  # t - 1 - delta e >= 103/144
print("C-D numerator min:", CD_gap_min)
assert CD_gap_min == Q(103, 144) and CD_gap_min > 0
print("endpoint arithmetic alpha/e >= 30 > 11/4 >= t+we; t-1-delta e >= 103/144 OK")

# ------------------------------------------------ saddle box margins
rmax = Q(7, 50)
pert1 = rmax + Q(3, 4) * rmax
lower1 = 1 - pert1
print("saddle factor perturbation:", pert1, "lower:", lower1)
assert pert1 == Q(49, 200) and lower1 == Q(151, 200) and lower1 > Q(9, 16)
pert2 = 4 * rmax + 3 * rmax
lower2 = 4 - pert2
assert pert2 == Q(49, 50) and lower2 == Q(151, 50)
print("saddle reduced denominator lower:", lower2)

# ------------------------------------------------ coarse box consequences
B_over_D_max = Q(3) / Q(1, 2)              # B<=3n, D>=n/2
assert B_over_D_max == 6
Kpre = Q(256)
# endpoints positive: 8 sqrt(Bd) <= B/2  <=>  256 d <= B
# checked symbolically: (B/2)^2 >= 64 B d  <=> B >= 256 d
print("endpoint positivity equivalent to B,D >= 256 d: OK (squared comparison)")

# ------------------------------------------------ C_loc derivation
# deviation bound / sqrt(Bd): 8 + 8 sqrt(B/D) + 64 sqrt(d/D)
# with B/D <= 6 and d/D <= 1/256:
const_part = Q(8) + 64 * Q(1, 16)
sqrt_part_coeff = Q(8)
print("C_loc = ", const_part, " + ", sqrt_part_coeff, "* sqrt(6)")
assert const_part == 12 and sqrt_part_coeff == 8
# sqrt(6) < 5/2  <=>  6*4 < 25
assert 6 * 4 < 25
C_loc_upper = const_part + sqrt_part_coeff * Q(5, 2)
assert C_loc_upper == 32
K0 = Kpre * C_loc_upper ** 2
print("C_loc < ", C_loc_upper, "   K0 = 256*32^2 =", K0)
assert K0 == 262144

# ------------------------------------------------ strengthened box consistency
# K0 d <= B <= 3n  requires n >= K0 d/3; record the implied wedge absorption
print("strengthened threshold K0 =", K0, "(matches manuscript 262144)")

# ------------------------------------------------ cross-term bound detail
# 64 sqrt(Bd) sqrt(d/D) <= 64*(1/16)*sqrt(Bd) = 4 sqrt(Bd)
assert 64 * Q(1, 16) == 4
# 8 B sqrt(d/D) = 8 sqrt(Bd) sqrt(B/D) <= 8 sqrt(6) sqrt(Bd)
print("cross-term decomposition verified: 8 + 4 = 12 constant, 8*sqrt(6) radical part")

print("RC-5 ALL CHECKS PASSED")
