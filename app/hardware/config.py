GPIO_CONFIG = {
    'LEFT_IN1': 69,    # GPIO69 (PC5) - ШИМ
    'LEFT_IN2': 70,    # GPIO70 (PC6)
    'RIGHT_IN1': 72,   # GPIO72 (PC8) - ШИМ
    'RIGHT_IN2': 73,   # GPIO73 (PC9)
    'STBY_PIN': 79,    # GPIO79 (PC15) - standby
    'LEFT_ABS': 226,   # GPIO226 (TXD5) - Энкодер левого мотора
    'RIGHT_ABS': 227,  # GPIO227 (RXD5) - Энкодер правого мотора
}

WHEEL_DIAMETER_MM = 64
WHEEL_CIRCUMFERENCE_M = 3.14159 * WHEEL_DIAMETER_MM / 1000

# Параметры энкодера
IMPULSES_PER_REVOLUTION = 20

# Настройки ШИМ
PWM_FREQUENCY = 10000

# Настройки обновления данных
UPDATE_INTERVAL = 0.5  # секунды
ENCODER_UPDATE_INTERVAL = 0.05  # секунды