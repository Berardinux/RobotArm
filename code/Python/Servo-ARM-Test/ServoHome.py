import RPi.GPIO as GPIO
from time import sleep
import threading
import sys

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.OUT)  # Middle arm
GPIO.setup(21, GPIO.OUT)  # Bottom arm
GPIO.setup(22, GPIO.OUT)  # Rotation servo

# Initialize servos
middle_servo = GPIO.PWM(20, 50)
bottom_servo = GPIO.PWM(21, 50)
rotation_servo = GPIO.PWM(22, 50)

middle_servo.start(0)
bottom_servo.start(0)
rotation_servo.start(0)

def Ramp(servo, OldDutyCycle, NewDutyCycle):
    if OldDutyCycle < NewDutyCycle:
        i = OldDutyCycle
        while i <= NewDutyCycle:
            servo.ChangeDutyCycle(i)
            i += 0.01
            sleep(0.01)
    elif OldDutyCycle > NewDutyCycle:
        i = OldDutyCycle
        while i >= NewDutyCycle:
            servo.ChangeDutyCycle(i)
            i -= 0.01
            sleep(0.01)

# Get the duty cycles from command-line arguments
OldPostionRotation = float(sys.argv[1])
OldPostionBottom = float(sys.argv[2])
OldPositionMiddle = float(sys.argv[3])

# Home = (RotationServo = 7.15) (BottomServo = 3.2) (MiddleServo = 10.8)
rotation_home = 7.15
bottom_home = 3.2
middle_home = 10.8

# Move all servos to the inputted positions
try:
    threading.Thread(target=Ramp, args=(rotation_servo, OldPostionRotation, rotation_home)).start()
    threading.Thread(target=Ramp, args=(bottom_servo, OldPostionBottom, bottom_home)).start()
    threading.Thread(target=Ramp, args=(middle_servo, OldPositionMiddle, middle_home)).start()
    sleep(3)  # Allow time for movement

finally:
    rotation_servo.stop()
    bottom_servo.stop()
    middle_servo.stop()
    GPIO.cleanup()
