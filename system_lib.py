import time

import RPi.GPIO as GPIO

from Lib.Button import Button
from Lib.IRSensor import IRSensor
from Lib.LED import LED
from Lib.ServoMotor import ServoMotor
from Lib.StepperMotor import StepperMotor
from Lib.ULSensor import ULSensor
from const import *


class System(object):
    """
    main thread
    """

    def __init__(self):
        # stack count 50
        self.stack_count = 50

        # Setup the pins
        GPIO.setmode(GPIO.BOARD)

        # IR sensors
        self.IR_sensor_Empty = IRSensor(IR_EMPTY_pin)
        self.IR_sensor_25P = IRSensor(IR_25P_pin)
        self.IR_sensor_50P = IRSensor(IR_50P_pin)
        self.IR_sensor_75P = IRSensor(IR_75P_pin)
        self.IR_sensor_Collect = IRSensor(IR_COLLECT_pin)

        # UL sensors
        # UL pin
        self.UL_sensor_1 = ULSensor()

        # Stepper_motor
        self.Stepper_motor_0 = StepperMotor(stepper0_control_pins)
        self.Stepper_motor_1 = StepperMotor(stepper1_control_pins)

        # Servo_motor
        self.Servo_motor_0 = ServoMotor(servo_pin)

        # TODO button
        self.reset_button = Button('''pin''')


        self.LED_READY = LED(LED_READY_pin)
        self.LED_USER = LED(LED_USER_pin)
        self.LED_DISPENSING = LED(LED_DISPENSING_pin)
        self.LED_EMPTY = LED(LED_EMPTY_pin)
        self.LED_FAULT = LED(LED_FAULT_pin)

        self.LED_100P = LED(LED_100P_pin)
        self.LED_75P = LED(LED_75P_pin)
        self.LED_50P = LED(LED_50P_pin)
        self.LED_25P = LED(LED_25P_pin)

    # reset all
    def reset(self):
        self.reset_stock_led()
        self.reset_report_led()

        self.close_door()
        #
        self.IR_sensor_Empty.current_read = IR_HIGH_NO_OBJ
        self.IR_sensor_25P.current_read = IR_HIGH_NO_OBJ
        self.IR_sensor_50P.current_read = IR_HIGH_NO_OBJ
        self.IR_sensor_75P.current_read = IR_HIGH_NO_OBJ
        self.IR_sensor_Collect.current_read = IR_HIGH_NO_OBJ

    # Remaining masks led display reset
    def reset_stock_led(self):
        self.turn_off_led(LED_25P)
        self.turn_off_led(LED_50P)
        self.turn_off_led(LED_75P)
        self.turn_off_led(LED_100P)

    # Reset empty, ready, fault, DISPENSING leds, all off
    def reset_report_led(self):
        self.turn_off_led(LED_EMPTY)
        self.turn_off_led(LED_DISPENSING)
        self.turn_off_led(LED_FAULT)
        self.turn_off_led(LED_READY)
        self.turn_off_led(LED_USER)

    # Turn on red "empty" LED and
    # notify control centre
    def report_empty(self):
        # turn off the rest of the leds
        self.reset_report_led()
        # open LED_EMPTY
        self.turn_on_led(LED_EMPTY)

    # Turn on fault LED and notify control centre
    def report_fault(self):
        # turn off the rest of the leds
        self.reset_report_led()
        # oen LED_FAULT
        self.turn_on_led(LED_FAULT)

    # what is the stack level?
    def display_stack_level(self):
        # update IR_sensor1
        self.IR_sensor_25P.read_data()
        self.IR_sensor_50P.read_data()
        self.IR_sensor_75P.read_data()
        # Reset the previous remaining amount display
        self.reset_stock_led()
        # 0-25%
        if self.IR_sensor_25P.current_read == IR_HIGH_NO_OBJ:
            self.turn_on_led(LED_25P)
        # 25-50%
        elif (self.IR_sensor_25P.current_read == IR_LOW_HAS_OBJ and
              self.IR_sensor_50P.current_read == IR_HIGH_NO_OBJ):
            self.turn_on_led(LED_50P)
        # 50-75
        elif (self.IR_sensor_25P.current_read == IR_LOW_HAS_OBJ and
              self.IR_sensor_50P.current_read == IR_LOW_HAS_OBJ and
              self.IR_sensor_75P.current_read == IR_HIGH_NO_OBJ):
            self.turn_on_led(LED_75P)
        # 75-100
        elif (self.IR_sensor_25P.current_read == IR_LOW_HAS_OBJ and
              self.IR_sensor_50P.current_read == IR_LOW_HAS_OBJ and
              self.IR_sensor_75P.current_read == IR_LOW_HAS_OBJ):
            self.turn_on_led(LED_100P)

    # Is mask tray empty?
    def is_mask_tray_empty(self):
        self.IR_sensor_Empty.read_data()
        if self.IR_sensor_Empty.current_read == IR_HIGH_NO_OBJ:
            return True
        else:
            return False
  
    # Is a mask in transit?
    def is_mask_in_transit(self):
        # Update the reading of IR_sensor5
        self.IR_sensor_Collect.read_data()
        if self.IR_sensor_Collect.current_read == IR_LOW_HAS_OBJ:
            return True
   
        else:
            return False

    # Is mask requested
    def is_mask_requested(self):
        self.UL_sensor_1.read_data()
        if self.UL_sensor_1.current_read < 40:
            return True
        else:
            return False

    # Is a mask in the waiting position?
    def is_mask_in_waiting_position(self):
        self.IR_sensor_Collect.read_data()
        if self.IR_sensor_Collect.current_read == IR_LOW_HAS_OBJ:
            return True
        else:
            return False

    # dispensing mask
    def dispensing_mask(self):
        self.reset_report_led()
        self.turn_on_led(LED_DISPENSING)
        self.Stepper_motor_0.act(2, "ccw")  # partially slide mask out of stack
        # TODO Should there be a time gap between two motor moves
        self.Stepper_motor_1.act(1, "ccw")  # pull the mask completely out of stack
        self.turn_off_led(LED_DISPENSING)

    # Open door
    def open_door(self):
        self.Servo_motor_0.act(100)

    # Close door
    def close_door(self):
        self.Servo_motor_0.act(0)

    # Release the mask partially
    # 将口罩部分推出机器等待客人拿取
    def release_mask_partially(self):
        self.Stepper_motor_1.act(2, "ccw")

    # Release the mask totally
    # Push the mask completely out of the machine
    # Here is simplified usage. 
    #It may only be necessary to partially do it. Delete depending on the situation.
    def release_mask_totally(self):
        self.Stepper_motor_1.act(2, "ccw")

    # Is a mask in the collection position?
    def is_mask_still_waiting_collection(self):
        if self.IR_sensor_Collect.current_read == IR_LOW_HAS_OBJ:
            return True
        else:
            return False

    # Turn on fault LED and
    # notify control centre
    def turn_on_led(self, led):
        if led == LED_EMPTY:
            self.LED_EMPTY.light_up()
        elif led == LED_DISPENSING:
            self.LED_DISPENSING.light_up()
        elif led == LED_USER:
            self.LED_USER.light_up()
        elif led == LED_READY:
            self.LED_READY.light_up()
        elif led == LED_FAULT:
            self.LED_FAULT.light_up()
        elif led == LED_25P:
            self.LED_25P.light_up()
        elif led == LED_50P:
            self.LED_50P.light_up()
        elif led == LED_75P:
            self.LED_75P.light_up()
        elif led == LED_100P:
            self.LED_100P.light_up()

    def turn_off_led(self, led):
        if led == LED_EMPTY:
            self.LED_EMPTY.turn_off()
        elif led == LED_DISPENSING:
            self.LED_DISPENSING.turn_off()
        elif led == LED_USER:
            self.LED_USER.turn_off()
        elif led == LED_READY:
            self.LED_READY.turn_off()
        elif led == LED_FAULT:
            self.LED_FAULT.turn_off()
        elif led == LED_25P:
            self.LED_25P.turn_off()
        elif led == LED_50P:
            self.LED_50P.turn_off()
        elif led == LED_75P:
            self.LED_75P.turn_off()
        elif led == LED_100P:
            self.LED_100P.turn_off()

    # HALT 
    def HALT(self):
        while not self.reset_button.is_pushed():
            # 每0.1秒轮询检测一次reset按钮是否按下
            time.sleep(0.1)

    # Wait_request 
    def wait_request(self):
        while not self.is_mask_requested():
            # Poll every 0.1 seconds to check whether a client sends a Mask request
            time.sleep(0.1)

    # Open door and move mask into collection position.
    # Wait 3 seconds for user to collect the mask
    def release_mask_partially_and_wait(self):
        self.open_door()
        self.release_mask_partially()
        time.sleep(3)

