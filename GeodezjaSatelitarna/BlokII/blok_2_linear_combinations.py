import numpy as np
import matplotlib.pyplot as plt

# Struktury danych
C1 = []
L1C = []
D1 = []
S1 = []
C2 = []
L2C = []
D2 = []
S2 = []

# STAŁE #
C = 299792458  # prędkość światła [m/s]
f1 = 1575.42e6
f2 = 1227.6e6

# Proste parsowanie
with open("BLOK_IIb.txt", 'r') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip().split()

        try:
            values = [float(val) for val in line[1:]]
        except ValueError:
            continue

        C1.append(values[0])
        L1C.append(values[1])
        D1.append(values[2])
        S1.append(values[3])
        C2.append(values[4])
        L2C.append(values[5])
        D2.append(values[6])
        S2.append(values[7])

C1 = np.array(C1)
L1C = np.array(L1C)
D1 = np.array(D1)
S1 = np.array(S1)
C2 = np.array(C2)
L2C = np.array(L2C)
D2 = np.array(D2)
S2 = np.array(S2)

print(C1, L1C, D1, S1, C2, L2C, D2, S2, sep='\n')

# Przeliczenie obserwacji fazowych
L1M = L1C * C / f1
L2M = L2C * C / f2

print(L1M, L2M, sep='\n')

# Kombinacje liniowe obserwacji
C_IF = (f1 ** 2 * C1 - f2 ** 2 * C2) / (f1 ** 2 - f2 ** 2)
L_IF = (f1 ** 2 * L1M - f2 ** 2 * L2M) / (f1 ** 2 - f2 ** 2)
C_GF = C1 - C2
L_GF = L2M - L1M
G1 = (C1 + L1M) / 2
G2 = (C2 + L2M) / 2

print(C_IF, L_IF, C_GF, L_GF, G1, G2, sep='\n')

# Tworzenie wykresów
t = np.array([i for i in range(len(L1C))])
plt.figure(dpi=600)
plt.xlabel('Indeks epoki', fontsize=12)
plt.ylabel('Obserwacja [m]', fontsize=12)
plt.plot(t, C1)
plt.plot(t, C2)
plt.plot(t, L1M)
plt.plot(t, L2M)
plt.plot(t, C_IF)
plt.plot(t, L_IF)
plt.plot(t, G1)
plt.plot(t, G2)
plt.legend(["${C_1}$", "${C_2}$", "${L_1}$", "${L_2}$", "${C_{IF}}$", "${L_{IF}}$", "${G_1}$", "${G_2}$"])
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure(dpi=600)
plt.xlabel('Indeks epoki', fontsize=12)
plt.ylabel('Obserwacja - C1 [m]', fontsize=12)
plt.plot(t, C2-C1)
plt.plot(t, L1M-C1)
plt.plot(t, L2M-C1)
plt.plot(t, C_IF-C1)
plt.plot(t, L_IF-C1)
plt.plot(t, G1-C1)
plt.plot(t, G2-C1)
plt.legend(["${C_2}$", "${L_1}$", "${L_2}$", "${C_{IF}}$", "${L_{IF}}$", "${G_1}$", "${G_2}$"])
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure(dpi=600)
plt.xlabel('Indeks epoki', fontsize=12)
plt.ylabel('Obserwacja geometry-free [m]', fontsize=12)
plt.plot(t, C_GF)
plt.plot(t, L_GF)
plt.legend(["${C_{GF}}$", "${L_{GF}}$"])
plt.grid(True)
plt.tight_layout()
plt.show()