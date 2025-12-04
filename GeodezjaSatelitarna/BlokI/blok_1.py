import numpy as np
import matplotlib.pyplot as plt

def wspolrzedneSatelity(t0c, t, nav, sp3):
    Xsp3, Ysp3, Zsp3, Tsp3 = sp3

    # STAŁE #
    omega_e = 0.000072921151467 # Prędkość obrotowa Ziemi wg. WGS84 [rad/s]
    mi = 3.986005e14 # Potencjał ziemski wg. WGS84 [G∙M]
    gps_pi = 3.1415926535898 # [rad]
    c = 299792458 # Prędkość światła [m/s]

    # ZMIENNE #
    a0 = nav[0, 1] # poprawka fazowa zegara [s]
    a1 = nav[0, 2] # poprawka częstotliwościowa zegara [s/s]
    a2 = nav[0, 3] # przyspieszenie poprawki zegara [s/s^2]
    IODE = nav[1, 0] # identyfikator danych efemerydalnych
    C_rs = nav[1, 1] # poprawka odległości geocentrycznej [m]
    delta_n = nav[1, 2] # średnia różnica ruchu [rad/s]
    M0 = nav[1, 3] # średnia anomalia na epokę odniesienia [rad]
    C_uc = nav[2, 0] # poprawka dla argumentu perygeum [rad]
    e = nav[2, 1] # ekscentr (mimośród elipsy orbity)
    C_us = nav[2, 2] # druga poprawka dla argumentu perygeum [rad]
    sqrt_a = nav[2, 3]
    t0e = nav[3, 0] # czas efemerydalny czasu GPS [s]
    C_ic = nav[3, 1] # poprawka inklinacji [rad]
    Omega0 = nav[3, 2] # kąt węzła wstępującego na epokę zegarową [rad]
    C_is = nav[3, 3] # druga poprawka inklinacji [rad]
    i0 = nav[4, 0] # inklinacja na epokę zegarową [rad]
    C_rc = nav[4, 1] # druga poprawka współczynnika odległości geocentrycznej
    omega = nav[4, 2] # argument perygeum [rad]
    Omega_dot = nav[4, 3] # prędkość zmiany rektascensji [rad/s]
    IDOT = nav[5, 0] # prędkość zmiany kąta nachylenia orbity [rad/s]
    KOD_L2 = nav[5, 1] # kody na kanale L2
    GPS_week = nav[5, 2] # numer tygodnia czasu GPS dla t0e
    L2_P = nav[5, 3] # flaga kodu precyzyjnego dla kanału L2
    SV = nav[6, 0] # przybliżona dokładność satelity [m]
    SV_Health = nav[6, 1] # kod zdrowia satelity
    TGD = nav[6, 2] # opóźnienie grupowe [s]
    IDOC = nav[6, 3] # identyfikator danych efemerydalnych zegara
    t_tc = nav[7, 0] # ekopa transmisji depeszy [s]

    # WZORY #
    # Poprawka zegara satelity (czas GPSt do czasu UTC)
    delta_t = a0 + a1*(t-t0c) + a2*(t-t0c)**2
    # Epoka odniesienia efemeryd
    tk = t - t0e
    # Duża półoś orbity satelity
    a = sqrt_a ** 2
    # Ruch średni satelity
    n0 = (mi / a ** 3) ** 0.5
    # Poprawiony ruch średni
    n = n0 + delta_n
    # Anomalia średnia w epoce tk; Mk w przedziale〈0,2π〉
    Mk = M0 + n * tk; Mk %= (2 * np.pi)

    # Anomalia mimośrodowej Ek
    # Metoda Newtona-Raphsona (zbieżność nie liniowa, a kwadratowa)
    Ek = 1
    Ek_ = 1e3
    i = 0
    while (abs(Ek-Ek_) > 10e-14):
        Ek_ = Ek
        # 1. Obliczenie f(Ek) i f'(Ek)
        f_Ek_numerator = Ek - e * np.sin(Ek) - Mk
        f_prime_Ek_denominator = 1 - e * np.cos(Ek)
        # 2. Obliczenie poprawki i nowej wartości
        Ek = Ek - (f_Ek_numerator / f_prime_Ek_denominator)
        i += 1
    # Anomalia prawdziwa
    v = np.atan2(np.sqrt(1 - e**2) * np.sin(Ek), np.cos(Ek) - e)
    # Argument szerokości
    u = omega + v; u %= (2 * np.pi)
    # Poprawka dla argumentu szerokości
    deltau_k = C_us * np.sin(2*u) + C_uc * np.cos(2*u)
    # Poprawka dla promienia wodzącego
    deltar_k = C_rs * np.sin(2*u) + C_rc * np.cos(2*u)
    # Poprawka dla kąta nachylenia orbity
    deltai_k = C_is * np.sin(2*u) + C_ic * np.cos(2*u) + IDOT * tk
    # Poprawiony argument szerokości
    uk = u + deltau_k
    # Poprawiony promień wodzący
    rk = a * (1 - e * np.cos(Ek)) + deltar_k
    # Poprawiona wartość kąta nachylenia orbity
    ik = i0 + deltai_k
    # Poprawiona długość węzła wstępującego orbity w przedziale〈0,2π〉
    Omega_k = Omega0 + (Omega_dot - omega_e) * tk - omega_e * t0e; Omega_k %= (2 * np.pi)
    # Współrzędne satelity w płaszczyźnie orbity
    ksi = rk * np.cos(uk); eta = rk * np.sin(uk)
    # Współrzędne geocentryczne satelity
    X = ksi * np.cos(Omega_k) - eta * np.cos(ik) * np.sin(Omega_k)
    Y = ksi * np.sin(Omega_k) + eta * np.cos(ik) * np.cos(Omega_k)
    Z = eta * np.sin(ik)
    # Iloczyn prędkości anomalii średniej i mimośrodowej
    EM = 1/(1 - e * np.cos(Ek))
    # Prędkość anomalii prawdziwej
    v_dot = ((1+e)/(1-e)) ** 0.5 * (1 / np.cos(Ek/2)**2) * (1 / (1 + np.tan(v/2)**2)) * EM * n
    # Prędkość argumentu szerokości
    u_dot = v_dot + 2 * v_dot * (C_us * np.cos(2*u) - C_uc * np.sin(2*u))
    omega_dot = Omega_dot - omega_e
    # Prędkość zmiany kąta nachylenia orbity
    i_dot = IDOT + 2 * v_dot * (C_is * np.cos(2*u) - C_ic * np.sin(2*u))
    # Prędkość promienia wodzącego
    r_dot = a * e * np.sin(Ek) * EM * n + 2 * v_dot * (C_rs * np.cos(2*u) - C_rc * np.sin(2*u))
    # Prędkość satelity w płaszczyźnie orbity
    ksi_dot = r_dot * np.cos(uk) - rk * np.sin(uk) * u_dot
    eta_dot = r_dot * np.sin(uk) + rk * np.cos(uk) * u_dot
    # Prędkości geocentryczne satelity
    X_dot = np.cos(Omega_k) * ksi_dot - np.cos(ik) * np.sin(Omega_k) * eta_dot - ksi * np.sin(Omega_k) * omega_dot - eta * np.cos(ik) * np.cos(Omega_k) * omega_dot + eta * np.sin(ik) * np.sin(Omega_k) * i_dot
    Y_dot = np.sin(Omega_k) * ksi_dot + np.cos(ik) * np.cos(Omega_k) * eta_dot + ksi * np.cos(Omega_k) * omega_dot - eta * np.cos(ik) * np.sin(Omega_k) * omega_dot - eta * np.sin(ik) * np.cos(Omega_k) * i_dot
    Z_dot = np.sin(ik) * eta_dot + eta * np.cos(ik) * i_dot
    # Poprawka relatywistyczna
    delta_t_rel = -2 * (X * X_dot + Y * Y_dot + Z * Z_dot) / (c ** 2)
    # Poprawka zegara satelity z uwzględnieniem efektu relatywistycznego
    delta_t_prim = delta_t + delta_t_rel
    # Promień orbity
    r = np.sqrt(X**2 + Y**2 + Z**2)
    r_sp3 = np.sqrt(Xsp3**2 + Ysp3**2 + Zsp3**2)
    # Prędkość wypadkowa
    v = np.sqrt(X_dot**2 + Y_dot**2 + Z_dot**2)
    return X, Y, Z, r, v, delta_t_prim


