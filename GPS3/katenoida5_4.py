"""
Poprawiono interpretację h (bo w końcu ogarnąłem, jak to się liczy poprawnie), przez co R^2 wzrosło prawie do 1
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize, root_scalar

# Dane pomiarowe
# St2 jest wyżej niż St1, przy czym H_St1 = 0
delta_h = np.mean([np.abs(1.757 + 5.18 / np.tan(101.7818 * np.pi / 200) - 1.6),
                   np.abs(1.733 + 5.18 / np.tan(101.7666 * np.pi / 200) - 1.6)])  # 0.01138112835524463 m
h_st1, h_st2 = 1.757, delta_h + 1.733
Va_data = np.array([93.7184 * np.pi / 200, 93.6156 * np.pi / 200, 93.4564 * np.pi / 200, 93.2572 * np.pi / 200,
                    92.9508 * np.pi / 200, 92.7258 * np.pi / 200, 92.3376 * np.pi / 200, 91.8820 * np.pi / 200,
                    91.6476 * np.pi / 200, 91.3314 * np.pi / 200, 91.6364 * np.pi / 200, 91.9412 * np.pi / 200,
                    92.4152 * np.pi / 200, 93.1032 * np.pi / 200, 93.7690 * np.pi / 200])
d_data = np.array([151, 129.52, 116.19, 106.16, 96.79, 91.65, 85.43, 82.09, 83.27,
                   79.08, 79.17, 81.01, 86.69, 101.64, 148.36])
h_data = d_data / np.tan(Va_data)
for i in range(9):
    h_data[i] += h_st1
for i in range(9, len(h_data)):
    h_data[i] += h_st2
x_data = np.array([0, 19.15, 45.69, 63.64, 78.56, 94.58, 105.1, 122.15, 143.92, 160, 156.27, 142.56,
                   131.24, 113.86, 85.77, 24.25, 169.61])
y_data = np.concat((np.array([18.336]), h_data, np.array([13.185])), axis=0)

# Funkcja katenoidy
def catenary(x, a, x0, c):
    return a * np.cosh((x - x0) / a) + c

# Funkcja celu z parametrami a, y_start, y_end (punkty brzegowe mogą się zmieniać)
def objective(params):
    a, y_start, y_end = params
    x_start, x_end = x_data[0], x_data[-1]
    def calculate_x0_c(a, y_start, y_end):
        def equation(x0):
            term1 = a * np.cosh((x_start - x0) / a)
            term2 = a * np.cosh((x_end - x0) / a)
            return (y_start - term1) - (y_end - term2)
        sol = root_scalar(equation, bracket=[x_start, x_end], method='brentq')
        if not sol.converged:
            raise ValueError("Nie znaleziono rozwiązania dla x0")
        x0 = sol.root
        c = y_start - a * np.cosh((x_start - x0) / a)
        return x0, c
    x0, c = calculate_x0_c(a, y_start, y_end)
    y_pred = catenary(x_data, a, x0, c)
    return np.sum((y_data - y_pred) ** 2)

# Początkowe wartości parametrów: a, y_start, y_end i optymalizacja
initial_guess = np.array([800.0, y_data[0], y_data[-1]])
result = minimize(objective, initial_guess, method='L-BFGS-B', bounds=[(1, 2000), (y_data[0], y_data[0]+0.01), (y_data[-1]-0.019, y_data[-1])])  # R^2 = 0.9955
# result = minimize(objective, initial_guess, method='L-BFGS-B', bounds=[(1, 2000), (None, None), (None, None)])  # R^2 = 0.9979 (najlepsze możliwe)

# Wyniki
if result.success:
    a_opt, y_start_opt, y_end_opt = result.x
    x_start, x_end = x_data[0], x_data[-1]
    def calculate_x0_c(a, y_start, y_end):
        def equation(x0):
            term1 = a * np.cosh((x_start - x0) / a)
            term2 = a * np.cosh((x_end - x0) / a)
            return (y_start - term1) - (y_end - term2)
        sol = root_scalar(equation, bracket=[x_start, x_end], method='brentq')
        x0 = sol.root
        c = y_start - a * np.cosh((x_start - x0) / a)
        return x0, c
    x0_opt, c_opt = calculate_x0_c(a_opt, y_start_opt, y_end_opt)

    # Wygeneruj gęstą siatkę do wykresu
    sort_idx = np.argsort(x_data)
    x_sorted, y_sorted = x_data[sort_idx], y_data[sort_idx]
    x_dense = np.linspace(x_sorted[0], x_sorted[-1], 400)
    y_fit_dense = catenary(x_dense, a_opt, x0_opt, c_opt)
    y_fit_sorted = catenary(x_sorted, a_opt, x0_opt, c_opt)

    # Współczynnik R^2
    ss_res = np.sum((y_sorted - y_fit_sorted) ** 2)
    ss_tot = np.sum((y_sorted - np.mean(y_sorted)) ** 2)
    r_squared = 1 - ss_res / ss_tot
    print(f"Współczynnik R^2: {r_squared:.4f}")

    param_text = (
        f"R² = {r_squared:.4f}\n\n"
        f"Parametry optymalne:\n"
        f"a = {a_opt:.3f}\n"
        f"P_opt = {y_start_opt:.3f} m\n"
        f"K_opt = {y_end_opt:.3f} m\n"
        f"c = {c_opt:.3f} m\n"
        f"x0 = {x0_opt:.3f} m\n"
        f"h_min = {catenary(x0_opt, a_opt, x0_opt, c_opt):.3f} m"
    )

    plt.figure(figsize=(10, 6))
    plt.plot(x_sorted, y_sorted, 'o', label='Dane pomiarowe')
    plt.plot(x_dense, y_fit_dense, '-', label='Dopasowana krzywa łańcuchowa', linewidth=1.5)
    plt.xlabel('Odległość od punktu początkowego liny [m]')
    plt.ylabel('Wysokość [m]')
    plt.title('Dopasowanie krzywej łańcuchowej do danych pomiarowych')
    plt.ylim(bottom=0)
    plt.legend()
    plt.grid(True)
    plt.gcf().text(
        0.72, 0.15, param_text,
        fontsize=10, bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray')
    )
    plt.savefig("katenoida.png", dpi=600)
    plt.show()
    print(f"Parametry optymalne:\na = {a_opt:.3f}\nP_opt = {y_start_opt:.3f} m\nK_opt = {y_end_opt:.3f} m\n"
          f"c = {c_opt:.3f} m\nx0 = {x0_opt:.3f} m\nh_min = {catenary(x0_opt, a_opt, x0_opt, c_opt):.3f} m")
else:
    raise ValueError("Optymalizacja nie powiodła się")

print(h_data)