from manim import *
import numpy as np

# Dane wejściowe
m_x2 = 7.688248e-4
m_y2 = 2.594801e-4
m_xy = -8.659253e-5

# Obliczenie kąta phi
phi = 0.5 * np.arctan((2 * m_xy) / (m_x2 - m_y2))
if phi < 0:
    phi += np.pi

# Długości półosi elipsy
m_max = np.sqrt(m_x2 * np.cos(phi) ** 2 + m_xy * np.sin(2 * phi) + m_y2 * np.sin(phi) ** 2)
m_min = np.sqrt(
    m_x2 * np.cos(phi + np.pi / 2) ** 2 + m_xy * np.sin(2 * (phi + np.pi / 2)) + m_y2 * np.sin(phi + np.pi / 2) ** 2)
if m_min > m_max:
    m_min, m_max = m_max, m_min

# Macierz rotacji
R = np.array([[np.cos(phi), -np.sin(phi)], [np.sin(phi), np.cos(phi)]])


class ErrorEllipseAnimation(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        # Oś współrzędnych
        axes = Axes(x_range=[-0.08, 0.08, 0.01], y_range=[-0.08, 0.08, 0.01], axis_config={"color": BLACK}, x_length = 6, y_length = 6)
        grid = NumberPlane(axis_config={"color": BLACK}, background_line_style={"stroke_color": DARK_GREY, "stroke_width": 1})
        self.play(Create(grid), run_time=1)

        # Funkcja pisania azymutu
        azimuth_text = Text(f"Azymut: {phi * 200/np.pi}g", color=BLACK).scale(0.5).to_corner(UP + RIGHT)
        def update_azimuth(mob, alpha):
            # for i, angle in enumerate(np.linspace(phi*200/np.pi, phi*200/np.pi+400, 50)):
            #     if angle >= 400:
            #         angle -= 400
            #     mob.become(Text(f"Azymut: {angle:.4f}g").scale(0.5).to_corner(UP + RIGHT))
                # self.wait(3/50)
            angle = phi * 200/np.pi + alpha * 400
            if angle >= 400:
                angle -= 400
            mob.become(Text(f"Azymut: {angle:.4f}g", color=BLACK).scale(0.5).to_corner(UP + RIGHT))
        def update_azimuth_2(mob, alpha):
            angle = alpha * 400
            mob.become(Text(f"Azymut: {angle:.4f}g", color=BLACK).scale(0.5).to_corner(UP + RIGHT))


        # Tworzenie elipsy błędu średniego
        t = np.linspace(0, 2 * np.pi, 100)
        ellipse_x = m_max * np.cos(t)
        ellipse_y = m_min * np.sin(t)
        rotated_ellipse = R @ np.array([ellipse_x, ellipse_y])
        rotated_ellipse_swapped = np.array([rotated_ellipse[1], rotated_ellipse[0]])
        ellipse_points = [axes.c2p(x, y) for x, y in zip(rotated_ellipse_swapped[0], rotated_ellipse_swapped[1])]
        ellipse = VMobject().set_points_smoothly(ellipse_points).set_color("#1f77b4")  # jasnoniebieski
        title_text = Text(f"Elipsa błędu średniego", color=BLACK).scale(0.75).to_corner(UP + LEFT)
        self.play(Write(title_text), run_time=0.5)
        self.play(AnimationGroup(Create(ellipse), UpdateFromAlphaFunc(azimuth_text, update_azimuth)), run_time=3)
        self.play(FadeOut(azimuth_text, title_text))
        self.wait(0.3)

        # Animacja rysowania krzywej błędu średniego
        a, b = m_max, m_min
        azimuths = np.linspace(0, 2 * np.pi, 100)
        r_error = np.sqrt((a ** 2 * np.cos(azimuths - phi) ** 2) + (b ** 2 * np.sin(azimuths - phi) ** 2))
        x_error = r_error * np.cos(azimuths)
        y_error = r_error * np.sin(azimuths)
        error_curve_points = [axes.c2p(x, y) for x, y in zip(y_error, x_error)]
        error_curve = VMobject().set_points_smoothly(error_curve_points).set_color("#0000ff")  # granatowy
        title_text = Text(f"Krzywa błędu średniego", color=BLACK).scale(0.75).to_corner(UP + LEFT)
        self.play(Write(title_text), run_time=0.5)
        self.play(AnimationGroup(Create(error_curve), UpdateFromAlphaFunc(azimuth_text, update_azimuth_2)), run_time=3)
        self.play(FadeOut(azimuth_text, title_text))
        self.wait(0.3)

        # Elipsy ufności
        scaling_86, scaling_99 = 1.83, 2.58
        xy_rotated_86 = R @ np.array([scaling_86 * a * np.cos(t), scaling_86 * b * np.sin(t)])
        xy_rotated_99 = R @ np.array([scaling_99 * a * np.cos(t), scaling_99 * b * np.sin(t)])
        title_text = Text(f"Elipsa ufności 86%", color=BLACK).scale(0.75).to_corner(UP + LEFT)
        title_text_2 = Text(f"Elipsa ufności 99%", color=BLACK).scale(0.75).to_corner(UP + LEFT)
        ellipse_86 = VMobject().set_points_smoothly(
            [axes.c2p(x, y) for x, y in zip(xy_rotated_86[1], xy_rotated_86[0])]).set_color("#ffa500")  # pomarańczowy
        ellipse_99 = VMobject().set_points_smoothly(
            [axes.c2p(x, y) for x, y in zip(xy_rotated_99[1], xy_rotated_99[0])]).set_color("#ff0000")  # czerwony

        self.play(Write(title_text), run_time=0.5)
        self.play(AnimationGroup(Create(ellipse_86), UpdateFromAlphaFunc(azimuth_text, update_azimuth)), run_time=3)
        self.play(FadeOut(azimuth_text, title_text))
        self.wait(0.3)
        self.play(Write(title_text_2), run_time=0.5)
        self.play(AnimationGroup(Create(ellipse_99), UpdateFromAlphaFunc(azimuth_text, update_azimuth)), run_time=3)
        self.play(FadeOut(azimuth_text, title_text_2))
        self.wait(0.3)
        self.wait(3.7)
