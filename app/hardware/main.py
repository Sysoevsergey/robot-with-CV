import signal
import sys
from motor_controller import MotorController
from encoder_reader import EncoderReader
from test_motion import TestMotion


MOTOR_CONTROLLER = None
ENCODER_READER = None
TEST_MOTION = None


def signal_handler(sig, frame):
    print("\nПолучен сигнал завершения...")
    shutdown()
    sys.exit(0)


def shutdown():
    global MOTOR_CONTROLLER, ENCODER_READER, TEST_MOTION

    print("Завершение работы системы...")

    if TEST_MOTION:
        TEST_MOTION.stop()

    if ENCODER_READER:
        ENCODER_READER.stop()

    if MOTOR_CONTROLLER:
        MOTOR_CONTROLLER.stop()

    print("Система полностью остановлена")


def main():
    global MOTOR_CONTROLLER, ENCODER_READER, TEST_MOTION

    # Настройка обработчика сигналов
    signal.signal(signal.SIGINT, signal_handler)

    try:
        print("ИНИЦИАЛИЗАЦИЯ УПРАВЛЕНИЯ МОТОРАМИ")

        MOTOR_CONTROLLER = MotorController()
        ENCODER_READER = EncoderReader(MOTOR_CONTROLLER)
        TEST_MOTION = TestMotion(MOTOR_CONTROLLER, ENCODER_READER)

        TEST_MOTION.run_all_tests()

    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        shutdown()


if __name__ == "__main__":
    main()