import RPi.GPIO as GPIO
from time import sleep
import threading
import sys

# Disable GPIO warnings
GPIO.setwarnings(False)

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.OUT)  # Middle arm
GPIO.setup(21, GPIO.OUT)  # Bottom arm
GPIO.setup(12, GPIO.OUT)  # Rotation servo

# Initialize servos
middle_servo = GPIO.PWM(20, 50)
bottom_servo = GPIO.PWM(21, 50)
rotation_servo = GPIO.PWM(12, 50)

# Error handling for command-line arguments
if len(sys.argv) != 4:
    OldPositionRotation = 7.0
    OldPositionBottom = 3.0
    OldPositionMiddle = 10.6
else:
    try:
        OldPositionRotation = float(sys.argv[1])
        OldPositionBottom = float(sys.argv[2])
        OldPositionMiddle = float(sys.argv[3])
    except ValueError:
        print("Error: All arguments must be valid float values.")
        sys.exit(1)

# Initialize servos at old positions
middle_servo.start(OldPositionMiddle)
bottom_servo.start(OldPositionBottom)
rotation_servo.start(OldPositionRotation)

# Home positions
rotation_home = 7.15
bottom_home = 3.2
middle_home = 10.8

def MoveHome(OldPositionRotation, OldPositionBottom, OldPositionMiddle):
    # Move all servos to the home position
    try:
        thread_rotation = threading.Thread(target=Ramp, args=(rotation_servo, OldPositionRotation, rotation_home))
        thread_bottom = threading.Thread(target=Ramp, args=(bottom_servo, OldPositionBottom, bottom_home))
        thread_middle = threading.Thread(target=Ramp, args=(middle_servo, OldPositionMiddle, middle_home))
   
        thread_rotation.start()
        thread_bottom.start()
        thread_middle.start()

        thread_rotation.join()
        thread_bottom.join()
        thread_middle.join()

    finally:
        rotation_servo.stop()
        bottom_servo.stop()
        middle_servo.stop()
        GPIO.cleanup()

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
    elif OldDutyCycle == NewDutyCycle:
        print("No Change")

# Print initial and home positions for debugging
print(f"Moving servos from positions: Rotation={OldPositionRotation}, Bottom={OldPositionBottom}, Middle={OldPositionMiddle}")
print(f"Home positions: Rotation={rotation_home}, Bottom={bottom_home}, Middle={middle_home}")

MoveHome(OldPositionRotation, OldPositionBottom, OldPositionMiddle)
