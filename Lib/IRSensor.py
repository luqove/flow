<<<<<<< HEAD
import RPi.GPIO as GPIO


class IRSensor(object):
    """
    IR
=======

class IRSensor(object):
    """
    IR sensor instance for implementing various methods of IRSensor
    Note that the method here should be changed according to the method of the classmate who wrote the sensor.
    My idea is that each sensor is a separate thread responsible for reading and returning data.
>>>>>>> ba00b04ea178c39d71c452e25ef1d277abf379af
    """

    def __init__(self, pin):
        self.current_read = 0  
        self.pin = pin
<<<<<<< HEAD
        GPIO.setup(self.pin, GPIO.IN)
=======
>>>>>>> ba00b04ea178c39d71c452e25ef1d277abf379af

    # Read the function of IR_sensor
    # Call this every time the data is updated and store the data in self.current_read
    # Consider reading multiple data and taking the average
    def read_data(self):
<<<<<<< HEAD
        self.current_read = GPIO.Input(self.pin)
=======
        # TODO
        pass
>>>>>>> ba00b04ea178c39d71c452e25ef1d277abf379af
