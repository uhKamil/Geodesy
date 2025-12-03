import numpy as np

# DANE #
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

# STAŁE #
C = 299792458  # prędkość światła [m/s]


class Satellite:
    def __init__(self, name, t, delta_t, delta_t_s, P, X):
        self.name = name
        self.t = t
        self.delta_t = delta_t
        self.delta_t_s = delta_t_s
        self.P = P
        self.X = X
        
    def __transmission__(self, X_transmission):
        self.X_transmission = X_transmission

    def transmission_coords(self, t, delta_t, delta_t_s, P, name, X):
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
        # print(name, X)
        return X_S_t_tr

    def odleglosc_geometryczna(self, x_r, x_s):
        return np.linalg.norm(x_s - x_r)


class Receiver:
    def __init__(self, initial_coords, cdt_r=0):
        self.X = np.array(initial_coords, dtype=np.float64)
        self.cdt_r = cdt_r # poprawka zegara odbiornika [m]

    def receiver_coords(self, satellites: dict, P, i):
        X_r = self.X

        L = []
        A = []

        for name, sat in satellites.items():
            X_s = sat.X_transmission
            rho = sat.odleglosc_geometryczna(X_r, X_s)
            L += [sat.P + C * sat.delta_t_s / 1e6 - rho]
            A += [-(X_s[0] - X_r[0]) / rho]
            A += [-(X_s[1] - X_r[1]) / rho]
            A += [-(X_s[2] - X_r[2]) / rho]
            A += [1]
            if i == 1:
                print(name, f"{rho:.3f}")

        L = np.array([L]).reshape(len(satellites), 1)
        A = np.array([A]).reshape(len(satellites), 4)

        if i == 1:
            for i in range(len(L)):
                print(f"{L[i][0]:.4f}")

        dX = mnk(A, L, P)
        dx, dy, dz, d_cdt_r = dX.flatten()

        if i > 1:
            print(f"{dx:.3f}, {dy:.3f}, {dz:.3f}, {d_cdt_r:.3f}")
        
        self.X[0] += dx
        self.X[1] += dy
        self.X[2] += dz
        self.cdt_r += d_cdt_r
        return max(abs(dx), abs(dy), abs(dz)), A


def mnk(A: np.ndarray, L: np.ndarray, P: np.ndarray):
    return np.linalg.inv(A.T @ P @ A) @ A.T @ L


sats = {}
for name, data in satelity.items():
    sats[name] = Satellite(name, **data)
    sats[name].X_transmission = sats[name].transmission_coords(**data, name=name)
    print(name, f"{sats[name].X_transmission[0]:.3f}, {sats[name].X_transmission[1]:.3f}, {sats[name].X_transmission[2]:.3f}")

Receiver = Receiver(initial_coords=([0, 0, 0]))  # założenie
dist_diff = 2  # zmienna do inicjalizacji pętli i kontroli przyrostów współrzędnych
i = 1 # do pliku txt (która iteracja)

while dist_diff > 1:
    P = np.diag([1] * 6)
    dist_diff, A = Receiver.receiver_coords(sats, P, i)
    i += 1

# Finalne współrzędne odbiornika
for c in Receiver.X:
    print(f"{c:.3f}")

# Różnica między współrzędnymi referencyjnymi
X_ref = np.array([3835044.3194, 1179902.7961, 4941503.7548])

for i in range(len(X_ref)):
    print(f"{X_ref[i]-Receiver.X[i]:.3f}")