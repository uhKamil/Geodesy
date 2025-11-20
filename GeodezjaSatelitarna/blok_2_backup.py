import numpy as np

"""
G    8 C1C L1C D1C S1C C2L L2L D2L S2L                      SYS / # / OBS TYPES
> 2025 03 04 03 15 00.0000000  0 32
G05  21158880.526   111190683.284          57.215          48.000    21158873.248    86642068.579          44.585          48.000
G07  22266144.866   117009417.031        2226.747          48.000    22266135.751    91176199.089        1735.113          44.000
G09  24786037.688   130251575.226        3521.717          37.000    24786033.648   101494796.675        2744.195          39.000
G14  21826960.376   114701466.779       -2671.867          46.000    21826953.017    89377769.552       -2082.006          46.000
G15  23955717.544   125888145.084       -3724.689          41.000    23955709.867    98094629.583       -2902.368          39.000
G30  20508210.340   107771417.487         560.301          51.000    20508204.506    83977758.313         436.597          47.000
*  2025  3  4  3  0  0.00000000
PG05  15786.990604  -8519.048568  19436.911986   -203.551466  4  6  5  55
PG07   5006.492128  15544.910971  21429.400522    -15.131174  2  6  7  85
PG09   6995.791112  25307.882655   3681.822550    587.052800  2  5  5  41
PG14  23028.320781  12886.430484   4090.884444    608.386742  3  4  5  59
PG15   3986.710364 -21728.148032  14126.329864    269.995058  5  5  3  59
PG30  15694.028676   6823.498243  20533.613054   -202.838116  6  6  7  79
*  2025  3  4  3 15  0.00000000
PG05  17825.476039  -7778.153234  17946.880448   -203.552242  4  6  4  51
PG07   3188.592979  16965.693706  20625.009554    -15.132246  3  5  7  74
PG09   6796.098769  25623.646806    837.694977    587.064507  2  5  5  22
PG14  22356.112248  12923.050496   6806.560916    608.392523  2  4  5  58
PG15   4825.374644 -20089.827842  16093.846950    269.998556  4  5  3  45 ,
PG30  13941.068538   8401.278147  21183.934830   -202.830096  6  6  6  66
*  2025  3  4  3 30  0.00000000
PG05  19717.301619  -7193.548603  16144.631303   -203.553529  3  6  4  74
PG07   1519.661158  18407.102372  19478.824177    -15.133036  4  5  7  68
PG09   6529.647601  25636.848199  -2020.921056    587.076298  3  5  5  34
PG14  21402.126281  12903.032378   9406.969401    608.398297  1  4  5  78
PG15   5823.529193 -18297.664098  17772.500732    270.002916  3  5  2  81
PG30  12227.459501  10100.782259  21476.028371   -202.822046  5  6  6  54
"""
# STAŁE #
C = 299792458  # prędkość światła [m/s]


# Dla jednego satelity G05
# P_05 = 21158880.526 # pseudoodległość
# delta_t_s = -203.552242 / 1e6
# X_SP3_03_00 = np.array([15786.990604,  -8519.048568,  19436.911986])
# X_SP3_03_15 = np.array([17825.476039,  -7778.153234,  17946.880448])
# X_SP3_03_30 = np.array([19717.301619,  -7193.548603,  16144.631303])
# delta_t = 15 * 60
#
# X_dot_S = (X_SP3_03_30 - X_SP3_03_00) / (2 * delta_t) * 1e3
# print(X_dot_S)
#
# t = 11700 # 3:15:00 (lokalnie dla dnia)
# t_tr = t - (P_05 + C * delta_t_s) / C # epoka transmisji sygnału
# print(t_tr)
#
# X_S_t_tr = X_SP3_03_15 + X_dot_S * (t_tr - t)
# print(X_S_t_tr)

class Coordinates:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Satelita:
    def __init__(self, name, t, delta_t, delta_t_s, P):
        self.name = name
        self.t = t
        self.delta_t = delta_t
        self.delta_t_s = delta_t_s
        self.P = P

    def wspolrzedne_transmisja(self, t, delta_t, delta_t_s, P, name, *X):
        """
        :param delta_t_s: Poprawka zegara dla satelity z pliku SP3 w mikrosekundach
        (zakłada się, że podana jest prawidłowa poprawka dla przyjętego t)
        :param t: Różnica czasu między obserwacjami środkową a skrajnymi (łącznie 3) w minutach
        :param P: Pseudoodległość (obserwacja w danym momencie z pliku OBS)
        :param name: Nazwa satelity (informacyjnie)
        :param X: Współrzędne satelity z pliku SP3 dla 3 epok (typ np.array)
        :return: Współrzędne przybliżone satelity w epoce transmisji
        """
        X1, X2, X3 = X
        delta_t *= 60
        delta_t_s /= 1e6  # poprawka zegara na czasu t z SP3 (w mikrosekundach)

        X_dot_S = (X3 - X1) / (2 * delta_t) * 1e3

        t_tr = t - (P + C * delta_t_s) / C  # epoka transmisji sygnału
        print(t_tr)

        X_S_t_tr = X2 + X_dot_S * (t_tr - t)
        print(name, X_S_t_tr)
        return X_S_t_tr




