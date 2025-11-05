import numpy as np
import matplotlib.pyplot as plt

## ELIPSA BŁĘDU ŚREDNIEGO ##
# Dane wejściowe (wariancje i kowariancja)
m_x2 = 7.688248e-4  # Wariancja w osi X
m_y2 = 2.594801e-4  # Wariancja w osi Y
m_xy = -8.659253e-5  # Kowariancja

# Obliczenie kąta phi, o który potencjalnie będzie obrócona elipsa (bądź o phi + pi/2 rad)
phi = 0.5 * np.arctan((2 * m_xy) / (m_x2 - m_y2))
if phi < 0:
    phi += np.pi
print(f"phi = {phi*(200/np.pi)}g = {phi} rad")


# Długości półosi elipsy błędu średniego
m_max = np.sqrt(m_x2*np.cos(phi)**2 + m_xy*np.sin(2*phi) + m_y2 * np.sin(phi)**2)
print(f"m_max = {m_max} m")
m_min = np.sqrt(m_x2*np.cos(phi+np.pi/2)**2 + m_xy*np.sin(2*(phi+np.pi/2)) + m_y2 * np.sin(phi+np.pi/2)**2)
print(f"m_min = {m_min} m")

if m_min > m_max:
    m_min, m_max = m_max, m_min

# Tworzenie punktów elipsy w standardowym układzie
t = np.linspace(0, 2 * np.pi, 100)
ellipse_x = m_max * np.cos(t)
ellipse_y = m_min * np.sin(t)

# Macierz rotacji
R = np.array([[np.cos(phi), -np.sin(phi)],
              [np.sin(phi),  np.cos(phi)]])

# Obrót elipsy o azymut
rotated_ellipse = R @ np.array([ellipse_x, ellipse_y])

# Zamiana osi X i Y
rotated_ellipse_swapped = np.array([rotated_ellipse[1], rotated_ellipse[0]])

# Rysowanie wykresu z zamienionymi osiami
plt.figure(figsize=(6, 6))
plt.plot(rotated_ellipse_swapped[0], rotated_ellipse_swapped[1])
plt.quiver(0, 0, m_max * np.sin(phi), m_max * np.cos(phi), angles='xy', scale_units='xy', scale=1, color='r', label="Półoś wielka")
plt.quiver(0, 0, m_min * np.sin(phi - np.pi / 2), m_min * np.cos(phi - np.pi / 2), angles='xy', scale_units='xy', scale=1, color='b', label="Półoś mała")
plt.axhline(0, color='gray', linestyle='-', linewidth=0.5)
plt.axvline(0, color='gray', linestyle='-', linewidth=0.5)
plt.legend(loc='upper right')
plt.xlabel("Y [m]")
plt.ylabel("X [m]")
plt.title("Elipsa błędu średniego")
plt.axis("equal")  # Równe proporcje osi
plt.tight_layout()
plt.savefig("elipsa_bledu.png", dpi=600, bbox_inches='tight')
plt.show()

## KRZYWA BŁĘDU ŚREDNIEGO ##
a = m_max
b = m_min

# Generowanie wartości azymutu
azimuths = np.linspace(0, 2*np.pi, 100)

# Wzór na błąd w funkcji azymutu (parametryczna krzywa błędu średniego)
r_error = np.sqrt((a**2 * np.cos(azimuths - phi)**2) + (b**2 * np.sin(azimuths - phi)**2))

# Współrzędne biegunowe -> kartezjańskie (trzeba zamienić przy plot)
x_error = r_error * np.cos(azimuths)
y_error = r_error * np.sin(azimuths)

# Tworzenie wykresu krzywej błędu średniego
plt.figure(figsize=(6, 6))
plt.plot(y_error, x_error, label="Krzywa błędu średniego", color="blue")

# Osie układu
plt.axhline(0, color='gray', linestyle='--', linewidth=0.5)
plt.axvline(0, color='gray', linestyle='--', linewidth=0.5)

# Ustawienia wykresu
plt.xlabel("Y [m]")
plt.ylabel("X [m]")
plt.title("Krzywa błędu średniego")
plt.axis('equal')
plt.grid(True)
plt.tight_layout()

# Wyświetlenie wykresu
plt.savefig("krzywa_bledu.png", dpi=600, bbox_inches='tight')
plt.show()

## ELIPSY UFNOŚCI ##
# Współczynniki skalowania dla elipsy ufności (odpowiednie wartości z tabeli rozkładu chi-kwadrat)
scaling_86 = np.sqrt(4.429)  # Współczynnik dla 86% poziomu ufności, dokładnie musi to być pierwiastek dla tego poziomu ufności z 2 stopniami swobody
scaling_99 = np.sqrt(9.210)  # Współczynnik dla 99% poziomu ufności

# Generowanie punktów dla elipsy ufności
x_86 = scaling_86 * a * np.cos(t)
y_86 = scaling_86 * b * np.sin(t)

x_99 = scaling_99 * a * np.cos(t)
y_99 = scaling_99 * b * np.sin(t)

# Obrót elipsy
xy_rotated_86 = R @ np.array([x_86, y_86])
xy_rotated_99 = R @ np.array([x_99, y_99])

# Tworzenie wykresu elipsy ufności (zamienione osie)
plt.figure(figsize=(6, 6))
plt.plot(xy_rotated_86[1], xy_rotated_86[0], label="Elipsa ufności 86%", color="orange")
plt.plot(xy_rotated_99[1], xy_rotated_99[0], label="Elipsa ufności 99%", color="red")

# Osie układu
plt.axhline(0, color='gray', linestyle='--', linewidth=0.5)
plt.axvline(0, color='gray', linestyle='--', linewidth=0.5)

# Ustawienia wykresu
plt.xlabel("Y [m]")
plt.ylabel("X [m]")
plt.title("Elipsy ufności dla poziomów ufności 0,86 i 0,99")
plt.axis('equal')
plt.legend(loc='upper right')
plt.grid(True)
plt.tight_layout()

# Wyświetlenie wykresu
plt.savefig("elipsa_ufnosci.png", dpi=600, bbox_inches='tight')
plt.show()


## WYKRES ZBIORCZY ##
plt.figure(figsize=(6, 6))
plt.plot(rotated_ellipse_swapped[0], rotated_ellipse_swapped[1], label="Elipsa błędu średniego")
plt.plot(y_error, x_error, label="Krzywa błędu średniego", color="blue")
plt.plot(xy_rotated_86[1], xy_rotated_86[0], label="Elipsa ufności 86%", color="orange")
plt.plot(xy_rotated_99[1], xy_rotated_99[0], label="Elipsa ufności 99%", color="red")
plt.axhline(0, color='gray', linestyle='-', linewidth=0.5)
plt.axvline(0, color='gray', linestyle='-', linewidth=0.5)
plt.legend(loc='upper right')
plt.xlabel("Y [m]")
plt.ylabel("X [m]")
plt.title("Wykres zbiorczy")
plt.axis("equal")
plt.tight_layout()
plt.savefig("wykres_zbiorczy.png", dpi=600, bbox_inches='tight')
plt.show()