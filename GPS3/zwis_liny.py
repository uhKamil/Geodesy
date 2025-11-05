import numpy as np

h1, i1, h2, i2 = 0.011, 1.58, -0.003, 1.57
z1, z2 = 94.1780 * np.pi / 200, 94.3724 * np.pi / 200
b = np.mean([3.57, 3.58])

c = h1 + i1 - (h2 + i2)
x = (c - b / np.tan(z2)) / (1 / np.tan(z2) - 1 / np.tan(z1))
print(f"c = {c:.9f} m, x = {x:.8f} m")

delta_h1 = x / np.tan(z1)
delta_h2 = (x + b) / np.tan(z2)
print(f"delta_h1 = {delta_h1:.9f} m, delta_h2 = {delta_h2:.9f} m")

HL1 = h1 + i1 + delta_h1
HL2 = h2 + i2 + delta_h2
print(f"HL1 = {HL1:.8f} m, HL2 = {HL2:.8f} m, HLśr = {np.mean([HL1, HL2]):.3f} m")
