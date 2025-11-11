import numpy as np
from wyrownanie import wyrownanie_mnk, deg_min_sec

# Wartości przybliżone potrzebne do przeprowadzenia wyrównania
deltax04, deltay04 = 948.857, 1188.719
d04 = np.sqrt(deltax04 ** 2 + deltay04 ** 2)  # d101-103
deltax05, deltay05 = -12.766, 2458.908
d05 = np.sqrt(deltax05 ** 2 + deltay05 ** 2)  # d102-103; było wpisane 2455.202, wychodzi inaczej z delt (2455.202 zdecydowanie musi być złe)
deltax06, deltay06 = 961.623, -1270.189
d06 = np.sqrt(deltax06 ** 2 + deltay06 ** 2)  # d101-102
deltax07, deltay07 = -948.857, 564.181
d07 = np.sqrt(deltax07 ** 2 + deltay07 ** 2)  # d104-103
deltax03, deltay03 = 0, 1752.90
d03 = np.sqrt(deltax03 ** 2 + deltay03 ** 2)  # d101-104
k0102, k0103, k0104 = 6.289817558 * 10 ** (-5), 1.819991011, 2.493644469
alfa03, alfa05, alfa06 = 1.03436624, 0.6787777447, 0.6427558943

print(deg_min_sec(alfa03 * 180 / np.pi), deg_min_sec(alfa05 * 180 / np.pi), deg_min_sec(alfa06 * 180 / np.pi))

# Podane w treści zadania
k102 = np.radians(13 / 3600)
k103 = np.radians(104 + 16 / 60 + 40 / 3600)
k104 = np.radians(142 + 52 / 60 + 31 / 3600)
alfa3 = np.radians(59 + 15 / 60 + 48 / 3600)
alfa5 = np.radians(38 + 53 / 60 + 28 / 3600)
alfa6 = np.radians(36 + 49 / 60 + 38 / 3600)
d3, d4, d5, d6, d7 = 1752.934, 1520.981, 2459.062, 1593.141, 1103.932

A101_104 = np.arctan2(3752.9 - 2000, 1000 - 1000) * 180 / np.pi
print(f"A101_104 = {A101_104}° = {deg_min_sec(A101_104)[0]}° {deg_min_sec(A101_104)[1]}' {deg_min_sec(A101_104)[2]}''")
A_zero = A101_104 - (142 + 52/60 + 31/3600) + 360
print(f"A_zero = {A_zero}° = {deg_min_sec(A_zero)[0]}° {deg_min_sec(A_zero)[1]}' {deg_min_sec(A_zero)[2]}''")

# Wyrównanie
A = np.array([[0, 0, deltax04 / d04, deltay04 / d04, 0],
              [-deltax05 / d05, -deltay05 / d05, deltax05 / d05, deltay05 / d05, 0],
              [-deltax06 / d06, -deltay06 / d06, 0, 0, 0],
              [0, 0, -deltax07 / d07, -deltay07 / d07, 0],
              [0, 0, -deltax07 / d07, -deltay07 / d07, 0],
              [-deltay05 / d05 ** 2, deltax05 / d05 ** 2, (deltay05 / d05 ** 2) - (deltay04 / d04 ** 2),
               -((deltax05 / d05 ** 2) - (deltax04 / d04 ** 2)), 0],
              [(deltay06 / d06 ** 2) - (deltay05 / d05 ** 2), -((deltax06 / d06 ** 2) - (deltax05 / d05 ** 2)),
               deltay05 / d05 ** 2, -deltax05 / d05 ** 2, 0],
              [0, 0, 0, 0, -1],
              [0, 0, -deltay05 / d05 ** 2, deltax05 / d05 ** 2, -1],
              [-deltay06 / d06 ** 2, deltax06 / d06 ** 2, 0, 0, -1]])

L = np.array([[d4 - d04],
              [d5 - d05],
              [d6 - d06],
              [d7 - d07],
              [alfa3 - alfa03],
              [alfa5 - alfa05],
              [alfa6 - alfa06],
              [k104 - k0104],
              [k103 - k0103],
              [k102 - k0102]])
print(f"L = {L}")

# Macierz wag
m1 = 0.012604905
m2 = 0.01729531
m3 = 0.012965705
m4 = 0.01055196
m5 = m6 = m7 = 0.000033937
m8 = m9 = m10 = 0.000024241

p1, p2, p3, p4, p5 = m1 ** -2, m2 ** -2, m3 ** -2, m4 ** -2, m5 ** -2
p6, p7, p8, p9, p10 = m6 ** -2, m7 ** -2, m8 ** -2, m9 ** -2, m10 ** -2

P = np.diag([p1, p2, p3, p4, p5, p6, p7, p8, p9, p10])
print(f"A = {A}", f"P = {P}", sep="\n")

wyrownanie_mnk(A, L, P)
