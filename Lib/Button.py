<<<<<<< HEAD
import RPi.GPIO as GPIO
import time

=======
>>>>>>> ba00b04ea178c39d71c452e25ef1d277abf379af

class Button(object):
    """
    按钮类
    """

    def __init__(self, pin):
        self.pin = pin
<<<<<<< HEAD
        GPIO.setup(self.pin, GPIO.IN)

    # TODO 这里看要怎么实现按钮按下检测。
    # 大抵是检测相应的GPIO输入
    # 可能需要做按钮防抖，但不是你的工作
    def is_pushed(self):
        time.sleep(0.005)
        return GPIO.Input(self.pin)

    def is_released(self):
        time.sleep(0.005)
        return GPIO.Input(self.pin) == 0
=======

    # TODO 
    def is_pushed(self):
        return True

    def is_released(self):
        return True
>>>>>>> ba00b04ea178c39d71c452e25ef1d277abf379af
