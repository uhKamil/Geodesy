import numpy as np
from wyrownanie import wyrownanie_mnk

xA, yA, xB, yB, xC, yC = 150, 150, 250, 350, 50, 280
d1, d2, d3 = 100.59, 127.63, 127.59

dAC = np.sqrt((xC - xA) ** 2 + (yC - yA) ** 2)
dBC = np.sqrt((xC - xB) ** 2 + (yC - yB) ** 2)
print(f"dAC = {dAC} m, dBC = {dBC} m")

A_AC = np.arctan2(yC - yA, xC - xA) * 200 / np.pi
A_CA = A_AC + 200
A_BC = np.arctan2(yC - yB, xC - xB) * 200 / np.pi + 400
A_CB = A_BC - 200
print(f"A_AC = {A_AC}g, A_CA = {A_CA}g, A_BC = {A_BC}g, A_CB = {A_CB}g")

alpha = np.arccos((d1 ** 2 + dAC ** 2 - d3 ** 2) / (2 * d1 * dAC)) * 200 / np.pi
beta = np.arccos((d2 ** 2 + dBC ** 2 - d3 ** 2) / (2 * d2 * dBC)) * 200 / np.pi
delta = np.arccos((dAC ** 2 + d3 ** 2 - d1 ** 2) / (2 * dAC * d3)) * 200 / np.pi
print(f"alpha = {alpha}g, beta = {beta}g, delta = {delta}g")

A_AP, A_BP, A_CP = A_AC - alpha, A_BC + beta, A_CA + delta
print(f"A_AP = {A_AP}g, A_BP = {A_BP}g, A_CP = {A_CP}g")

xP0_AP = xA + d1 * np.cos(A_AP * np.pi / 200)
xP0_BP = xB + d2 * np.cos(A_BP * np.pi / 200)
xP0_CP = xC + d3 * np.cos(A_CP * np.pi / 200)
xP0 = 1 / 3 * (xP0_AP + xP0_BP + xP0_CP)
print(f"xP0_AP = {xA} + {d1}cos({A_AP}g) = {xP0_AP}\n"
      f"xP0_BP = {xB} + {d2}cos({A_BP}g) = {xP0_BP}\n"
      f"xP0_CP = {xC} + {d3}cos({A_CP}g) = {xP0_CP}\n"
      f"xP0 = | średnia | = {xP0} m")

yP0_AP = yA + d1 * np.sin(A_AP * np.pi / 200)
yP0_BP = yB + d2 * np.sin(A_BP * np.pi / 200)
yP0_CP = yC + d3 * np.sin(A_CP * np.pi / 200)
yP0 = 1 / 3 * (yP0_AP + yP0_BP + yP0_CP)
print(f"yP0_AP = {yA} + {d1}sin({A_AP}g) = {yP0_AP}\n"
      f"yP0_BP = {yB} + {d2}sin({A_BP}g) = {yP0_BP}\n"
      f"yP0_CP = {yC} + {d3}sin({A_CP}g) = {yP0_CP}\n"
      f"yP0 = | średnia | = {yP0} m")
d_xAP0, d_yAP0 = xP0_AP - xA, yP0_AP - yA
d_AP0 = d1_0 = np.sqrt(d_xAP0 ** 2 + d_yAP0 ** 2)
print(f"∆xAP0 = {xP0_AP} - {xA} = {d_xAP0}\n"
      f"∆yAP0 = {yP0_AP} - {yA} = {d_yAP0}\n"
      f"dAP0 = {d_AP0} = d1_0")

d_xBP0, d_yBP0 = xP0_BP - xB, yP0_BP - yB
d_BP0 = d2_0 = np.sqrt(d_xBP0 ** 2 + d_yBP0 ** 2)
print(f"∆xBP0 = {xP0_BP} - {xB} = {d_xBP0}\n"
      f"∆yBP0 = {yP0_BP} - {yB} = {d_yBP0}\n"
      f"dBP0 = {d_BP0} = d2_0")

d_xCP0, d_yCP0 = xP0_CP - xC, yP0_CP - yC
d_CP0 = d3_0 = np.sqrt(d_xCP0 ** 2 + d_yCP0 ** 2)
print(f"∆xCP0 = {xP0_CP} - {xC} = {d_xCP0}\n"
      f"∆yCP0 = {yP0_CP} - {yC} = {d_yCP0}\n"
      f"dCP0 = {d_CP0} = d3_0")

# Macierze A, L
A = np.array([[-d_xAP0 / d_AP0, -d_yAP0 / d_AP0],
              [-d_xBP0 / d_BP0, -d_yBP0 / d_BP0],
              [-d_xCP0 / d_CP0, -d_yCP0 / d_CP0]])
print(f"A = {A}")

L = np.array([[d1 - d1_0],
              [d2 - d2_0],
              [d3 - d3_0]])
print(f"L = {L} [m]")

# Macierz wag
P = np.diag([.03 ** -2, .02 ** -2, .01 ** -2])
print(f"P = {P} [m^-2]")

wyrownanie_mnk(A, L, P)
