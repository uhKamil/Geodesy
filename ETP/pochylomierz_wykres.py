import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Dane z tabeli
measurement_points = np.arange(1, 11)

# Pomiary pochylenia wzdłuż osi X
pomiar_tam_x = np.array([0.400, 0.227, -0.079, -0.282, -0.687, -1.213, -1.711, -2.170, -2.461, -2.929])
pomiar_powrot_x = np.array([0.415, 0.142, -0.043, -0.357, -0.541, -0.928, -1.369, -1.578, -1.957, -2.425])

# Pomiary pochylenia wzdłuż osi Y
pomiar_tam_y = np.array([0.266, 0.775, 1.112, 1.674, 2.187, 2.461, 2.728, 2.816, 2.940, 3.000])
pomiar_powrot_y = np.array([0.255, 0.881, 1.275, 1.603, 1.842, 2.103, 2.374, 2.588, 2.792, 2.649])

# Funkcja do tworzenia wykresów z regresją liniową
def plot_with_regression(x, y1, y2, title, ylabel):
    plt.figure(figsize=(10, 6), dpi=600)
    plt.plot(x, y1, 'o-', label='Pomiar tam')
    plt.plot(x, y2, 'o-', label='Pomiar powrót')

    # Regresja liniowa dla pomiar tam
    model1 = LinearRegression().fit(x.reshape(-1, 1), y1)
    y1_pred = model1.predict(x.reshape(-1, 1))
    plt.plot(x, y1_pred, '--', linewidth=1, label='Regresja tam')

    # Regresja liniowa dla pomiar powrót
    model2 = LinearRegression().fit(x.reshape(-1, 1), y2)
    y2_pred = model2.predict(x.reshape(-1, 1))
    plt.plot(x, y2_pred, '--', linewidth=1, label='Regresja powrót')
    plt.title(title)
    plt.xlabel('Punkty pomiarowe')
    plt.ylabel(ylabel)
    plt.xticks(x)
    plt.legend()
    plt.grid(True)
    plt.show()

# Wykres dla osi X
plot_with_regression(measurement_points, pomiar_tam_x, pomiar_powrot_x,
                    'Pomiar pochylenia wzdłuż osi X', 'Pochylenie [mrad]')

# Wykres dla osi Y
plot_with_regression(measurement_points, pomiar_tam_y, pomiar_powrot_y,
                    'Pomiar pochylenia wzdłuż osi Y', 'Pochylenie [mrad]')
