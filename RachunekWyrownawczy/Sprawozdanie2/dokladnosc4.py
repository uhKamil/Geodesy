import numpy as np

# Liczba stanowisk
n = [8, 7, 9, 10, 6, 12, 16]
n1, n2, n3, n4, n5, n6, n7 = n

# Wagi obserwacji
# mi = 1 # Założono, że błędy wysokości wyznaczanych punktów nie mogą być większe niż 1 mm
# p1, p2, p3, p4, p5, p6, p7 = (mi*np.sqrt(n1), mi*np.sqrt(n2), mi*np.sqrt(n3), mi*np.sqrt(n4), mi*np.sqrt(n5),
#                               mi*np.sqrt(n6), mi*np.sqrt(n7))
#
# P = np.diag([p1, p2, p3, p4, p5, p6, p7]) * 10 ** -2
# print(f"P={P} [mm^-2]")
#
# # Macierz przekształcenia liniowego
# A = np.array([[0, 1],
#               [1, 0],
#               [-1, 0],
#               [-1, 0],
#               [1, -1],
#               [0, 0],
#               [0, 0]])
# print(f"A={A}")
#
# Qx = np.linalg.inv(A.T @ P @ A)
# print(f"Qx={Qx} [mm^2]")
# Cx = mi ** 2 * Qx
# print(f"Cx={Cx}")

# Wagi obserwacji
mi = 1 # Założono, że błędy wysokości wyznaczanych punktów nie mogą być większe niż 1 mm
P = np.diag([n1, n2, n3, n4, n5, n6, n7]) * 10 ** -1
print(f"P={P} [-]")

# Macierz przekształcenia liniowego
A = np.array([[0, 1],
              [1, 0],
              [-1, 0],
              [-1, 0],
              [1, -1],
              [0, 0],
              [0, 0]])
print(f"A={A}")

Qx = np.linalg.inv(A.T @ P @ A)
print(f"Qx={Qx} [-]")
Cx = mi ** 2 * Qx
print(f"Cx={Cx} [mm^2]")

m0 = [np.sqrt(Cx[i][i]) for i in range(len(Cx))]
print(f"Otrzymane mi do sprawdzenia: {m0}")
mh = [[m0[i]*np.sqrt(n[j])] for i in range(len(m0)) for j in range(len(n))]
print(f"Otrzymane dopuszczalne błędy wysokości: {mh}")
for i in range(len(n)):
    print(f"{mh[i]} <= m_deltah_{i+1} <= {mh[i+len(n)]}")
