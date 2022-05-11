import RPi.GPIO as GPIO
import time


class ServoMotor(object):
    """
    servo
    """

    # pin
    def __init__(self, servo_pin):
        # angle
        self.angle = 0
        self.servo_pin = servo_pin
        self.gpio_setup()

    def gpio_setup(self):
        GPIO.setup(self.servo_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.servo_pin, 50)  # 50 Hz

        # Initialise the pwm with pulse off
        self.pwm.start(0)
        self.pwm.ChangeDutyCycle(7.5)  # Set starting position

    # To achieve rotation, to achieve door opening, or to rotate the belt
    def act(self, angle):
        if 0 <= angle <= 180:
            duty = (angle / 18) + 2
            self.pwm.ChangeDutyCycle(duty)
        else:
            # Incorrect argument given
            print("Incorrect argument. Angle must be between 0 and 180.")
        return
