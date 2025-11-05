import numpy as np
from scipy.optimize import minimize, root_scalar

x_data = np.array([0, 19.15, 45.7, 63.64, 78.61, 94.58, 105.1, 122.14, 143.92, 160.01, 156.27, 142.56, 131.24, 113.86, 85.77, 24.25, 169.61])
y_data = np.array([18.336, 14.947, 13.033, 11.986, 11.283, 10.755, 10.518, 10.332, 10.525, 10.988, 11.334, 10.852, 10.311, 10.378, 11.054, 14.567, 13.185])

def weighted_catenary_fit(x_data, y_data, weights=None):
    if weights is None:
        weights = np.ones(len(x_data))

    # Punkty brzegowe (niezmienne)
    x_start, y_start = x_data[0], y_data[0]
    x_end, y_end = x_data[-1], y_data[-1]

    def calculate_x0_c(a):
        def equation(x0):
            term1 = a * np.cosh((x_start - x0) / a)
            term2 = a * np.cosh((x_end - x0) / a)
            return (y_start - term1) - (y_end - term2)

        sol = root_scalar(equation, bracket=[x_start, x_end], method='brentq')
        x0 = sol.root
        c = y_start - a * np.cosh((x_start - x0) / a)
        return x0, c

    def weighted_objective(a):
        x0, c = calculate_x0_c(a)
        y_pred = a * np.cosh((x_data[1:-1] - x0) / a) + c
        residuals = y_data[1:-1] - y_pred
        # Zastosuj wagi - mniejsze wagi dla punktów z dużymi odchyleniami
        return np.sum(weights[1:-1] * residuals ** 2)

    # Dynamiczne obliczanie wag na podstawie odchyleń
    def calculate_adaptive_weights():
        # Pierwszy fit bez wag
        result = minimize(weighted_objective, 50.0, bounds=[(1, 1000)])
        a_temp = result.x[0]
        x0_temp, c_temp = calculate_x0_c(a_temp)

        # Oblicz poprawki
        y_pred_temp = a_temp * np.cosh((x_data - x0_temp) / a_temp) + c_temp
        residuals = np.abs(y_data - y_pred_temp)

        # Wagi odwrotnie proporcjonalne do residuów
        # weights_new = 1.0 / (1.0 + residuals ** 2)
        weights_new = 1.0 / (residuals ** 2)
        weights_new[0] = 20.0  # Wysokie wagi dla punktów brzegowych
        weights_new[-1] = 15.0
        return weights_new

    weights = calculate_adaptive_weights()
    result = minimize(weighted_objective, 100.0, bounds=[(1, 1000)])

    return result.x[0], weights

print(weighted_catenary_fit(x_data, y_data))