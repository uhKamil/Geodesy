"""
Chciałem w tym kodzie wygenerować sobie wartości dla różnych kątów, żeby móc narysować tą krzywą błędu średniego
"""

import numpy as np

# Dane wejściowe (wariancje i kowariancja)
m_x2 = 7.688248e-4  # Wariancja w osi X
m_y2 = 2.594801e-4  # Wariancja w osi Y
m_xy = -8.659253e-5  # Kowariancja

for phi in range(0, 200, 10):
    m = np.sqrt(m_x2*np.cos(phi*np.pi/200)**2 + m_xy*np.sin(2*(phi*np.pi/200)) + m_y2 * np.sin(phi*np.pi/200)**2)
    if phi <= 100:
        stopnie = 100-phi
    elif phi <= 200:
        stopnie = 300-phi
    print(f"Wartość błędu dla kąta {phi}g: {m*100:.2f} cm, aby narysować w Goodnotes: {(1.105/0.75)*100*m:.2f} cm, kąt w stopniach ustaw na {stopnie*180/200}")

print(f"\n ELIPSA BŁĘDU ŚREDNIEGO\n")

# Elipsa błędu średniego
def r(phi, a, b, theta):
    return (a * b) / np.sqrt((b * np.cos((phi - theta)*np.pi/200))**2 + (a * np.sin((phi - theta)*np.pi/200))**2)


for p in range(0, 200, 10):
    if p <= 100:
        stopnie = 100-p
    elif p <= 200:
        stopnie = 300-p
    x = r(189.56732226626625, 0.02798470356851064, 0.015657625088012227, p)
    print(f"Wartość błędu dla kąta {p}g: {x*100:.2f} cm, aby narysować w Goodnotes: {(1.105/0.75)*100*x:.2f} cm, kąt w stopniach ustaw na {stopnie*180/200}")


# Elipsa ufności 86%
print(f"\n ELIPSA UFNOŚCI 86%\n")
for p in range(0, 200, 10):
    if p <= 100:
        stopnie = 100-p
    elif p <= 200:
        stopnie = 300-p
    x = r(189.56732226626625, 0.02798470356851064*np.sqrt(4.429), 0.015657625088012227*np.sqrt(4.429), p)
    print(f"Wartość błędu dla kąta {p}g: {x*100:.2f} cm, aby narysować w Goodnotes: {(1.105/1)*100*x:.2f} cm, kąt w stopniach ustaw na {stopnie*180/200}")

# Elipsa ufności 99%
print(f"\n ELIPSA UFNOŚCI 99%\n")
for p in range(0, 200, 10):
    if p <= 100:
        stopnie = 100-p
    elif p <= 200:
        stopnie = 300-p
    x = r(189.56732226626625, 0.02798470356851064*np.sqrt(9.210), 0.015657625088012227*np.sqrt(9.210), p)
    print(f"Wartość błędu dla kąta {p}g: {x*100:.2f} cm, aby narysować w Goodnotes: {(1.105/1.5)*100*x:.2f} cm, kąt w stopniach ustaw na {stopnie*180/200}")