import numpy as np
from wyrownanie import wyrownanie_mnk, deg_min_sec

# Podane w treści zadania
k102 = np.radians(13 / 3600)
k103 = np.radians(104 + 16 / 60 + 40 / 3600)
k104 = np.radians(142 + 52 / 60 + 31 / 3600)
alfa3 = np.radians(59 + 15 / 60 + 48 / 3600)
alfa5 = np.radians(38 + 53 / 60 + 28 / 3600)
alfa6 = np.radians(36 + 49 / 60 + 38 / 3600)
d3, d4, d5, d6, d7 = 1752.934, 1520.981, 2459.062, 1593.141, 1103.932
x101, y101, x104, y104 = 1000, 2000, 1000, 3752.9

# Wcięcie liniowe 101-104, punkt wyznaczany 103
L = np.arccos((d3 ** 2 + d4 ** 2 - d7 ** 2) / (2 * d3 * d4))
P = np.arccos((d3 ** 2 + d7 ** 2 - d4 ** 2) / (2 * d3 * d7))

A_101_104 = np.arctan2(y104 - y101, x104 - x101)
A_101_103, A_104_103 = A_101_104 - L, A_101_104 + np.pi + P
x_103_L, y_103_L = x101 + d4 * np.cos(A_101_103), y101 + d4 * np.sin(A_101_103)
x_103_P, y_103_P = x104 + d7 * np.cos(A_104_103), y104 + d7 * np.sin(A_104_103)
x103, y103 = np.mean([x_103_L, x_103_P]), np.mean([y_103_L, y_103_P])

# Wcięcie liniowe 101-103, punkt wyznaczany 102
A_101_103 = np.arctan2(y103 - y101, x103 - x101)
L = np.arccos((d4 ** 2 + d6 ** 2 - d5 ** 2) / (2 * d4 * d6))
P = np.arccos((d4 ** 2 + d5 ** 2 - d6 ** 2) / (2 * d4 * d5))
A_101_102, A_103_102 = A_101_103 - L, A_101_103 + np.pi + P
x_102_L, y_102_L = x101 + d6 * np.cos(A_101_102), y101 + d6 * np.sin(A_101_102)
x_102_P, y_102_P = x103 + d5 * np.cos(A_103_102), y103 + d5 * np.sin(A_103_102)
x102, y102 = np.mean([x_102_L, x_102_P]), np.mean([y_102_L, y_102_P])
A_101_102 = np.arctan2(y102 - y101, x102 - x101)

# Przybliżone kierunki
A_zero_102 = A_101_102 - k102
A_zero_103 = A_101_103 - k103
A_zero_104 = A_101_104 - k104
A_zero = np.mean([A_zero_102, A_zero_103, A_zero_104])

k0102 = A_101_102 - A_zero
k0103 = A_101_103 - A_zero
k0104 = A_101_104 - A_zero

# Przybliżone przyrosty
deltax03, deltay03 = x104 - x101, y104 - y101
d03 = np.sqrt(deltax03 ** 2 + deltay03 ** 2)  # d101-104
deltax04, deltay04 = x103 - x101, y103 - y101
d04 = np.sqrt(deltax04 ** 2 + deltay04 ** 2) # d101-103
deltax05, deltay05 = x103 - x102, y103 - y102
d05 = np.sqrt(deltax05 ** 2 + deltay05 ** 2) # d102-103
deltax06, deltay06 = x101 - x102, y101 - y102
d06 = np.sqrt(deltax06 ** 2 + deltay06 ** 2) # d102-101
deltax07, deltay07 = x104 - x103, y104 - y103
d07 = np.sqrt(deltax07 ** 2 + deltay07 ** 2)  # d104-103

# Przybliżone kąty
alfa03 = np.arccos((d3 ** 2 + d7 ** 2 - d4 ** 2) / (2 * d3 * d7))
alfa05 = np.arccos((d4 ** 2 + d5 ** 2 - d6 ** 2) / (2 * d4 * d5))
alfa06 = np.arccos((d5 ** 2 + d6 ** 2 - d4 ** 2) / (2 * d5 * d6))

# Wyrównanie
# Macierz A - dx102, dy102, dx103, dy103, dz
A = np.array([[0, 0, deltax04 / d04, deltay04 / d04, 0], # v_d4
              [-deltax05 / d05, -deltay05 / d05, deltax05 / d05, deltay05 / d05, 0], # v_d5
              [-deltax06 / d06, -deltay06 / d06, 0, 0, 0], # v_d6
              [0, 0, -deltax07 / d07, -deltay07 / d07, 0], # v_d7
              [0, 0, -deltay07 / d07 ** 2, deltax07 / d07 ** 2, 0], # v_alfa3
              [-deltay05 / d05 ** 2, deltax05 / d05 ** 2, deltay05 / d05 ** 2 - deltay04 / d04 ** 2,
               -deltax05 / d05 ** 2 - (-deltax04 / d04 ** 2), 0], # v_alfa5
              [deltay06 / d06 ** 2 - deltay05 / d05 ** 2, -deltax06 / d06 ** 2 - (-deltax05 / d05 ** 2),
               -deltay05 / d05 ** 2, deltax05 / d05 ** 2, 0], # v_alfa6
              [-deltay06 / d06 ** 2, deltax06 / d06 ** 2, 0, 0, -1], # v_k102
              [0, 0, -deltay04 / d04 ** 2, deltax04 / d04 ** 2, -1], # v_k103
              [0, 0, 0, 0, -1]]) # v_k104

L = np.array([[d4 - d04],
              [d5 - d05],
              [d6 - d06],
              [d7 - d07],
              [alfa3 - alfa03],
              [alfa5 - alfa05],
              [alfa6 - alfa06],
              [k102 - k0102],
              [k103 - k0103],
              [k104 - k0104]])

# Macierz wag
m1 = 0.005 + 0.005 * np.sqrt(d5 / 1000)
m2 = 0.005 + 0.005 * np.sqrt(d4 / 1000)
m3 = 0.005 + 0.005 * np.sqrt(d6 / 1000)
m4 = 0.005 + 0.005 * np.sqrt(d7 / 1000)
m5 = m6 = m7 = np.radians(7 / 3600)
m8 = m9 = m10 = np.radians(5 / 3600)

p1, p2, p3, p4, p5 = m1 ** -2, m2 ** -2, m3 ** -2, m4 ** -2, m5 ** -2
p6, p7, p8, p9, p10 = m6 ** -2, m7 ** -2, m8 ** -2, m9 ** -2, m10 ** -2

P = np.diag([p1, p2, p3, p4, p5, p6, p7, p8, p9, p10])
print(f"A = {A}", f"L = {L}", f"P = {P}", sep="\n")

wyrownanie_mnk(A, L, P)
