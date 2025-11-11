import numpy as np
import scipy.stats as stats


def wyrownanie_mnk(A, L, P):
    # Macierz X
    y = A.T @ P
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
    print(f"v={v}")

    # Kontrola
    kontrola = y @ v
    print(f"A^T*P*v={kontrola}")

    # Wektor obserwacji wyrównanych
    L_daszek = L + v
    print(f"L_daszek={L_daszek}")

    # Błąd średni
    v_TPv = v.T @ P @ v
    print(f"v^T*P*v={v_TPv}")
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
    C_L_daszek = A @ Cx @ A.T
    print(f"C_L_daszek={C_L_daszek}")
    m_CL_daszek = [np.sqrt(C_L_daszek[i][i]) for i in range(len(C_L_daszek))]
    print(f"Błędy obserwacji wyrównanych: {m_CL_daszek}")
    C_L = m0 ** 2 * np.linalg.inv(P)
    print(f"C_L={C_L}")
    m_CL = [np.sqrt(C_L[i][i]) for i in range(len(C_L))]
    print(f"Błędy obserwacji: {m_CL}")
    Cv = C_L - C_L_daszek
    print(f"Cv={Cv}")
    m_v = [np.sqrt(Cv[i][i]) for i in range(len(Cv))]
    print(f"Błędy poprawek: {m_v}")

    # Testy statystyczne
    c1 = m0 ** 2 * nk
    c2 = stats.chi2.ppf(0.95, nk)
    if c1 <= c2:
        print(
            f"{c1} <= {c2}. Brak podstaw do odrzucenia hipotezy m0 ≊ σ0, czyli wyrównanie prawdopodobnie jest poprawne")
    else:
        print(f"{c1} > {c2}. Odrzuca się hipotezę m0 ≊ σ0, czyli wyrównanie nie jest poprawne")

    C = [abs(v[i] / m_v[i]) for i in range(len(v))]
    print(f"Test 3. {C}")


def ocena_dokladnosci(A, L, P):
    Qx = np.linalg.inv(A.T @ P @ A)
    print(f"Qx = Cx = {Qx}")
    return Qx


def deg_min_sec(angle):
    """:param angle: wartość w stopniach"""
    d = int(angle)
    m = int((angle - angle // 1) * 60)
    s = ((angle - angle // 1) * 60 - (angle - angle // 1) * 60 // 1) * 60
    return d, m, s
