from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config

from ui import MainUI, SpeedometerWidget
from data_handler import DataReader

Config.set('graphics', 'fullscreen', '0')  # 0 - okno, 1 - fullscreen

class CarApp(App):
    def build(self):
        self.reader = DataReader()
        self.reader.start()

        # Tworzymy speedometer i dodajemy go do UI albo sam widget na start
        self.speedometer = SpeedometerWidget()
        
        # Aktualizacja prędkości co 1/30 sekundy (możesz zmienić)
        Clock.schedule_interval(self.update_speed, 1/30)

        return self.speedometer

    def update_speed(self, dt):
        # Pobierz prędkość z readera (np. reader.speed)
        # Zakładam, że DataReader ma atrybut speed z prędkością w zakresie 0-200
        speed = getattr(self.reader, 'speed', 0)  
        self.speedometer.set_speed(speed)

    def on_stop(self):
        self.reader.stop()  # zatrzymaj wątek lub czyść zasoby, jeśli masz taką metodę

if __name__ == '__main__':
    CarApp().run()
