import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize, root_scalar

# Dane pomiarowe
x_data = np.array([0, 19.15, 45.7, 63.64, 78.61, 94.58, 105.1, 122.14, 143.92, 160.01, 156.27, 142.56,
                   131.24, 113.86, 85.77, 24.25, 169.61])
y_data = np.array([18.336, 14.947, 13.033, 11.986, 11.283, 10.755, 10.518, 10.332, 10.525, 10.988, 11.334, 10.852,
                   10.311, 10.378, 11.054, 14.567, 13.185])

# Sortowanie danych według x
sort_idx = np.argsort(x_data)
x_sorted = x_data[sort_idx]
y_sorted = y_data[sort_idx]

# Funkcja katenoidy
def catenary(x, a, x0, c):
    return a * np.cosh((x - x0) / a) + c

# Oblicz x0 i c dla danego a, aby katenoida przechodziła przez punkty brzegowe
def calculate_x0_c(a):
    def equation(x0):
        term1 = a * np.cosh((x_sorted[0] - x0) / a)
        term2 = a * np.cosh((x_sorted[-1] - x0) / a)
        return (y_sorted[0] - term1) - (y_sorted[-1] - term2)
    sol = root_scalar(equation, bracket=[x_sorted[0], x_sorted[-1]], method='brentq')
    if not sol.converged:
        raise ValueError("Nie znaleziono rozwiązania dla x0!")
    x0 = sol.root
    c = y_sorted[0] - a * np.cosh((x_sorted[0] - x0) / a)
    return x0, c

# Funkcja celu (tylko dla punktów pośrednich)
def weighted_objective(a, weights):
    x0, c = calculate_x0_c(a)
    y_pred = catenary(x_sorted[1:-1], a, x0, c)
    residuals = y_sorted[1:-1] - y_pred
    return np.sum(weights[1:-1] * residuals ** 2)

# Dynamiczne obliczanie wag na podstawie odchyleń
def calculate_adaptive_weights():
    # Pierwszy fit bez wag
    result = minimize(lambda a: weighted_objective(a, np.ones(len(x_sorted))), np.array([100.0]), bounds=[(1, 1000)])
    a_temp = result.x[0]
    x0_temp, c_temp = calculate_x0_c(a_temp)
    y_pred_temp = catenary(x_sorted, a_temp, x0_temp, c_temp)
    residuals = np.abs(y_sorted - y_pred_temp)
    # Wagi odwrotnie proporcjonalne do kwadratu poprawek
    weights_new = 1.0 / (residuals ** 2 + 1e-10)  # +1e-10 by uniknąć dzielenia przez zero
    # Wyższe wagi dla punktów brzegowych
    weights_new[0], weights_new[-1] = 20.0, 15.0
    return weights_new

# Wyznaczenie wag i optymalizacja
weights = calculate_adaptive_weights()
result = minimize(lambda a: weighted_objective(a, weights), 100.0, bounds=[(1, 1000)])

if result.success:
    a_opt = result.x[0]
    x0_opt, c_opt = calculate_x0_c(a_opt)
    # Generowanie gęstej siatki punktów do rysowania gładkiej krzywej
    x_dense = np.linspace(x_sorted[0], x_sorted[-1], 1000)
    y_fit = catenary(x_sorted, a_opt, x0_opt, c_opt)
    y_fit_dense = catenary(x_dense, a_opt, x0_opt, c_opt)

    # Współczynnik R^2
    ss_res = np.sum((y_sorted - y_fit) ** 2)
    ss_tot = np.sum((y_sorted - np.mean(y_sorted)) ** 2)
    r_squared = 1 - (ss_res / ss_tot)
    print(f"Współczynnik R^2: {r_squared:.5f}")

    # Rysowanie wykresu
    plt.figure(figsize=(10, 6))
    plt.plot(x_sorted, y_sorted, 'o', label='Dane pomiarowe')
    plt.plot(x_dense, y_fit_dense, '-', label='Dopasowana katenoida', linewidth=1.5)
    plt.xlabel('Odległość od początku liny [m]')
    plt.ylabel('Wysokość [m]')
    plt.title('Dopasowanie katenoidy do danych pomiarowych z wagami adaptacyjnymi')
    plt.ylim(bottom=0)
    plt.legend()
    plt.grid(True)
    plt.show()

    print(f"Parametry optymalne:\na = {a_opt:.2f}\nx0 = {x0_opt:.2f} m\nc = {c_opt:.2f} m\n"
          f"h_min = {catenary(x0_opt, a_opt, x0_opt, c_opt):.2f} m")
else:
    print("Optymalizacja nie powiodła się!")