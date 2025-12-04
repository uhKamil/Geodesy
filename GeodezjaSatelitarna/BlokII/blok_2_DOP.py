import numpy as np
import blok_2_SPP as spp

# Macierz z ostatniej iteracji SPP
A = spp.A
Cx = np.linalg.inv(A.T @ A)
C_XYZ = Cx[0:3, 0:3].copy()  # macierz kowariancji współrzędnych ECEF

# print(Cx)
# print(C_XYZ)

X = spp.Receiver.X.copy()


class Ellipsoid:
    def __init__(self, name: str, a, f):
        self.name = name
        self.a = a
        self.f = f
        self.b = a * (1 - f)
        self.e2 = 1 - (1 - f) ** 2

    def matrix_f(self, x, y, z):
        """
        :param x: Współrzędna x odbiornika
        :param y: Współrzędna y odbiornika
        :param z: Współrzędna z odbiornika
        :return: Macierz F potrzebna do obliczenia C_ENU
        """

        lamb = np.atan2(y, x)
        e = self.e2 * (self.a / self.b) ** 2
        p = np.sqrt(x ** 2 + y ** 2)
        r = np.sqrt(p ** 2 + z ** 2)
        u = np.atan2(self.b * z * (1 + e * self.b / r), self.a * p)
        phi = np.atan2(z + e * self.b * np.sin(u) ** 3, p - self.e2 * self.a * np.cos(u) ** 3)
        v = self.a / np.sqrt(1 - self.e2 * np.sin(phi) ** 2)
        h = p * np.cos(phi) + z * np.sin(phi) - self.a ** 2 / v

        print(f"{np.rad2deg(phi):.8f}, {np.rad2deg(lamb):.8f}")

        F = np.array([
            [-np.sin(lamb), np.cos(lamb), 0],
            [-np.sin(phi) * np.cos(lamb), -np.sin(phi) * np.sin(lamb), np.cos(phi)],
            [np.cos(phi) * np.cos(lamb), np.cos(phi) * np.sin(lamb), np.sin(phi)]
        ]).reshape(3, 3)

        return F


WGS84 = Ellipsoid("WGS 84", 6378137.0, 1 / 298.257223563)
F = WGS84.matrix_f(*X)
C_ENU = F.T @ C_XYZ @ F

# Współczynniki rozmycia dokładności (DOP)
GDOP = np.sqrt(C_ENU[0][0] + C_ENU[1][1] + C_ENU[2][2] + Cx[3][3])
PDOP = np.sqrt(C_ENU[0][0] + C_ENU[1][1] + C_ENU[2][2])
HDOP = np.sqrt(C_ENU[0][0] + C_ENU[1][1])
VDOP = np.sqrt(C_ENU[2][2])
TDOP = np.sqrt(Cx[3][3])
print(f"{GDOP:.1f}, {PDOP:.1f}, {HDOP:.1f}, {VDOP:.1f}, {TDOP:.1f}")

# Współrzędne, azymuty i kąty elewacji satelitów
for name, sat in spp.sats.items():
    ENU_S = F.T @ (sat.X_transmission - X)
    A_S_rad = np.atan2(ENU_S[0], ENU_S[1])
    A_S_rad = np.where(A_S_rad < 0, A_S_rad + 2 * np.pi, A_S_rad)
    A_S_deg = np.rad2deg(A_S_rad)
    print(sat.name, f"{A_S_deg:.1f}")

    e_S_rad = np.atan2(ENU_S[2], np.sqrt(ENU_S[0] ** 2 + ENU_S[1] ** 2))
    e_S_deg = np.rad2deg(e_S_rad)
    print(sat.name, f"{e_S_deg:.1f}")
