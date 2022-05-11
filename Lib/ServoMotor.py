import RPi.GPIO as GPIO
import time


class ServoMotor(object):
    """
<<<<<<< HEAD
   servo
    """

    # pin。
    def __init__(self, servo_pin):
        # current angle
=======
    Servo
    """

    # pin就是对应的引脚。
    def __init__(self, servo_pin):
        # 记录目前的角度，可以根据这个判断门的开关。
>>>>>>> ba00b04ea178c39d71c452e25ef1d277abf379af
        self.angle = 0
        self.servo_pin = servo_pin
        self.gpio_setup()

    def gpio_setup(self):
        GPIO.setup(self.servo_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.servo_pin, 50)  # 50 Hz

        # Initialise the pwm with pulse off
        self.pwm.start(0)
        self.pwm.ChangeDutyCycle(7.5)  # Set starting position

<<<<<<< HEAD
    # To achieve rotation, to achieve door opening
    # or to rotate the belt。
=======
    # 实现转动，来达成开门，或者转动皮带
    # 参数是输入的脉冲。
>>>>>>> ba00b04ea178c39d71c452e25ef1d277abf379af
    def act(self, angle):
        if 0 <= angle <= 180:
            duty = (angle / 18) + 2
            self.pwm.ChangeDutyCycle(duty)
        else:
            # Incorrect argument given
            print("Incorrect argument. Angle must be between 0 and 180.")
        return
