from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.widget import Widget

from datetime import datetime

from kivy.core.text import Label as CoreLabel

from math import radians, cos, sin, atan2, degrees
from kivy.graphics import Color, Ellipse, Line, Rectangle, PushMatrix, PopMatrix, Rotate





class MainUI(BoxLayout):
    def __init__(self, data_reader, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.label = Label(text="Oczekiwanie na dane...", font_size=48)
        self.add_widget(self.label)

        self.data_reader = data_reader

        Clock.schedule_interval(self.update_data, 0.5)

    def update_data(self, dt):
        self.label.text = self.data_reader.latest_value

    def on_stop(self):
        self.data_reader.stop()
        self.data_reader.join()





class SpeedometerWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (400, 400)
        self.speed = 0  # prędkość od 0 do 200
        Clock.schedule_interval(self.update, 1/30)
        self.bind(pos=self.update, size=self.update)

    def set_speed(self, speed):
        # ograniczamy prędkość do zakresu 0-200
        self.speed = max(0, min(200, speed))

    def update(self, *args):
        self.canvas.clear()

        cx = self.x + self.width / 2
        cy = self.y + self.height / 2
        radius = min(self.width, self.height) / 2 * 0.9

        with self.canvas:
            # Tło tarczy
            Color(0, 0, 0)
            Ellipse(pos=(cx - radius, cy - radius), size=(2*radius, 2*radius))

            # Obręcz tarczy
            Color(0.7, 0.7, 0.7)
            Line(circle=(cx, cy, radius), width=3)

            # Podziałki i cyfry
            # Skala od 135° do 45° (czyli kąt 270°, zostawiając dół puste)
            steps = 10
            start_angle = 135+90  # początek skali w stopniach
            end_angle = 45+90
            total_angle = 360 - (start_angle - end_angle)  # 270 stopni

            for i in range(steps + 1):
                angle_deg = start_angle - i * (total_angle / steps)  # przesuwamy w kierunku zgodnym z ruchem wskazówek
                angle_rad = radians(angle_deg)
                inner = radius * 0.8
                outer = radius * 0.9

                x1 = cx + inner * cos(angle_rad)
                y1 = cy + inner * sin(angle_rad)
                x2 = cx + outer * cos(angle_rad)
                y2 = cy + outer * sin(angle_rad)

                Color(1, 1, 1)
                Line(points=[x1, y1, x2, y2], width=2)

                # Cyfry
                value = i * 20
                label = CoreLabel(text=str(value), font_size=20)
                label.refresh()
                tw, th = label.texture.size
                tx = cx + (radius * 0.65) * cos(angle_rad) - tw / 2
                ty = cy + (radius * 0.65) * sin(angle_rad) - th / 2

                Color(1, 1, 1)
                Rectangle(texture=label.texture, pos=(tx, ty), size=label.texture.size)

            # Wskazówka
            # Kąt wskazówki odpowiada prędkości
            speed_angle_deg = start_angle - (self.speed / 200) * total_angle
            speed_angle_rad = radians(speed_angle_deg)
            length = radius * 0.75

            x_end = cx + length * cos(speed_angle_rad)
            y_end = cy + length * sin(speed_angle_rad)

            Color(1, 0, 0)
            Line(points=[cx, cy, x_end, y_end], width=4, cap='round')

            # Środek tarczy
            Color(0.7, 0.7, 0.7)
            Ellipse(pos=(cx - 12, cy - 12), size=(24, 24))