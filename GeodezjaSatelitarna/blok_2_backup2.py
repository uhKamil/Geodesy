import numpy as np

# STAŁE #
C = 299792458  # prędkość światła [m/s]


class Receiver:
    def __init__(self, initial_coords):
        self.X = np.array(initial_coords, dtype=np.float64)


class Satellite:
    def __init__(self, name, t, delta_t, delta_t_s, P, X):
        self.name = name
        self.t = t
        self.delta_t = delta_t
        self.delta_t_s = delta_t_s
        self.P = P
        self.X = X

    @staticmethod
    def wspolrzedne_transmisja(t, delta_t, delta_t_s, P, name, X):
        """
        :param delta_t: Różnica czasu między obserwacjami środkową a skrajnymi (łącznie 3) w minutach
        :param delta_t_s: Poprawka zegara dla satelity z pliku SP3 w mikrosekundach
        (zakłada się, że podana jest prawidłowa poprawka dla przyjętego t)
        :param t: Czas początkowy, np. lokalny albo jako czas GPS
        :param P: Pseudoodległość (obserwacja w danym momencie z pliku OBS)
        :param name: Nazwa satelity (informacyjnie)
        :param X: Współrzędne satelity z pliku SP3 dla 3 epok (typ np.array)
        :return: Współrzędne przybliżone satelity w epoce transmisji
        """
        X1, X2, X3 = X * 1e3
        delta_t *= 60
        delta_t_s /= 1e6

        X_dot_S = (X3 - X1) / (2 * delta_t)

        t_tr = t - (P + C * delta_t_s) / C  # epoka transmisji sygnału

        X_S_t_tr = X2 + X_dot_S * (t_tr - t)
        print(name, X)
        return X_S_t_tr

    @staticmethod
    def odleglosc_geometryczna(x_r, x_s):
        return np.linalg.norm(x_s - x_r)


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
        'delta_t_s': -15.132246,
        'P': 22266144.866,
        'X': np.array([
            [5006.492128, 15544.910971, 21429.400522],
            [3188.592979, 16965.693706, 20625.009554],
            [1519.661158, 18407.102372, 19478.824177]
        ])
    },
    "G09": {
        't': 11700,
        'delta_t': 15,
        'delta_t_s': 587.064507,
        'P': 24786037.688,
        'X': np.array([
            [6995.791112, 25307.882655, 3681.822550],
            [6796.098769, 25623.646806, 837.694977],
            [6529.647601, 25636.848199, -2020.921056]
        ])
    },
    "G14": {
        't': 11700,
        'delta_t': 15,
        'delta_t_s': 608.392523,
        'P': 21826960.376,
        'X': np.array([
            [23028.320781, 12886.430484, 4090.884444],
            [22356.112248, 12923.050496, 6806.560916],
            [21402.126281, 12903.032378, 9406.969401]
        ])
    },
    "G15": {
        't': 11700,
        'delta_t': 15,
        'delta_t_s': 269.998556,
        'P': 23955717.544,
        'X': np.array([
            [3986.710364, -21728.148032, 14126.329864],
            [4825.374644, -20089.827842, 16093.846950],
            [5823.529193, -18297.664098, 17772.500732]
        ])
    },
    "G30": {
        't': 11700,
        'delta_t': 15,
        'delta_t_s': -202.830096,
        'P': 20508210.340,
        'X': np.array([
            [15694.028676, 6823.498243, 20533.613054],
            [13941.068538, 8401.278147, 21183.934830],
            [12227.459501, 10100.782259, 21476.028371]
        ])
    }
}


def mnk(A: np.ndarray, L: np.ndarray, P: np.ndarray):
    return np.linalg.inv(A.T @ P @ A) @ A.T @ L


