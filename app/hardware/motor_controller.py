import gpiod
import time
import threading
from config import GPIO_CONFIG, PWM_FREQUENCY


class SoftwarePWM:
    def __init__(self, pin, frequency=PWM_FREQUENCY):
        self.pin = pin
        self.frequency = frequency
        self.duty_cycle = 0
        self.running = False

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()

    def _run(self):
        period = 1.0 / self.frequency
        while self.running:
            on_time = period * self.duty_cycle
            off_time = period - on_time
            if on_time > 0:
                self.pin.set_value(1)
                time.sleep(on_time)
            if off_time > 0:
                self.pin.set_value(0)
                time.sleep(off_time)

    def stop(self):
        self.running = False
        self.pin.set_value(0)

    def set_duty_cycle(self, duty_cycle):
        self.duty_cycle = max(0.0, min(1.0, duty_cycle / 100.0))


class MotorController:

    def __init__(self):
        self.chip = gpiod.Chip('gpiochip0')

        self.left_in1 = self.chip.get_line(GPIO_CONFIG['LEFT_IN1'])
        self.left_in2 = self.chip.get_line(GPIO_CONFIG['LEFT_IN2'])
        self.right_in1 = self.chip.get_line(GPIO_CONFIG['RIGHT_IN1'])
        self.right_in2 = self.chip.get_line(GPIO_CONFIG['RIGHT_IN2'])
        self.stby = self.chip.get_line(GPIO_CONFIG['STBY_PIN'])

        self.left_abs_line = self.chip.get_line(GPIO_CONFIG['LEFT_ABS'])
        self.right_abs_line = self.chip.get_line(GPIO_CONFIG['RIGHT_ABS'])

        output_lines = [self.left_in1, self.left_in2, self.right_in1, self.right_in2, self.stby]
        for line in output_lines:
            line.request(consumer="MOTOR", type=gpiod.LINE_REQ_DIR_OUT)

        self.left_abs_line.request(consumer="LEFT_ABS", type=gpiod.LINE_REQ_DIR_IN)
        self.right_abs_line.request(consumer="RIGHT_ABS", type=gpiod.LINE_REQ_DIR_IN)

        self.stby.set_value(1)

        self.pwm_left = SoftwarePWM(self.left_in1)
        self.pwm_right = SoftwarePWM(self.right_in1)

        self.current_left_speed = 0
        self.current_right_speed = 0

        self.pwm_left.start()
        self.pwm_right.start()

        print("motor_controller запущен")

    def set_motors(self, left_speed, right_speed):
        # Ограничение скорости
        left_speed = max(-100, min(100, left_speed))
        right_speed = max(-100, min(100, right_speed))

        # левый мотор
        if left_speed == 0:
            self.left_in2.set_value(0)
            self.pwm_left.set_duty_cycle(0)
        elif left_speed > 0:
            self.left_in2.set_value(0)
            self.pwm_left.set_duty_cycle(left_speed)
        else:
            self.left_in2.set_value(1)
            self.pwm_left.set_duty_cycle(-left_speed)

        # правый мотор
        if right_speed == 0:
            self.right_in2.set_value(0)
            self.pwm_right.set_duty_cycle(0)
        elif right_speed > 0:
            self.right_in2.set_value(0)
            self.pwm_right.set_duty_cycle(right_speed)
        else:
            self.right_in2.set_value(1)
            self.pwm_right.set_duty_cycle(-right_speed)

        # Сохранение текущие скорости
        self.current_left_speed = left_speed
        self.current_right_speed = right_speed

        print(f"Установлена скорость: Левый: {left_speed}%, Правый: {right_speed}%")

    def stop(self):
        self.set_motors(0, 0)
        self.stby.set_value(0)
        self.pwm_left.stop()
        self.pwm_right.stop()

        # Освобождение GPIO
        output_lines = [self.left_in1, self.left_in2, self.right_in1, self.right_in2, self.stby]
        for line in output_lines:
            line.release()

        self.left_abs_line.release()
        self.right_abs_line.release()

        print("motor_controller остановлен")