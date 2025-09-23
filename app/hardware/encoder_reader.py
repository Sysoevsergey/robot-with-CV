import time
import threading
from config import GPIO_CONFIG, WHEEL_CIRCUMFERENCE_M, IMPULSES_PER_REVOLUTION, ENCODER_UPDATE_INTERVAL


class EncoderReader:
    def __init__(self, motor_controller):
        self.motor_controller = motor_controller
        self.left_speed_kmh = 0.0
        self.right_speed_kmh = 0.0
        self.left_rpm = 0.0
        self.right_rpm = 0.0
        self.data_lock = threading.Lock()
        self.stop_threads = False

        # запуск потоков для чтения энкодеров
        self.left_encoder_thread = threading.Thread(target=self._left_encoder_loop)
        self.left_encoder_thread.daemon = True

        self.right_encoder_thread = threading.Thread(target=self._right_encoder_loop)
        self.right_encoder_thread.daemon = True

        self.left_encoder_thread.start()
        self.right_encoder_thread.start()

        print("encoder_reader запущен")

    def _left_encoder_loop(self):
        position = 0
        last_position = 0
        last_time = time.time()
        last_state = self.motor_controller.left_abs_line.get_value()

        while not self.stop_threads:
            current_state = self.motor_controller.left_abs_line.get_value()

            if current_state != last_state:
                position += 1
                last_state = current_state

                current_time = time.time()
                time_diff = current_time - last_time

                if time_diff > ENCODER_UPDATE_INTERVAL:
                    position_diff = position - last_position

                    # Расчет скорости (м/с)
                    distance_m = (position_diff / IMPULSES_PER_REVOLUTION) * WHEEL_CIRCUMFERENCE_M
                    speed_ms = distance_m / time_diff

                    # Конвертация в км/ч
                    speed_kmh = speed_ms * 3.6

                    # Расчет оборотов в минуту (RPM)
                    rps = position_diff / (IMPULSES_PER_REVOLUTION * time_diff)
                    rpm = rps * 60

                    last_position = position
                    last_time = current_time

                    with self.data_lock:
                        self.left_speed_kmh = speed_kmh
                        self.left_rpm = rpm

            time.sleep(0.001)

    def _right_encoder_loop(self):
        position = 0
        last_position = 0
        last_time = time.time()
        last_state = self.motor_controller.right_abs_line.get_value()

        while not self.stop_threads:
            current_state = self.motor_controller.right_abs_line.get_value()

            if current_state != last_state:
                position += 1
                last_state = current_state

                current_time = time.time()
                time_diff = current_time - last_time

                if time_diff > ENCODER_UPDATE_INTERVAL:
                    position_diff = position - last_position

                    # Расчет скорости (м/с)
                    distance_m = (position_diff / IMPULSES_PER_REVOLUTION) * WHEEL_CIRCUMFERENCE_M
                    speed_ms = distance_m / time_diff

                    # Конвертация в км/ч
                    speed_kmh = speed_ms * 3.6

                    # Расчет оборотов в минуту (RPM)
                    rps = position_diff / (IMPULSES_PER_REVOLUTION * time_diff)
                    rpm = rps * 60

                    last_position = position
                    last_time = current_time

                    with self.data_lock:
                        self.right_speed_kmh = speed_kmh
                        self.right_rpm = rpm

            time.sleep(0.001)

    def get_speeds(self):
        with self.data_lock:
            return {
                'left_speed_kmh': self.left_speed_kmh,
                'right_speed_kmh': self.right_speed_kmh,
                'left_rpm': self.left_rpm,
                'right_rpm': self.right_rpm
            }

    def stop(self):
        self.stop_threads = True
        print("encoder_reader остановлен")