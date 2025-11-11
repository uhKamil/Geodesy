import numpy as np
from datetime import datetime, timedelta

# Dane wyjściowe
nr = 18
alfa_GCRS = np.radians(8 * (360 / 24))
delta_GCRS = np.radians(50 + (nr / 60))
UTC = datetime(2010, 9, 1, 0, 5, 0) + timedelta(minutes=15 * nr)

# Obliczenia czasu i dat
def czas_na_julianski(t: datetime):
    S = 0
    y, mn, d, h, m, s, ms = t.year, t.month, t.day, t.hour, t.minute, t.second, t.microsecond
    # print(y, mn, d, h, m, s, ms)
    z = True
    # Kalendarz gregoriański
    while y > 1582:
        # print(y, y % 4 == 0 and y % 100 != 0, y % 400 == 0, S)
        if (y % 4 == 0 and y % 100 != 0) or y % 400 == 0:
            S += 366
        else:
            S += 365
        y -= 1
    # Kalendarz juliański
    while 1582 >= y > -4713:
        # print(y, y % 4 == 0 and y % 100 != 0, y % 400 == 0, S)
        if z:
            S -= 10  # uwzględnienie faktu, że 10 dni pominięto po reformie kalendarza
            z = False
        if y == 0:
            y -= 1
            continue
        if y % 4 == 0:
            S += 366
        else:
            S += 365
        y -= 1
    # print(f"S={S}")
    # Miesiące
    months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]  # dla 4173 r. p.n.e.
    if mn > 1:
        S += sum(months[:mn-1])
    # Dni
    if d > 1:
        S += d-1
    if d == 1 and h > 12:
        S += 1
    # Godziny (dodane w taki sposób, żeby utrzymać precyzję)
    d_diff = h * 3600 + m * 60 + s + ms / 10 ** 6
    d_diff = d_diff / 3600
    t_diff = abs(d_diff - 12)
    if h < 12:
        t_diff = 24 - t_diff
    S += t_diff/24
    return S

TT = UTC + timedelta(seconds=69.184)
TT_JD = czas_na_julianski(TT)
J2000 = datetime(2000, 1, 1, 12)
J2000_JD = czas_na_julianski(J2000)
t = (TT_JD - J2000_JD) / 36525
UT1 = UTC + timedelta(seconds=-0.0509211)
JD_UT1 = czas_na_julianski(UT1)

# Wektor kierunkowy do gwiazdy (GCRS)
p_GCRS = np.array([[np.cos(delta_GCRS) * np.cos(alfa_GCRS)],
              [np.cos(delta_GCRS) * np.sin(alfa_GCRS)],
              [np.sin(delta_GCRS)]])

# Macierz Q(t)
X = ((-0.016617 / 3600) + (2004.191898 / 3600) * t + (-0.4297829 / 3600) * t ** 2 +
     (-0.19861834 / 3600) * t ** 3 + (0.000007578 / 3600) * t ** 4 +
     (0.0000059285 / 3600) * t ** 5) * np.pi / 180
Y = ((-0.006951 / 3600) + (-0.025896 / 3600) * t + (-22.4072747 / 3600) * t ** 2 +
            (0.00190059 / 3600) * t ** 3 + (0.001112526 / 3600) * t ** 4 +
                 (0.0000001358 / 3600) * t ** 5) * np.pi / 180

a = 1/2 + 1/8 * (X ** 2 + Y ** 2)
s = (-(X * Y) / 2 + (0.000094 / 3600) + (0.00380865 / 3600) * t + (-0.00012268 / 3600) * t ** 2 +
     (-0.07257411 / 3600) * t ** 3 + (0.00002798 / 3600) * t ** 4 + (0.00001562 / 3600) * t ** 5) * np.pi / 180
E = np.degrees(np.arctan2(Y, X))
d = np.arctan(np.sqrt((X**2+Y**2) / (1-X**2-Y**2))) * 6371e3

Q0 = np.array([[1 - a * X ** 2, -a * X * Y, X],
              [-a * X * Y, 1 - a * Y ** 2, Y],
              [-X, -Y, 1 - a * (X ** 2 + Y ** 2)]])
R3 = np.array([[np.cos(s), np.sin(s), 0],
               [-np.sin(s), np.cos(s), 0],
               [0, 0, 1]])
Q = Q0 @ R3

# Macierz R(t)
Tu = JD_UT1 - J2000_JD
ERA = 2 * np.pi * (0.779057273264 + 1.00273781191135448 * Tu)

R = np.array([[np.cos(-ERA), np.sin(-ERA), 0],
               [-(np.sin(-ERA)), np.cos(-ERA), 0],
               [0, 0, 1]])

# Macierz W(t)
xp, yp = np.radians(0.206861) / 3600, np.radians(0.424536) / 3600
s2 = np.radians(-47 / (3600 * 1000)) * t

R3 = np.array([[np.cos(s2), np.sin(s2), 0],
               [-(np.sin(s2)), np.cos(s2), 0],
               [0, 0, 1]])
R2 = np.array([[np.cos(xp), 0, -(np.sin(xp))],
               [0, 1, 0],
               [np.sin(xp), 0, np.cos(xp)]])
R1 = np.array([[1, 0, 0],
               [0, np.cos(yp), np.sin(yp)],
               [0, -(np.sin(yp)), np.cos(yp)]])

Wt = R3 @ R2 @ R1

# Wektor kierunkowy do gwiazdy (ITRS)
p_ITRS = Wt.T @ R.T @ Q.T @ p_GCRS

# Współrzędne w ITRS
alfa_ITRS = np.arctan2(p_ITRS[1], p_ITRS[0])
delta_ITRS = np.arctan2(p_ITRS[2], np.sqrt(p_ITRS[0] ** 2 + p_ITRS[1] ** 2))

def deg_min_sec(d):
    deg = np.int_(d)
    r = d - deg
    min = np.int_(r * 60)
    r -= min / 60
    sec = r * 3600
    return deg, min, sec
def hr_m_s(d):
    hr = np.int_(d // 15)
    r = d - hr * 15
    min = np.int_(r // (15 / 60))
    r -= min * .25
    sec = r // (15 / 3600)
    return hr, min, sec

a, d = np.degrees(alfa_ITRS), np.degrees(delta_ITRS),
print(a, d)
print(f"Rektascensja (h,m,s): {hr_m_s(a)}, Deklinacja (deg,min,sec): {deg_min_sec(d)}")