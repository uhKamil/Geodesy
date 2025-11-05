import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Dane pomiarowe (odległość od początku liny, wysokość)
data_points = np.array([
    (0, 18.336),
    (19.15, 14.947),
    (45.7, 13.033),
    (63.64, 11.986),
    (78.61, 11.283),
    (94.58, 10.755),
    (105.10, 10.518),
    (122.14, 10.332),
    (143.92, 10.525),
    (160.01, 10.988),
    (169.61, 13.185),
    (156.27, 11.334),
    (142.56, 10.852),
    (131.24, 10.311),
    (113.86, 10.378),
    (85.77, 11.054),
    (24.25, 14.567)
])

x_data = data_points[:, 0]
y_data = data_points[:, 1]

# Definicja funkcji katenoidy
# y = a * cosh((x - x0) / a) + c

def catenary(x, a, x0, c):
    return a * np.cosh((x - x0) / a) + c

# Przybliżenie początkowe parametrów
initial_guess = [10, np.mean(x_data), np.min(y_data)]

# Dopasowanie krzywej
params, covariance = curve_fit(catenary, x_data, y_data, p0=initial_guess)
a_fit, x0_fit, c_fit = params

# Wyznaczenie minimum funkcji katenoidy (punkt zwisu liny)
# Minimum funkcji cosh jest w punkcie x0
minimum_x = x0_fit
minimum_y = catenary(minimum_x, a_fit, x0_fit, c_fit)

# Wykres dopasowania
x_fit = np.linspace(np.min(x_data), np.max(x_data), 500)
y_fit = catenary(x_fit, a_fit, x0_fit, c_fit)

plt.figure(figsize=(10, 6))
plt.scatter(x_data, y_data, color='blue', label='Dane pomiarowe')
plt.plot(x_fit, y_fit, color='red', label='Dopasowana katenoida')
plt.scatter(minimum_x, minimum_y, color='green', s=100, label='Minimum (zwis liny)')
plt.xlabel('Odległość od początku liny')
plt.ylabel('Wysokość')
plt.title('Dopasowanie katenoidy do danych pomiarowych')
plt.legend()
plt.grid(True)
plt.show()

print(minimum_x, minimum_y, a_fit, x0_fit, c_fit)