def wspolrzedne_transmisja(t, delta_t, delta_t_s, P, name, *X):
    """
    :param delta_t_s: Poprawka zegara dla satelity z pliku SP3 w mikrosekundach
    (zakłada się, że podana jest prawidłowa poprawka dla przyjętego t)
    :param t: Różnica czasu między obserwacjami środkową a skrajnymi (łącznie 3) w minutach
    :param P: Pseudoodległość (obserwacja w danym momencie z pliku OBS)
    :param name: Nazwa satelity (informacyjnie)
    :param X: Współrzędne satelity z pliku SP3 dla 3 epok (typ np.array)
    :return: Współrzędne przybliżone satelity w epoce transmisji
    """
    X1, X2, X3 = X
    delta_t *= 60
    delta_t_s /= 1e6  # poprawka zegara na czasu t z SP3 (w mikrosekundach)

    X_dot_S = (X3 - X1) / (2 * delta_t) * 1e3

    t_tr = t - (P + C * delta_t_s) / C  # epoka transmisji sygnału
    print(t_tr)

    X_S_t_tr = X2 + X_dot_S * (t_tr - t)
    print(name, X_S_t_tr)
    return X_S_t_tr


satelity = {
    "G05": {
        't': 11700,
        'delta_t': 15,
        'delta_t_s': -203.552242,
        'P': 21158880.526,
        'X': np.array([
            [15786.990604, -8519.048568, 19436.911986],
            [17825.476039, -7778.153234, 17946.880448],
            [19717.301619, -7193.548603, 16144.631303]
        ])
    },
    "G07": {
        't': 11700,
        'delta_t': 15,
        'delta_t_s': -203.552242,
        'P': 21158880.526,
        'X': np.array([
            [15786.990604, -8519.048568, 19436.911986],
            [17825.476039, -7778.153234, 17946.880448],
            [19717.301619, -7193.548603, 16144.631303]
        ])
    },
    "G09": {
        't': 11700,
        'delta_t': 15,
        'delta_t_s': -203.552242,
        'P': 21158880.526,
        'X': np.array([
            [15786.990604, -8519.048568, 19436.911986],
            [17825.476039, -7778.153234, 17946.880448],
            [19717.301619, -7193.548603, 16144.631303]
        ])
    },
    "G14": {
        't': 11700,
        'delta_t': 15,
        'delta_t_s': -203.552242,
        'P': 21158880.526,
        'X': np.array([
            [15786.990604, -8519.048568, 19436.911986],
            [17825.476039, -7778.153234, 17946.880448],
            [19717.301619, -7193.548603, 16144.631303]
        ])
    },
    "G15": {
        't': 11700,
        'delta_t': 15,
        'delta_t_s': -203.552242,
        'P': 21158880.526,
        'X': np.array([
            [15786.990604, -8519.048568, 19436.911986],
            [17825.476039, -7778.153234, 17946.880448],
            [19717.301619, -7193.548603, 16144.631303]
        ])
    },
    "G30": {
        't': 11700,
        'delta_t': 15,
        'delta_t_s': -203.552242,
        'P': 21158880.526,
        'X': np.array([
            [15786.990604, -8519.048568, 19436.911986],
            [17825.476039, -7778.153234, 17946.880448],
            [19717.301619, -7193.548603, 16144.631303]
        ])
    }
}


def odleglosc_geometryczna(x_r, x_s):
    xr, yr, zr = x_r
    xs, ys, zs = x_s
    return np.sqrt((xs - xr) ** 2 + (ys - yr) ** 2 + (zs - zr) ** 2)


X_G05 = wspolrzedne_transmisja(11700, 15, -203.552242, 21158880.526, "G05",
                                np.array([15786.990604, -8519.048568, 19436.911986]),
                                np.array([17825.476039, -7778.153234, 17946.880448]),
                                np.array([19717.301619, -7193.548603, 16144.631303]))
X_G07 = wspolrzedne_transmisja(11700, 15, -15.132246, 22266144.866, "G07",
                                np.array([5006.492128, 15544.910971, 21429.400522]),
                                np.array([3188.592979, 16965.693706, 20625.009554]),
                                np.array([1519.661158, 18407.102372, 19478.824177]))
X_G09 = wspolrzedne_transmisja(11700, 15, 587.064507, 24786037.688, "G09",
                                np.array([6995.791112, 25307.882655, 3681.822550]),
                                np.array([6796.098769, 25623.646806, 837.694977]),
                                np.array([6529.647601, 25636.848199, -2020.921056]))
X_G14 = wspolrzedne_transmisja(11700, 15, 608.392523, 21826960.376, "G14",
                                np.array([23028.320781, 12886.430484, 4090.884444]),
                                np.array([22356.112248, 12923.050496, 6806.560916]),
                                np.array([21402.126281, 12903.032378, 9406.969401]))
X_G15 = wspolrzedne_transmisja(11700, 15, 269.998556, 23955717.544, "G15",
                                np.array([3986.710364, -21728.148032, 14126.329864]),
                                np.array([4825.374644, -20089.827842, 16093.846950]),
                                np.array([5823.529193, -18297.664098, 17772.500732]))
X_G30 = wspolrzedne_transmisja(11700, 15, -202.830096, 20508210.340, "G30",
                               np.array([15694.028676, 6823.498243, 20533.613054]),
                               np.array([13941.068538, 8401.278147, 21183.934830]),
                               np.array([12227.459501, 10100.782259, 21476.028371]))

dist_G05 = odleglosc_geometryczna([0, 0, 0], X_G05)
print(dist_G05)

G05 = Satelita(*satelity["G05"])
print(G05)
X_G05 = G05.wspolrzedne_transmisja()
print(X_G05)