# Dane
"""
G09 2025 03 04 02 00 00
5.870070308447e-04 1.307398633799e-11 0.000000000000e+00 0.000000000000e+00
2.400000000000e+01-1.025000000000e+01 4.909133056525e-09 4.117597310113e-01
-6.388872861862e-07 3.030300256796e-03 5.196779966354e-06 5.153749139786e+03
1.800000000000e+05-8.009374141693e-08-9.203488554469e-01-1.862645149231e-09
9.608171808408e-01 2.788125000000e+02 2.029634976455e+00-8.358919611125e-09
7.536028191537e-11 1.000000000000e+00 2.356000000000e+03 0.000000000000e+00
2.000000000000e+00 0.000000000000e+00 9.313226000000e-10 2.400000000000e+01
1.728000000000e+05 4.000000000000e+00 0.000000000000e+00 0.000000000000e+00
*  2025  3  4  3 15  0.00000000
PG09   6796.098769  25623.646806    837.694977    587.064507  2  5  5  22
toc = 180000.0
t = 184500.0
"""

t0c = 2 * 24 * 60 * 60 + 2 * 60 * 60 + 0 * 60 + 0 # 180000.0 (data odniesienia depeszy nawigacyjnej)
t = 2 * 24 * 60 * 60 + 3 * 60 * 60 + 15 * 60 + 0 # 184500.0

