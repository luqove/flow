import RPi.GPIO as GPIO
import time

# Setup stepper GPIO Pins
stepper_control_pins = [7, 11, 13, 15, 22, 23, 24, 25]

for outpin in stepper_control_pins:
    GPIO.setup(outpin, GPIO.OUT)
    GPIO.output(outpin, 0)

# Static Variables
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


def act(motor_num, num_rev, direction):
    # To avoid complications in remembering which step a motor is currently at
    # limit commands exclusively to a full revolution

    # Repeat loop for however many sequences requested, 512 sequences per revolution
    if direction == "cw":
        for i in range(num_rev * 512):
            # Loop through 8 steps per sequence
            for half_step in range(8):
                # Set all pins for the half step
                for pin in range(4):
                    GPIO.output(stepper_control_pins[pin + 4 * motor_num], half_seq_cw[half_step][pin])
                    # Sleep for short time to give motor time to react to pin change
                    time.sleep(0.001)
        return
    elif direction == "ccw":
        for i in range(num_rev * 512):
            # Loop through 8 steps per sequences
            for half_step in range(8):
                # Set all pins for the half step
                for pin in range(4):
                    GPIO.output(stepper_control_pins[pin + 4 * motor_num], half_seq_ccw[half_step][pin])
                    # Sleep for short time to give motor time to react to pin change
                    time.sleep(0.001)
        return
