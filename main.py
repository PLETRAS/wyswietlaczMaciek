from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button

from ui import MainUI, ShapeWidget
from data_handler import DataReader

Config.set('graphics', 'fullscreen', '0')


class SpeedometerScreen(Screen):
    def __init__(self, data_reader, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.name = 'speedometer'
        self.add_widget(MainUI(data_reader, screen_manager))


class DummyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'dummy'
        self.add_widget(Label(text="To jest inny ekran"))


class DummyScreen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'dummy2'
        self.add_widget(Label(text="To jest 2 ekran"))


class DummyScreen3(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'dummy3'

        self.layout = BoxLayout(orientation='horizontal', spacing=50, padding=50)
        self.left_shape = ShapeWidget()
        self.right_shape = ShapeWidget()
        self.layout.add_widget(self.left_shape)
        self.layout.add_widget(Widget())  # puste miejsce na środku
        self.layout.add_widget(self.right_shape)

        self.add_widget(self.layout)

    def on_up(self):
        self.left_shape.next_shape()

    def on_down(self):
        self.right_shape.next_shape()


class RootLayout(BoxLayout):
    def __init__(self, reader, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        self.start_x = None
        self.start_y = None

        self.screen_manager = ScreenManager()
        self.speedo_screen = SpeedometerScreen(reader, self.screen_manager)
        self.screen_manager.add_widget(self.speedo_screen)
        self.screen_manager.add_widget(DummyScreen())
        self.screen_manager.add_widget(DummyScreen2())
        self.dummy3 = DummyScreen3()
        self.screen_manager.add_widget(self.dummy3)

        self.screens = ['speedometer', 'dummy', 'dummy2', 'dummy3']

        self.add_widget(self.screen_manager)
        self.create_navigation_buttons()

        self.screen_manager.bind(current=self.update_nav_buttons)
        self.update_nav_buttons(self.screen_manager, self.screen_manager.current)

    def create_navigation_buttons(self):
        self.button_layout = BoxLayout(size_hint_y=0.1)

        self.left_button = Button(text="◀️", on_press=self.go_left)
        self.up_button = Button(text="▲", on_press=self.go_up)
        self.down_button = Button(text="▼", on_press=self.go_down)
        self.right_button = Button(text="▶️", on_press=self.go_right)

        self.button_layout.add_widget(self.left_button)
        self.button_layout.add_widget(self.up_button)
        self.button_layout.add_widget(self.down_button)
        self.button_layout.add_widget(self.right_button)

        self.add_widget(self.button_layout)

    def update_nav_buttons(self, instance, value):
        if value == 'dummy3':
            self.up_button.disabled = False
            self.down_button.disabled = False
            self.up_button.opacity = 1
            self.down_button.opacity = 1
        else:
            self.up_button.disabled = True
            self.down_button.disabled = True
            self.up_button.opacity = 0
            self.down_button.opacity = 0

    def go_left(self, instance):
        current = self.screen_manager.current
        idx = self.screens.index(current)
        idx = (idx - 1) % len(self.screens)
        self.screen_manager.transition = SlideTransition(direction='right')
        self.screen_manager.current = self.screens[idx]

    def go_right(self, instance):
        current = self.screen_manager.current
        idx = self.screens.index(current)
        idx = (idx + 1) % len(self.screens)
        self.screen_manager.transition = SlideTransition(direction='left')
        self.screen_manager.current = self.screens[idx]

    def go_up(self, instance):
        if self.screen_manager.current == 'dummy3':
            self.dummy3.on_up()

    def go_down(self, instance):
        if self.screen_manager.current == 'dummy3':
            self.dummy3.on_down()

    # --- GESTY DOTYKU ---
    def on_touch_down(self, touch):
        self.start_x = touch.x
        self.start_y = touch.y
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        dx = touch.x - self.start_x
        dy = touch.y - self.start_y
        threshold = 50  # minimalna odległość, by uznać za gest

        if abs(dx) > abs(dy) and abs(dx) > threshold:
            if dx > 0:
                self.go_left(None)   # swipe w prawo
            else:
                self.go_right(None)  # swipe w lewo
        elif abs(dy) > abs(dx) and abs(dy) > threshold:
            if dy > 0:
                self.go_down(None)   # swipe w dół
            else:
                self.go_up(None)     # swipe w górę

        return super().on_touch_up(touch)


class CarApp(App):
    def build(self):
        self.reader = DataReader()
        self.reader.start()
        return RootLayout(self.reader)

    def on_stop(self):
        self.reader.stop()


if __name__ == '__main__':
    CarApp().run()
