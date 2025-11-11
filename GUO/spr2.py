import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Dane wyjściowe
nr = 18
alfa_GCRS = np.radians(8 * (360 / 24))
delta_GCRS = np.radians(50 + (nr / 60))
UTC = datetime(2010, 9, 1, 0, 5, 0) + timedelta(minutes=15 * nr)
ts_UTC = pd.Timestamp(UTC)
# Obliczenia czasu i dat
def czas_na_julianski(t: datetime):
    S = 0
    y, mn, d, h, m, s, ms = t.year, t.month, t.day, t.hour, t.minute, t.second, t.microsecond
    print(y, mn, d, h, m, s, ms)
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
    # Godziny
    t_diff = abs((h+m/60+s/(60**2)+ms/1000/(60**3)) - 12)
    if h < 12:
        t_diff = 24 - t_diff
    S += t_diff/24
    return S

def czas_na_julianski_2(t: datetime):
    S = 0
    y, mn, d, h, m, s, ms = t.year, t.month, t.day, t.hour, t.minute, t.second, t.microsecond
    print(y, mn, d, h, m, s, ms)
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
    # Godziny
    d_diff = h * 3600 + m * 60 + s + ms / 10 ** 6
    d_diff = d_diff / 3600
    t_diff = abs(d_diff - 12)
    if h < 12:
        t_diff = 24 - t_diff
    S += t_diff/24
    return S

TT = UTC + timedelta(seconds=69.184)
ts_TT = pd.Timestamp(TT)
TT_JD = ts_TT.to_julian_date()
J2000 = pd.Timestamp(datetime(2000, 1, 1, 12))
J2000_JD = J2000.to_julian_date()
print(J2000, czas_na_julianski(J2000), J2000_JD)
print(TT, czas_na_julianski(TT), czas_na_julianski_2(TT), TT_JD)
a = pd.Timestamp(datetime(2010, 9, 1, 13, 0, 0))
print(czas_na_julianski(a), a.to_julian_date())
stulecia_JD = (TT_JD - J2000_JD) / 36525
UT1 = UTC + timedelta(seconds=-0.0509211)
ts_UT1 = pd.Timestamp(UT1)
JD_UT1 = ts_UT1.to_julian_date()
print(ts_UT1, JD_UT1, czas_na_julianski(ts_UT1))

# Wektor kierunkowy do gwiazdy (GCRS)
p = np.array([[np.cos(delta_GCRS) * np.cos(alfa_GCRS)],
              [np.cos(delta_GCRS) * np.sin(alfa_GCRS)],
              [np.sin(delta_GCRS)]])
print(p)

# Macierze R
x = 1
R1x = np.array([[1, 0, 0],
                [0, np.cos(x), np.sin(x)],
                [0, -(np.sin(x)), np.cos(x)]])
R2x = np.array([[np.cos(x), 0, -(np.sin(x))],
                [0, 1, 0],
                [np.sin(x), 0, np.cos(x)]])
R3x = np.array([[np.cos(x), np.sin(x), 0],
                [-(np.sin(x)), np.cos(x), 0],
                [0, 0, 1]])

# Macierz Q
t = stulecia_JD
X = ((-0.016617 / 3600) + ((2004.191898 / 3600) * t) + ((-0.4297829 / 3600) * (t ** 2)) + (
            (-0.19861834 / 3600) * (t ** 3)) + ((0.000007578 / 3600) * (t ** 4)) + (
                 (0.0000059285 / 3600) * (t ** 5))) * (np.pi / 180)
Y = ((-0.006951 / 3600) + ((-0.025896 / 3600) * t) + ((-22.4072747 / 3600) * (t ** 2)) + (
            (0.00190059 / 3600) * (t ** 3)) + ((0.001112526 / 3600) * (t ** 4)) + (
                 (0.0000001358 / 3600) * (t ** 5))) * (np.pi / 180)
a = 1/2 + 1/8 * (X ** 2 + Y ** 2)
s = (-((X * Y) / 2)) + (((0.000094 / 3600) + ((0.00380865 / 3600) * t) + ((-0.00012268 / 3600) * (t ** 2)) + (
            (-0.07257411 / 3600) * (t ** 3)) + ((0.00002798 / 3600) * (t ** 4)) + ((0.00001562 / 3600) * (t ** 5))) * (
                                    np.pi / 180))

Q = np.array([[1 - a * (X ** 2), (-1) * a * X * Y, X],
              [(-1) * a * X * Y, 1 - a * (Y ** 2), Y],
              [-X, -Y, 1 - a * ((X ** 2) + (Y ** 2))]])

# Macierz R(t)
Tu = JD_UT1 - J2000_JD
ERA = 2 * np.pi * (0.779057273264 + (1.00273781191135448 * Tu))

Rt = np.array([[np.cos(-ERA), np.sin(-ERA), 0],
               [-(np.sin(-ERA)), np.cos(-ERA), 0],
               [0, 0, 1]])

# Macierz W(t)
xp, yp = np.radians(0.206861) / 3600, np.radians(0.424536) / 3600
st = -47 * (1 / 3600) * (1 / 1000) * (np.pi / 180) * t

R3_st = np.array([[np.cos(st), np.sin(st), 0],
                  [-(np.sin(st)), np.cos(st), 0],
                  [0, 0, 1]])
R2_xp = np.array([[np.cos(xp), 0, -(np.sin(xp))],
                  [0, 1, 0],
                  [np.sin(xp), 0, np.cos(xp)]])
R1_yp = np.array([[1, 0, 0],
                  [0, np.cos(yp), np.sin(yp)],
                  [0, -(np.sin(yp)), np.cos(yp)]])

Wt = R3_st @ R2_xp @ R1_yp

# Wektor kierunkowy do gwiazdy (ITRS)
p_ITRS = Wt.T @ Rt.T @ Q.T @ p

# α i δ dla ITRS
alfa_ITRS = np.arctan(p_ITRS[0] / p_ITRS[1])
delta_ITRS = np.arctan(p_ITRS[2] / (np.sqrt((p_ITRS[0] ** 2) + (p_ITRS[1] ** 2))))

ITRS = np.array([24 + np.degrees(alfa_ITRS * (24 / 360)),
                 np.degrees(delta_ITRS)])
print(ITRS)