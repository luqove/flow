# Micro Servo 9g Control class
import RPi.GPIO as GPIO
import time

servo_pin = 12

# Initialise the pin as on output and PWM
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)  # 50 Hz

# Initialise the pwm with pulse off
pwm.start(0)
pwm.ChangeDutyCycle(7.5)  # Set starting position


# Activation function, angle variable of 0 to 180 degree
def act(angle):
    if 0 <= angle <= 180:
        duty = (angle / 18) + 2
        pwm.ChangeDutyCycle(duty)
    else:
        # Incorrect argument given
        print("Incorrect argument. Angle must be between 0 and 180.")
    return
