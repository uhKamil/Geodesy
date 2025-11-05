import numpy as np

h1, i1 = 0.011, 1.58
z1, z2 = 93.4780 * np.pi / 200, 93.6724 * np.pi / 200
z1_st, z2_st = 101.9058 * np.pi / 200, 101.0068 * np.pi / 200
d1, d2 = 3.57, 3.58
i2 = 1.57
h23, h32 = np.abs(i1 + d1 / np.tan(z1_st) - 1.5), np.abs(i2 + d2 / np.tan(z2_st) - 1.5)
h2 = h1 - np.mean([h23, h32])
b = np.mean([d1, d2])

c = h1 + i1 - (h2 + i2)
x = (c - b / np.tan(z2)) / (1 / np.tan(z2) - 1 / np.tan(z1))
# x2 = (b / np.tan(z2) - c) / (1 / np.tan(z1) - 1 / np.tan(z2))
print(f"c = {c:.9f} m, x = {x:.8f} m")

delta_h1 = x / np.tan(z1)
delta_h2 = (x + b) / np.tan(z2)
print(f"delta_h1 = {delta_h1:.9f} m, delta_h2 = {delta_h2:.9f} m")

HL1 = h1 + i1 + delta_h1
HL2 = h2 + i2 + delta_h2
print(f"HL1 = {HL1:.8f} m, HL2 = {HL2:.8f} m, HLśr = {np.mean([HL1, HL2]):.3f} m")
