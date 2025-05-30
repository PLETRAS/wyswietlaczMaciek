import threading
import time

class DataReader:
    def __init__(self):
        self.counter = 0
        self.speed = 0  # nowy atrybut dla prędkości
        self.latest_value = "Brak danych"
        self._running = True

    def read_loop(self):
        while self._running:
            time.sleep(0.05)
            self.counter += 1
            if self.counter > 200:
                self.counter = 0
            self.speed = self.counter  # aktualizujemy prędkość
            self.latest_value = f"Wartość: {self.counter}"

    def start(self):
        self.thread = threading.Thread(target=self.read_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self._running = False

    def join(self):
        self.thread.join()
