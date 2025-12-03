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
        :return: Macierz F potrzebna do obliczenia C_NEU
        """

        lamb = np.atan2(y, x)
        e = self.e2 * (self.a / self.b) ** 2
        p = np.sqrt(x ** 2 + y ** 2)
        r = np.sqrt(p ** 2 + z ** 2)
        u = np.atan2()

        F = np.array([
            [],
            [],
            []
        ]).reshape(3, 3)

        return lamb


WGS84 = Ellipsoid("WGS 84", 6378137.0, 1 / 298.257223563)
F = WGS84.matrix_f(*X)
