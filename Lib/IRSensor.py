import RPi.GPIO as GPIO


class IRSensor(object):
    """
    IR
    """

    def __init__(self, pin):
        self.current_read = 0  # current reading
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN)

    def read_data(self):
        self.current_read = GPIO.input(self.pin)
