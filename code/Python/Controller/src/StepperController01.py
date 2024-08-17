from time import sleep
import RPi.GPIO as GPIO
from evdev import InputDevice, categorize, ecodes

# Initialize GPIO
DIR = 14
STEP = 15
DIR0 = 18
DIR1 = 23
LEFT = -1
RIGHT = 1

# Setup GPIO
GPIO.setmode(GPIO.BCM)  # Use GPIO numbers
GPIO.setup(DIR, GPIO.OUT)  # Direction pin
GPIO.setup(STEP, GPIO.OUT)  # Step pin (PWM)
GPIO.setup(DIR0, GPIO.IN)
GPIO.setup(DIR1, GPIO.IN)

# Initialize PWM on STEP pin with a frequency of 1000 Hz
pwm = GPIO.PWM(STEP, 1000)  # 1000 Hz frequency
pwm.start(0)  # Start PWM with a 0% duty cycle (motor stopped)

# Set initial direction
GPIO.output(DIR, GPIO.HIGH)

# Open the event file for your input device (replace with your actual event number)
gamepad = InputDevice('/dev/input/event4')  # Change to your specific event file

moving = False  # Track whether the motor should be moving
direction = None  # Track the current direction (LEFT, RIGHT, or None)

def handle_limit_switch():
    global moving
    if GPIO.input(DIR0) == GPIO.HIGH:
        print("Limit switch DIR0 triggered")
        pwm.ChangeDutyCycle(0)  # Stop the motor
        moving = False
        return True

    elif GPIO.input(DIR1) == GPIO.HIGH:
        print("Limit switch DIR1 triggered")
        pwm.ChangeDutyCycle(0)  # Stop the motor
        moving = False
        return True

    return False

try:
    while True:
        # Continuously check for limit switches
        if handle_limit_switch():
            direction = None  # Reset direction if limit switch is triggered
            continue  # Skip further input processing if limit switch is active

        # Read and process input events
        for event in gamepad.read_loop():
            if event.type == ecodes.EV_ABS:
                absevent = categorize(event)
                if absevent.event.code == ecodes.ABS_HAT0X:
                    if absevent.event.value == LEFT and not moving:
                        if GPIO.input(DIR1) == GPIO.LOW:
                            print("D-pad left pressed")
                            GPIO.output(DIR, GPIO.LOW)
                            pwm.ChangeDutyCycle(50)
                            moving = True
                            direction = LEFT

                    elif absevent.event.value == RIGHT and not moving:
                        if GPIO.input(DIR0) == GPIO.LOW:
                            print("D-pad right pressed")
                            GPIO.output(DIR, GPIO.HIGH)
                            pwm.ChangeDutyCycle(50)
                            moving = True
                            direction = RIGHT

                    elif absevent.event.value == 0:  # D-pad released
                        if moving:
                            print("D-pad released")
                            pwm.ChangeDutyCycle(0)
                            moving = False
                            direction = None

            sleep(0.01)  # Short delay before the next loop iteration

        # If the D-pad is still held, continue moving in that direction
        if direction == LEFT and GPIO.input(DIR1) == GPIO.LOW:
            pwm.ChangeDutyCycle(50)
        elif direction == RIGHT and GPIO.input(DIR0) == GPIO.LOW:
            pwm.ChangeDutyCycle(50)

        sleep(0.01)

except KeyboardInterrupt:
    pass

finally:
    pwm.stop()
    GPIO.cleanup()
