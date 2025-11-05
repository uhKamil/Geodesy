import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# Dane pomiarowe
x_data = np.array([0, 19.15, 45.7, 63.64, 78.61, 94.58, 105.1, 122.14, 143.92, 160.01, 156.27, 142.56, 131.24, 113.86, 85.77, 24.25, 169.61])
y_data = np.array([18.336, 14.947, 13.033, 11.986, 11.283, 10.755, 10.518, 10.332, 10.525, 10.988, 11.334, 10.852, 10.311, 10.378, 11.054, 14.567, 13.185])

# Punkty brzegowe (niezmienne)
x_start, y_start = x_data[0], y_data[0]
x_end, y_end = x_data[-1], y_data[-1]


# Funkcja katenoidy z parametrami a, x0, c
def catenary(x, a, x0, c):
    return a * np.cosh((x - x0) / a) + c


# Oblicz x0 i c dla danego a, aby katenoida PRZECHODZIŁA DOKŁADNIE przez punkty brzegowe
def calculate_x0_c(a):
    # Rozwiązujemy układ równań nieliniowych dla x0
    from scipy.optimize import root_scalar

    def equation(x0):
        term1 = a * np.cosh((x_start - x0) / a)
        term2 = a * np.cosh((x_end - x0) / a)
        return (y_start - term1) - (y_end - term2)

    # Szukamy x0 w przedziale między punktami
    sol = root_scalar(equation, bracket=[x_start, x_end], method='brentq')

    if not sol.converged:
        raise ValueError("Nie znaleziono rozwiązania dla x0!")

    x0 = sol.root
    c = y_start - a * np.cosh((x_start - x0) / a)

    return x0, c


# Funkcja celu (tylko dla punktów pośrednich)
def objective(a):
    x0, c = calculate_x0_c(a)
    y_pred = catenary(x_data[1:-1], a, x0, c)  # Tylko punkty pośrednie
    return np.sum((y_data[1:-1] - y_pred) ** 2)


# Optymalizacja parametru a
initial_guess = 50.0  # Lepsze przybliżenie początkowe
result = minimize(objective, initial_guess, method='L-BFGS-B', bounds=[(1, 1000)])

# Wyniki
if result.success:
    a_opt = result.x[0]
    x0_opt, c_opt = calculate_x0_c(a_opt)

    # Weryfikacja punktów brzegowych
    y_start_fit = catenary(x_start, a_opt, x0_opt, c_opt)
    y_end_fit = catenary(x_end, a_opt, x0_opt, c_opt)

    print(f"Parametry optymalne:")
    print(f"a = {a_opt:.2f} m")
    print(f"x0 = {x0_opt:.2f} m")
    print(f"c = {c_opt:.2f} m")
    print(f"\nWeryfikacja punktów brzegowych:")
    print(f"Początek: y_measured={y_start}, y_fitted={y_start_fit:.3f}, różnica={y_start - y_start_fit:.6f} m")
    print(f"Koniec: y_measured={y_end}, y_fitted={y_end_fit:.3f}, różnica={y_end - y_end_fit:.6f} m")
else:
    print("Optymalizacja nie powiodła się!")

# Wykres dopasowania
x_fit = np.linspace(np.min(x_data), np.max(x_data), 500)
y_fit = catenary(x_fit, a_opt, x0_opt, c_opt)
minimum_x = x0_opt
minimum_y = catenary(minimum_x, a_opt, x0_opt, c_opt)

plt.figure(figsize=(10, 6))
plt.ylim(0, 20)
plt.scatter(x_data, y_data, color='blue', label='Dane pomiarowe')
plt.plot(x_fit, y_fit, color='red', label='Dopasowana katenoida')
plt.scatter(minimum_x, minimum_y, color='green', s=100, label='Minimum (zwis liny)')
plt.xlabel('Odległość od początku liny')
plt.ylabel('Wysokość')
plt.title('Dopasowanie katenoidy do danych pomiarowych')
plt.legend()
plt.grid(True)
plt.show()