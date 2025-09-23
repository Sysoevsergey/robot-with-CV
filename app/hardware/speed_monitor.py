import time
import threading
from config import UPDATE_INTERVAL


class SpeedMonitor:
    def __init__(self, encoder_reader):
        self.encoder_reader = encoder_reader
        self.stop_threads = False
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()

        print("speed_monitor запущен")

    def _monitor_loop(self):
        while not self.stop_threads:
            speeds = self.encoder_reader.get_speeds()
            print(f"Левый: {speeds['left_speed_kmh']:.2f} км/ч, {speeds['left_rpm']:.1f} об/мин | "
                  f"Правый: {speeds['right_speed_kmh']:.2f} км/ч, {speeds['right_rpm']:.1f} об/мин")
            time.sleep(UPDATE_INTERVAL)

    def stop(self):
        self.stop_threads = True
        print("speed_monitor остановлен")