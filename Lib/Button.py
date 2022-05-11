import RPi.GPIO as GPIO
import time


class Button(object):
    """
    button
    """

    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN)

    def is_pushed(self):
        time.sleep(0.005)
        return GPIO.Input(self.pin)

    def is_released(self):
        time.sleep(0.005)
        return GPIO.Input(self.pin) == 0
