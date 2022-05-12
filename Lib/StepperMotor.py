import RPi.GPIO as GPIO
import time

# stepper
half_seq_ccw = [[1, 0, 0, 0],
                [1, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 1],
                [0, 0, 0, 1],
                [1, 0, 0, 1]]

half_seq_cw = [[0, 0, 0, 1],
               [0, 0, 1, 1],
               [0, 0, 1, 0],
               [0, 1, 1, 0],
               [0, 1, 0, 0],
               [1, 1, 0, 0],
               [1, 0, 0, 0],
               [1, 0, 0, 1]]


class StepperMotor(object):
    """
    Stepper 

    """

    def __init__(self, motor_pins):
        # One motor corresponds to four pins, 
        #and the following are the corresponding pins of two motors. need to be entered when creating。
        # [7, 11, 13, 15],
        # [22, 23, 24, 25]
        # To distinguish motor, it is written as Stepper_motor_0 Stepper_motor_1 in sourcelib
        self.motor_pins = motor_pins
        # initial motor pins
        self.gpio_setup()

    def gpio_setup(self):
        for outpin in self.motor_pins:
            GPIO.setup(outpin, GPIO.OUT)
            GPIO.output(outpin, 0)

    # To achieve rotation, door opening, or to rotate the belt
    def act(self, num_rev, direction):
        # To avoid complications in remembering which step a motor is currently at
        # limit commands exclusively to a full revolution
        # Repeat loop for however many sequences requested, 512 sequences per revolution
        if direction == "cw":
            for i in range(num_rev * 512):
                # Loop through 8 steps per sequence
                for half_step in range(8):
                    # Set all pins for the half step
                    for pin in range(4):
                        GPIO.output(self.motor_pins[pin], half_seq_cw[half_step][pin])
                        # Sleep for short time to give motor time to react to pin change
                        time.sleep(0.001)
        elif direction == "ccw":
            for i in range(num_rev * 512):
                # Loop through 8 steps per sequences
                for half_step in range(8):
                    # Set all pins for the half step
                    for pin in range(4):
                        GPIO.output(self.motor_pins[pin], half_seq_ccw[half_step][pin])
                        # Sleep for short time to give motor time to react to pin change
                        time.sleep(0.001)
