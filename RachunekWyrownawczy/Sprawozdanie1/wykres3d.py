import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Tworzymy siatkę wartości dla X i Y
y = np.linspace(-5, 5, 100)
z = np.linspace(-5, 5, 100)  # Zmienna wysokości
Y, Z = np.meshgrid(y, z)

# Obliczamy wartości X zgodnie z nierównością
X = np.abs(Y) / np.sqrt(0.85)

# Tworzenie wykresu
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

# Powierzchnie stożków dla dodatnich i ujemnych wartości X
ax.plot_surface(X, Y, Z, color='blue', alpha=0.5)
ax.plot_surface(-X, Y, Z, color='blue', alpha=0.5)

# Poprawienie zakresów osi
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.set_zlim(-5, 5)

# Obrót kamery dla lepszego widoku
ax.view_init(elev=25, azim=30)

# Siatka na osiach dla lepszej czytelności
ax.grid(True)
plt.show()

## WYKRES 2 ##
# Tworzenie siatki 3D
x = np.linspace(-5, 5, 50)
y = np.linspace(-5, 5, 50)
z = np.linspace(-5, 5, 50)
X, Y, Z = np.meshgrid(x, y, z)

# Sprawdzenie warunku nierówności
inside = (0.85 * (X**2 / Y**2)) <= 1

# Tworzenie wykresu
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

# Rysowanie chmury punktów spełniających nierówność
ax.scatter(X[inside], Y[inside], Z[inside], color='blue', alpha=0.1, s=10)

# Ustawienia osi
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.set_zlim(-5, 5)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_title("Wypełniona bryła spełniająca nierówność")

# Obrót kamery
ax.view_init(elev=25, azim=30)

plt.show()


## WYKRES 3 ##
# Tworzenie siatki cylindrycznej (dla stożka)
theta = np.linspace(0, 2 * np.pi, 100)  # Kąt w płaszczyźnie XY
z = np.linspace(-5, 5, 50)  # Wysokość
Theta, Z = np.meshgrid(theta, z)

# Promień stożka w danym punkcie wysokości
R = np.abs(Z) / np.sqrt(0.85)

# Współrzędne X i Y w układzie biegunowym
X = R * np.cos(Theta)
Y = R * np.sin(Theta)

# Tworzenie wykresu
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

# Rysowanie powierzchni stożka z półprzezroczystością i konturami
ax.plot_surface(X, Y, Z, color='blue', alpha=0.3, edgecolor='black')

# Ustawienia osi
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.set_zlim(-5, 5)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_title("Wypełniona bryła z konturami")

# Obrót kamery dla lepszego widoku
ax.view_init(elev=25, azim=30)

plt.show()


## WYKRES 4 ##
# Zakres wartości
y = np.linspace(-5, 5, 100)
z = np.linspace(-5, 5, 100)
Y, Z = np.meshgrid(y, z)

# Obliczamy X na podstawie nierówności
X_max = np.sqrt(Y**2 / 0.85)  # Górna powierzchnia bryły
X_min = -X_max  # Symetryczna dolna część

# Tworzenie wykresu
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

# Powierzchnie graniczne bryły (dwie warstwy)
ax.plot_surface(X_max, Y, Z, color='blue', alpha=0.3, edgecolor='black')
ax.plot_surface(X_min, Y, Z, color='blue', alpha=0.3, edgecolor='black')

# Ustawienia osi
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.set_zlim(-5, 5)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_title("Poprawiona bryła spełniająca nierówność")

# Obrót kamery dla lepszego widoku
ax.view_init(elev=25, azim=30)

plt.show()
