from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.core.text import Label as CoreLabel
from math import radians, cos, sin
from data_handler import DataReader


class SpeedometerWidget(Widget):
    def __init__(self, **kwargs):
        size = kwargs.pop('size', (300, 300))
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = size
        self.speed = 0
        Clock.schedule_interval(self.update, 1 / 30)
        self.bind(pos=self.update, size=self.update)

    def set_speed(self, speed):
        self.speed = max(0, min(200, speed))

    def update(self, *args):
        self.canvas.clear()
        cx = self.x + self.width / 2
        cy = self.y + self.height / 2
        radius = min(self.width, self.height) / 2 * 0.9

        with self.canvas:
            # tło tarczy
            Color(0, 0, 0)
            Ellipse(pos=(cx - radius, cy - radius), size=(2 * radius, 2 * radius))

            # obręcz
            Color(0.7, 0.7, 0.7)
            Line(circle=(cx, cy, radius), width=3)

            # podziałki i liczby
            steps = 10
            start_angle = 225
            end_angle = 135
            total_angle = 360 - (start_angle - end_angle)

            for i in range(steps + 1):
                angle_deg = start_angle - i * (total_angle / steps)
                angle_rad = radians(angle_deg)
                inner = radius * 0.8
                outer = radius * 0.9
                x1 = cx + inner * cos(angle_rad)
                y1 = cy + inner * sin(angle_rad)
                x2 = cx + outer * cos(angle_rad)
                y2 = cy + outer * sin(angle_rad)

                Color(1, 1, 1)
                Line(points=[x1, y1, x2, y2], width=2)

                # liczby
                value = i * 20
                label = CoreLabel(text=str(value), font_size=20)
                label.refresh()
                tw, th = label.texture.size
                tx = cx + (radius * 0.65) * cos(angle_rad) - tw / 2
                ty = cy + (radius * 0.65) * sin(angle_rad) - th / 2
                Rectangle(texture=label.texture, pos=(tx, ty), size=label.texture.size)

            # wskazówka
            speed_angle_deg = start_angle - (self.speed / 200) * total_angle
            speed_angle_rad = radians(speed_angle_deg)
            length = radius * 0.75
            x_end = cx + length * cos(speed_angle_rad)
            y_end = cy + length * sin(speed_angle_rad)

            Color(1, 0, 0)
            Line(points=[cx, cy, x_end, y_end], width=4)

            # środek tarczy
            Color(0.7, 0.7, 0.7)
            Ellipse(pos=(cx - 12, cy - 12), size=(24, 24))


class MainUI(GridLayout):
    def __init__(self, data_reader, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.reader = data_reader
        self.screen_manager = screen_manager

        # Dwa prędkościomierze obok siebie
        row = BoxLayout(orientation='horizontal', spacing=20)
        self.speedo1 = SpeedometerWidget(size=(200, 200))
        self.speedo2 = SpeedometerWidget(size=(200, 200))
        row.add_widget(self.speedo1)
        row.add_widget(self.speedo2)
        self.add_widget(row)

        # Aktualizacja co 1/30s
        Clock.schedule_interval(self.update_data, 1 / 30)

    def update_data(self, dt):
        speed = getattr(self.reader, 'speed', 0)
        self.speedo1.set_speed(speed)
        self.speedo2.set_speed(speed / 2)


   
        
class ShapeWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.shape_state = 0  # 0=triangle, 1=square, 2=circle
        self.bind(pos=self.redraw, size=self.redraw)
        self.redraw()

    def redraw(self, *args):
        self.canvas.clear()
        cx, cy = self.center
        size = min(self.width, self.height) * 0.6
        with self.canvas:
            Color(0.2, 0.6, 0.8)  # kolor kształtu

            if self.shape_state == 0:
                # trójkąt skierowany w górę (linia zamknięta)
                points = [
                    cx, cy + size / 2,
                    cx - size / 2, cy - size / 2,
                    cx + size / 2, cy - size / 2,
                ]
                Line(points=points + points[:2], width=2, close=True)
            elif self.shape_state == 1:
                # kwadrat
                Rectangle(pos=(cx - size / 2, cy - size / 2), size=(size, size))
            elif self.shape_state == 2:
                # koło
                Ellipse(pos=(cx - size / 2, cy - size / 2), size=(size, size))

    def next_shape(self):
        self.shape_state = (self.shape_state + 1) % 3
        self.redraw()

    def prev_shape(self):
        self.shape_state = (self.shape_state - 1) % 3
        self.redraw()
