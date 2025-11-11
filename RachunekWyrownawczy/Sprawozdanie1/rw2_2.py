import math
import numpy as np
import sympy as sp


# Do programu
indeks = "127337"
id_2  = int(indeks[4:6])
print(f"Nr = {id_2}g")


# Dane do zadania
Xa=100
m_xa=0.02
Ya=200
m_ya=0.01
a=(30+id_2)*(np.pi/200)
m_a=0.0030*(np.pi/200)
A_ab=(100+(3*id_2))*(np.pi/200)
m_A=0.0020*(np.pi/200)
d=200
m_d=0.02

print(f"A_ab-a = {100 + 2*id_2 - 30}g")

# Podpunkt 1
Xp=Xa+d*math.cos(A_ab-a)
Yp=Ya+d*math.sin(A_ab-a)
print(f"Xp = {Xp:.4f}")
print(f"Yp = {Yp:.4f}")

# Macierz wariancyjno-kowariancyjna
Cx = np.array([
    [m_xa ** 2, 0, 0, 0, 0],
    [0, m_ya ** 2, 0, 0, 0],
    [0, 0, m_a ** 2, 0, 0],
    [0, 0, 0, m_d ** 2, 0],
    [0, 0, 0, 0, m_A ** 2]
])
print("Macierz wariancyjno-kowariancyjna:")
print(Cx)

zmienne = ["Xa", "Ya", "a", "d", "A_ab"]
Xa_sym, Ya_sym, a_sym, d_sym, A_ab_sym = sp.symbols('Xa Ya a d A_ab')
# Wyrażenia symboliczne na Xp i Yp
Xp_sym = Xa_sym + d_sym * sp.cos(A_ab_sym - a_sym)
Yp_sym = Ya_sym + d_sym * sp.sin(A_ab_sym - a_sym)


# Macierz pochodnych A (Jakobian)
A = np.array([[0,0,0,0,0],
             [0,0,0,0,0]], dtype=np.float64)  # 2 funkcje (Xp, Yp) po 5 zmiennych (Xa, Ya, a, d, A_ab)

# Obliczanie pochodnych cząstkowych
for i, zmienna in enumerate(zmienne):
    # Pochodna Xp po zmiennej
    pochodna_Xp = sp.diff(Xp_sym, eval(f"{zmienna}_sym"))
    wartosc_Xp = pochodna_Xp.subs({
        Xa_sym: float(Xa),
        Ya_sym: float(Ya),
        a_sym: float(a),
        A_ab_sym: float(A_ab),
        d_sym: float(d)
    }).evalf(16)
    A[0, i] = float(wartosc_Xp)

    # Pochodna Yp po zmiennej
    pochodna_Yp = sp.diff(Yp_sym, eval(f"{zmienna}_sym"))
    wartosc_Yp = pochodna_Yp.subs({
        Xa_sym: float(Xa),
        Ya_sym: float(Ya),
        a_sym: float(a),
        A_ab_sym: float(A_ab),
        d_sym: float(d)
    }).evalf(16)
    A[1, i] = float(wartosc_Yp)

# Ustawienia wyświetlania
np.set_printoptions(precision=10, suppress=True, floatmode='maxprec')
print("Macierz pochodnych A:")
print(A)

# Mnożenie macierzy
# Macierz N=A*Cx
N=np.dot(A,Cx)
print("Macierz pochodnych mnożenia A*Cx:")
print(N)
# Macierz M=N*A.T=Cy
M=np.dot(N,np.transpose(A))
print("Macierz pochodnych mnożenia A*Cx*A_T:")
print(M)

# Podpunkt 3
mx_2 = M[0,0]
my_2 = M[1,1]
mxy = M[0,1]
# Korelacja punktu P
r_xpyp = float( M[0,1] / (math.sqrt(M[0,0])*math.sqrt(M[0,0])) )
print("Korelacja wynosi")
print(f"{r_xpyp:.15f}")

# Podpunkt 4
Azymut = 0.5*math.atan(2 * (M[0,1]) / (M[0,0]-M[1,1]))
if Azymut < 0:
    Azymut += np.pi
if Azymut+np.pi/2 > np.pi:
    Azymut_90 = Azymut - np.pi/2
else:
    Azymut_90 = Azymut + np.pi/2

blad_1 = math.sqrt(mx_2*math.cos(Azymut)**2 + mxy*math.sin(2*Azymut) + my_2 * math.sin(Azymut) ** 2)
blad_2 = math.sqrt(mx_2*math.cos(Azymut_90)**2 + mxy*math.sin(2*Azymut_90) + my_2 * math.sin(Azymut_90) ** 2)

if blad_1 > blad_2:
    Aa, Bb, AzMax = blad_1, blad_2, Azymut
else:
    Aa, Bb, AzMax = blad_2, blad_1, Azymut_90

print("Wartość maksymalna wynosi")
print(Aa)
print("Wartość minimalna wynosi")
print(Bb)
print("Azymut wartości maksymalnej wynosi")
print(f"{AzMax*200/np.pi}g")