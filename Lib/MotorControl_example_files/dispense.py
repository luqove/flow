# Import Raspberry Pi pin library, time library, and
import RPi.GPIO as GPIO
import time
import servo
import stepper
import sensor


def dispense_mask():
    # Check if there is not another mask in the collection area
<<<<<<< HEAD:Lib/MotorControl_example_files/dispense.py
=======
    # 检查收集区是否有其它口罩。
>>>>>>> ba00b04ea178c39d71c452e25ef1d277abf379af:JWH_MotorControl/dispense.py
    #### Sensor Code ####

    # Path is clear, isolate mask from stack by rotating stepper1
    stepper.act(0, 2, "ccw")

    # Shortly after, rotate stepper2 to pull the mask out
    stepper.act(1, 1, "ccw")

    # Is mask in position?
<<<<<<< HEAD:Lib/MotorControl_example_files/dispense.py
=======
    # 口罩被运送到相应的区域了吗？
>>>>>>> ba00b04ea178c39d71c452e25ef1d277abf379af:JWH_MotorControl/dispense.py
    #### Sensor Code ####

    # Open the door and proceed to push the mask out
    servo.act(100)
    stepper.act(1, 2, "ccw")
    time.sleep(3)

    # Is the mask still in collection position?
    if True:
        # If the mask is still there after 3 seconds, ejected it from the structure and close door
        stepper.act(1, 3, "ccw")

    # Close door
    servo.act(0)
    return 0








