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

def handle_limit_switch():
    if GPIO.input(DIR0) == GPIO.HIGH:
        print("Limit switch DIR0 triggered")
        GPIO.output(DIR, GPIO.HIGH)  # Reverse direction to move away from the switch
        pwm.ChangeDutyCycle(50)  # Move away from the switch
        while GPIO.input(DIR0) == GPIO.HIGH:
            sleep(0.01)  # Continue moving until the limit switch is deactivated
        pwm.ChangeDutyCycle(0)  # Stop motor when limit switch is deactivated

    elif GPIO.input(DIR1) == GPIO.HIGH:
        print("Limit switch DIR1 triggered")
        GPIO.output(DIR, GPIO.LOW)  # Reverse direction to move away from the switch
        pwm.ChangeDutyCycle(50)  # Move away from the switch
        while GPIO.input(DIR1) == GPIO.HIGH:
            sleep(0.01)  # Continue moving until the limit switch is deactivated
        pwm.ChangeDutyCycle(0)  # Stop motor when limit switch is deactivated

try:
    for event in gamepad.read_loop():
        # Continuously check if limit switches are triggered
        if GPIO.input(DIR0) == GPIO.HIGH or GPIO.input(DIR1) == GPIO.HIGH:
            handle_limit_switch()  # Handle limit switch event first
            continue  # Skip further input processing if limit switch is active
        if event.type == ecodes.EV_ABS:
            absevent = categorize(event)
            if absevent.event.code == ecodes.ABS_HAT0X:
                if absevent.event.value == LEFT:  # D-pad left
                    if GPIO.input(DIR1) == GPIO.LOW:  # Allow movement only if the switch is not active
                        print("D-pad left pressed")
                        GPIO.output(DIR, GPIO.LOW)  # Set direction to LOW
                        pwm.ChangeDutyCycle(50)  # Start motor
                        moving = True
                elif absevent.event.value == RIGHT:  # D-pad right
                    if GPIO.input(DIR0) == GPIO.LOW:  # Allow movement only if the switch is not active
                        print("D-pad right pressed")
                        GPIO.output(DIR, GPIO.HIGH)  # Set direction to HIGH
                        pwm.ChangeDutyCycle(50)  # Start motor
                        moving = True
                elif absevent.event.value == 0:  # D-pad released (centered)
                    if moving:
                        print("D-pad released")
                        pwm.ChangeDutyCycle(0)  # Stop motor
                        moving = False

        sleep(0.01)  # Short delay before the next loop iteration

except KeyboardInterrupt:
    pass

finally:
    pwm.stop()
    GPIO.cleanup()
