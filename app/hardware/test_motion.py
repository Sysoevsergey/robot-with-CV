import time
from speed_monitor import SpeedMonitor


class TestMotion:
    def __init__(self, motor_controller, encoder_reader):
        self.motor_controller = motor_controller
        self.encoder_reader = encoder_reader
        self.speed_monitor = SpeedMonitor(encoder_reader)

        print("test_runner запущен")

    def forward_test(self, power=50, duration=5):
        print(f"\n\ДВИЖЕНИЯ ВПЕРЕД {power}%")
        print(f"Длительность: {duration} секунд")

        self.motor_controller.set_motors(power, power)
        time.sleep(duration)
        self.motor_controller.set_motors(0, 0)

        print("завершен\n")

    def backward_test(self, power=40, duration=3):
        print(f"\nДВИЖЕНИЯ НАЗАД {power}%")
        print(f"Длительность: {duration} секунд")

        self.motor_controller.set_motors(-power, -power)
        time.sleep(duration)
        self.motor_controller.set_motors(0, 0)

        print("завершен\n")

    def turn_right_test(self, left_power=40, right_power=10, duration=3):
        print(f"\nПОВОРОТ НАПРАВО")
        print(f"Левый: {left_power}%, Правый: {right_power}%")
        print(f"Длительность: {duration} секунд")

        self.motor_controller.set_motors(left_power, right_power)
        time.sleep(duration)
        self.motor_controller.set_motors(0, 0)

        print("завершен\n")

    def turn_left_test(self, left_power=10, right_power=40, duration=3):
        print(f"\nТЕСТ ПОВОРОТА НАЛЕВО")
        print(f"Левый: {left_power}%, Правый: {right_power}%")
        print(f"Длительность: {duration} секунд")

        self.motor_controller.set_motors(left_power, right_power)
        time.sleep(duration)
        self.motor_controller.set_motors(0, 0)

        print("завершен\n")

    def run_all_tests(self):
        print("ЗАПУСК ВСЕХ ТЕСТОВ")

        # ожидание для инициализации
        time.sleep(1)

        # вперед на 30%
        self.forward_test(30, 3)
        time.sleep(1)

        # вперед на 60%
        self.forward_test(60, 3)
        time.sleep(1)

        # назад
        self.backward_test(40, 3)
        time.sleep(1)

        # поворот направо
        self.turn_right_test(40, 10, 3)
        time.sleep(1)

        # поворот налево
        self.turn_left_test(10, 40, 3)

        print("\nзавершен")

    def stop(self):
        self.speed_monitor.stop()
        print("test_motion остановлен")
