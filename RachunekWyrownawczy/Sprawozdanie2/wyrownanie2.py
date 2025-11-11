import numpy as np
import scipy.stats as stats

id = "127347"
nr = int(id[4:6])

# Zadanie 2
Ha, Hb, Hc = 100.001 + nr, 102.002 + nr, 102.001 + nr
delta1, delta2, delta3, delta4, delta5 = 1, 3.004, -.995, -1.012, 2
# print(Ha, Hb, Hc)

# Wartości długości ciągów są wyrażone w km
L1, L2, L3, L4, L5 = 2, 3 + nr * 0.01, 1, 2 + nr * 0.01, 1 + nr * 0.01
# print(L1, L2, L3, L4, L5)

# Równania obserwacyjne
Lm_1 = Ha + delta1
Lm_2 = Ha + delta2
Lm_3 = -Hb + delta3
Lm_4 = -Hc + delta4
Lm_5 = delta5

# Macierz L
L = np.array([[Lm_1],
              [Lm_2],
              [Lm_3],
              [Lm_4],
              [Lm_5]])
print(f"L={L}")

# Wagi obserwacji
p1, p2, p3, p4, p5 = 1 / L1, 1 / L2, 1 / L3, 1 / L4, 1 / L5

P = np.array([[p1, 0, 0, 0, 0],
              [0, p2, 0, 0, 0],
              [0, 0, p3, 0, 0],
              [0, 0, 0, p4, 0],
              [0, 0, 0, 0, p5]])
# print(P)
# Macierz A
A = np.array([[0, 1],
              [1, 0],
              [-1, 0],
              [-1, 0],
              [1, -1]])
A_T = np.transpose(A)

# Macierz X
y = A_T @ P
print(f"A^T*P={y}")
z = y @ A
print(f"A^T*P*A={z}")
c = Qx = np.linalg.inv(z)
print(f"(A^T*P*A)**(-1)={c}")
q = y @ L
print(f"A^T*P*L={q}")
x = c @ q
print(f"x={x}")

# Poprawki
v = A @ x - L
print(f"v={v} [m] =\n{v*1000} [mm]")

# Kontrola
kontrola = y @ v
print(f"A^T*P*v={kontrola}")

# Wektor obserwacji wyrównanych
L_daszek = L + v
print(f"L_daszek={L_daszek}")

# m0
v_T = np.transpose(v)
v_TPv = v_T @ P @ v
print(f"v^T*P*v={v_TPv} [mm^2]")
nk = len(L) - len(x)
print(f"n-k={len(L)}-{len(x)}={nk}")
m0 = np.sqrt(v_TPv / nk)
print(f"m0={m0} [sqrt(mm)]")
m_km = m0 * np.sqrt(1e6)
print(f"m_km={m_km} [mm/km]")

# Macierz kowariancji
print(f"Qx={Qx}")
Cx = m0 ** 2 * Qx
print(f"Cx={Cx}")
m_Cx = [np.sqrt(Cx[i][i]) for i in range(len(Cx))]
print(f"Błędy niewiadomych pośredniczących: {m_Cx}")
C_L_daszek = A @ Cx @ A_T
print(f"C_L_daszek={C_L_daszek}")
m_CL_daszek = [np.sqrt(C_L_daszek[i][i]) for i in range(len(C_L_daszek))]
print(f"Błędy obserwacji wyrównanych: {m_CL_daszek}")
C_L = m0 ** 2 * np.linalg.inv(P)
print(f"C_L={C_L}")
Cv = C_L - C_L_daszek
print(f"Cv={Cv}")
m_v = [np.sqrt(Cv[i][i]) for i in range(len(Cv))]
print(f"Błędy poprawek: {m_v}")

# Testy statystyczne
c1 = m0 ** 2 * nk
c2 = stats.chi2.ppf(0.95, nk)
if c1 <= c2:
    print(f"{c1} <= {c2}. Brak podstaw do odrzucenia hipotezy m0 ≊ σ0, czyli wyrównanie prawdopodobnie jest poprawne")
else:
    print(f"{c1} > {c2}. Odrzuca się hipotezę m0 ≊ σ0, czyli wyrównanie nie jest poprawne")

C = [abs(v[i]/m_v[i]) for i in range(len(v))]
print(f"Test 3. {C}")