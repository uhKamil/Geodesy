import numpy as np

X, Y, Z = 3530686.5373, 1243375.5402, 5146944.6214
X = np.array([X, Y, Z]).reshape(3, 1)

t_etrf2000, t = 2015, 2011
delta_t = t - t_etrf2000

T1, T2, T3, D = 53.8e-3, 51.8e-3, -82.2e-3, 2.25e-9
R1, R2, R3 = np.radians(2.106 / 3600 * 1e-3), np.radians(12.74 / 3600 * 1e-3), np.radians(-20.592 / 3600 * 1e-3)
T1_R, T2_R, T3_R, D_R = .1e-3, 0, -1.7e-3, .11e-9
R1_R, R2_R, R3_R = np.radians(.081 / 3600 * 1e-3), np.radians(.49 / 3600 * 1e-3), np.radians(-.792 / 3600 * 1e-3)

T = np.array([T1, T2, T3]).reshape(3, 1) + np.array([T1_R, T2_R, T3_R]).reshape(3, 1) * delta_t
D = D + D_R * delta_t
R1, R2, R3 = R1 + R1_R * delta_t, R2 + R2_R * delta_t, R3 + R3_R * delta_t
R = np.array([D, -R3, R2,
              R3, D, -R1,
              -R2, R1, D]).reshape(3, 3)

X_2011 = X + T + R @ X
print(X_2011)