G05 = Satellite("G05", **satelity["G05"])
X_G05 = G05.wspolrzedne_transmisja(G05.t, G05.delta_t, G05.delta_t_s, G05.P, G05.name, G05.X)
G07 = Satellite("G07", **satelity["G07"])
X_G07 = G05.wspolrzedne_transmisja(G07.t, G07.delta_t, G07.delta_t_s, G07.P, G07.name, G07.X)
G09 = Satellite("G09", **satelity["G09"])
X_G09 = G05.wspolrzedne_transmisja(G09.t, G09.delta_t, G09.delta_t_s, G09.P, G09.name, G09.X)
G14 = Satellite("G14", **satelity["G14"])
X_G14 = G05.wspolrzedne_transmisja(G14.t, G14.delta_t, G14.delta_t_s, G14.P, G14.name, G14.X)
G15 = Satellite("G15", **satelity["G15"])
X_G15 = G05.wspolrzedne_transmisja(G15.t, G15.delta_t, G15.delta_t_s, G15.P, G15.name, G15.X)
G30 = Satellite("G30", **satelity["G30"])
X_G30 = G05.wspolrzedne_transmisja(G30.t, G30.delta_t, G30.delta_t_s, G30.P, G30.name, G30.X)

# Wedle założenia
Receiver = Receiver(np.array([0, 0, 0]))
X_r = Receiver.X
distDiff = 2

while distDiff > 1:
    print(f"X_r = {X_r}")
    dist_G05 = G05.odleglosc_geometryczna(X_r, X_G05)
    dist_G07 = G07.odleglosc_geometryczna(X_r, X_G07)
    dist_G09 = G09.odleglosc_geometryczna(X_r, X_G09)
    dist_G14 = G14.odleglosc_geometryczna(X_r, X_G14)
    dist_G15 = G15.odleglosc_geometryczna(X_r, X_G15)
    dist_G30 = G30.odleglosc_geometryczna(X_r, X_G30)
    print(dist_G05, dist_G07, dist_G09, dist_G14, dist_G15, dist_G30)
    L = np.array((
        [G05.P + C * G05.delta_t_s / 1e6 - dist_G05],
        [G07.P + C * G07.delta_t_s / 1e6 - dist_G07],
        [G09.P + C * G09.delta_t_s / 1e6 - dist_G09],
        [G14.P + C * G14.delta_t_s / 1e6 - dist_G14],
        [G15.P + C * G15.delta_t_s / 1e6 - dist_G15],
        [G30.P + C * G30.delta_t_s / 1e6 - dist_G30]
    )).reshape(6, 1)
    print(L)
    A = np.array([
        [-(X_G05[0] - X_r[0]) / dist_G05, -(X_G05[1] - X_r[1]) / dist_G05, -(X_G05[2] - X_r[2]) / dist_G05, 1],
        [-(X_G07[0] - X_r[0]) / dist_G07, -(X_G07[1] - X_r[1]) / dist_G07, -(X_G07[2] - X_r[2]) / dist_G07, 1],
        [-(X_G09[0] - X_r[0]) / dist_G09, -(X_G09[1] - X_r[1]) / dist_G09, -(X_G09[2] - X_r[2]) / dist_G09, 1],
        [-(X_G14[0] - X_r[0]) / dist_G14, -(X_G14[1] - X_r[1]) / dist_G14, -(X_G14[2] - X_r[2]) / dist_G14, 1],
        [-(X_G15[0] - X_r[0]) / dist_G15, -(X_G15[1] - X_r[1]) / dist_G15, -(X_G15[2] - X_r[2]) / dist_G15, 1],
        [-(X_G30[0] - X_r[0]) / dist_G30, -(X_G30[1] - X_r[1]) / dist_G30, -(X_G30[2] - X_r[2]) / dist_G30, 1],
    ])
    print(A)
    x, y, z, c_delta_t_r = mnk(A, L, np.diag([1] * 6).reshape(6, 6))
    distDiff = max(abs(x), abs(y), abs(z))
    print(x, y, z, c_delta_t_r, distDiff)
    X_r[0] += x
    X_r[1] += y
    X_r[2] += z
    G05.P -= c_delta_t_r
    G07.P -= c_delta_t_r
    G09.P -= c_delta_t_r
    G14.P -= c_delta_t_r
    G15.P -= c_delta_t_r
    G30.P -= c_delta_t_r

print(f"Ostatnia iteracja:\nX_r = {Receiver.X}, L^T = {L.T}")