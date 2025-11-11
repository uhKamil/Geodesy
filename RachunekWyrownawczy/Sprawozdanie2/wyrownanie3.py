import numpy as np
import scipy.stats as stats

# Marta Sz. - 127306
# Marta W. - 127330
# Tosia - 127337
# Karolina - 127323
# Michał - 127332
# Ja
# Patryk - 127347
# Bartek - 127363

id = "127363"
nr = int(id[-2:])

# Zadanie 3
Ha, Hb, Hc = 100.001 + nr, 102.002 + nr, 102.001 + nr
d1, d2, d3, d4, d5, d6, d7 = 1, 3.004, -.995, -1.012, 2, -.005, -1.996
# print(Ha, Hb, Hc)

# Liczba stanowisk
n1, n2, n3, n4, n5, n6, n7 = 8, 7, 9, 10, 6, 12, 16

# Równania obserwacyjne
Lm_1 = d1
Lm_2 = d2
Lm_3 = d3
Lm_4 = d4
Lm_5 = d5
Lm_6 = d6
Lm_7 = d7
Lm_8 = Ha
Lm_9 = Hb
Lm_10 = Hc

# Macierz L
L = np.array([[Lm_1], [Lm_2], [Lm_3], [Lm_4], [Lm_5], [Lm_6],
              [Lm_7], [Lm_8], [Lm_9], [Lm_10]])
print(f"L={L}")

# Wagi obserwacji
p1, p2, p3, p4, p5 = np.sqrt(n1), np.sqrt(n2), np.sqrt(n3), np.sqrt(n4), np.sqrt(n5)
p6, p7, p8, p9, p10 = np.sqrt(n6), np.sqrt(n7), 1, 3, 2

P = np.diag(
    [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]) * 10 ** -2 * 10 ** -6  # ^-2 żeby były wagi w mm^-2, ^-6 żeby z mm^-2 zrobić m^-2
print(f"P={P} [m^-2]")

# Macierz przekształcenia liniowego
A = np.array([[0, 1, -1, 0, 0],
              [1, 0, -1, 0, 0],
              [-1, 0, 0, 1, 0],
              [-1, 0, 0, 0, 1],
              [1, -1, 0, 0, 0],
              [0, 0, 0, 1, -1],
              [0, 0, 1, -1, 0],
              [0, 0, 1, 0, 0],
              [0, 0, 0, 1, 0],
              [0, 0, 0, 0, 1]])
print(f"A={A}")

def wyrownanie_mnk(A, L, P):
    A_T = np.transpose(A)
    # Macierz X
    y = A_T @ P
    print(f"A^T*P={y} [m^-2]")
    z = y @ A
    print(f"A^T*P*A={z} [m^-2]")
    c = Qx = np.linalg.inv(z)
    print(f"(A^T*P*A)**(-1)={c} [m^2]")
    q = y @ L
    print(f"A^T*P*L={q} [m^-1]")
    x = c @ q
    print(f"x={x} [m]")

    # Poprawki
    v = A @ x - L
    print(f"v={v} [m]")

    # Kontrola
    kontrola = y @ v
    print(f"A^T*P*v={kontrola} [m^-1]")

    # Wektor obserwacji wyrównanych
    L_daszek = L + v
    print(f"L_daszek={L_daszek} [m]")

    # Błąd średni
    v_T = np.transpose(v)
    v_TPv = v_T @ P @ v
    print(f"v^T*P*v={v_TPv} [-]")
    nk = len(L) - len(x)
    print(f"n-k={len(L)}-{len(x)}={nk}")
    m0 = np.sqrt(v_TPv / nk)
    print(f"m0={m0}")

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

    C = [abs(v[i] / m_v[i]) for i in range(len(v))]
    print(f"Test 3. {C}")


wyrownanie_mnk(A, L, P)