nav = np.array([[t0c, 5.870070308447e-04, 1.307398633799e-11, 0.000000000000e+00],
                [2.400000000000e+01, -1.025000000000e+01, 4.909133056525e-09, 4.117597310113e-01],
                [-6.388872861862e-07, 3.030300256796e-03, 5.196779966354e-06, 5.153749139786e+03],
                [1.800000000000e+05,-8.009374141693e-08,-9.203488554469e-01,-1.862645149231e-09],
                [9.608171808408e-01, 2.788125000000e+02, 2.029634976455e+00, -8.358919611125e-09],
                [7.536028191537e-11, 1.000000000000e+00, 2.356000000000e+03, 0.000000000000e+00],
                [2.000000000000e+00, 0.000000000000e+00, 9.313226000000e-10, 2.400000000000e+01],
                [1.728000000000e+05, 4.000000000000e+00, 0.000000000000e+00, 0.000000000000e+00],
                ])

# ORBITY PRECYZYJNE #
Xsp3 = 6796.098769e3
Ysp3 = 25623.646806e3
Zsp3 = 837.694977e3
Tsp3 = 587.06450710e-6


s = 5 # częstotliwość próbkowania
N = 6*3600 / s + 1
Xarr = np.zeros(int(N))
Yarr = np.zeros(int(N))
Zarr = np.zeros(int(N))
rarr = np.zeros(int(N))
vararr = np.zeros(int(N))
delta_t_prim_arr = np.zeros(int(N))

j = 0
for i in range(184500, 184500+6*3600+1, s):
    data = wspolrzedneSatelity(180000, i, nav, [6796.098769e3, 25623.646806e3, 837.694977e3, 587.06450710e-6])
    Xarr[j] = data[0] / 1e3; Yarr[j] = data[1] / 1e3; Zarr[j] = data[2] / 1e3; rarr[j] = data[3] / 1e3
    vararr[j] = data[4]; delta_t_prim_arr[j] = data[5] * 1e6
    j += 1

delta_t = np.arange(0, 6*3600+1, s)
fig, axs = plt.subplots(2, 2, figsize=(10, 8), dpi=600)

axs[0, 0].plot(delta_t, Xarr)
axs[0, 0].plot(delta_t, Yarr)
axs[0, 0].plot(delta_t, Zarr)
axs[0, 0].set_title('Współrzędne geocentryczne satelity')
axs[0, 0].legend(['X', 'Y', 'Z'])
axs[0, 0].set_xlabel('Δt [s]')
axs[0, 0].set_ylabel('XYZ [km]')
axs[0, 0].grid(True)
axs[0, 0].ticklabel_format(style='plain')
axs[0, 1].plot(delta_t, rarr)
axs[0, 1].set_title('Promień orbity')
axs[0, 1].legend(['Promień'])
axs[0, 1].set_xlabel('Δt [s]')
axs[0, 1].set_ylabel('Promień [km]')
axs[0, 1].grid(True)
axs[0, 0].ticklabel_format(style='plain')
axs[1, 0].plot(delta_t, vararr)
axs[1, 0].set_title('Promień orbity')
axs[1, 0].legend(['Promień'])
axs[1, 0].set_xlabel('Δt [s]')
axs[1, 0].set_ylabel('Prędkość satelity [m/s]')
axs[1, 0].grid(True)
axs[1, 0].set_title('Prędkość wypadkowa')
axs[1, 0].legend(['Prędkość'])
axs[1, 1].plot(delta_t, delta_t_prim_arr)
axs[1, 1].set_title('Poprawka zegara satelity')
axs[1, 1].legend(["δt'"])
axs[1, 1].set_xlabel('Δt [s]')
axs[1, 1].set_ylabel("δt' [μs]")
axs[1, 1].grid(True)

fig.suptitle('Parametry satelity GPS w okresie 6 godzin od czasu t')
plt.tight_layout()
plt.show()
