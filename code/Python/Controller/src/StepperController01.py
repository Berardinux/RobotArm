from time import sleep
import threading
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

def check_limit_switch():
    global moving, direction
    while True:
        if GPIO.input(DIR0) == GPIO.HIGH:
            print("Limit switch DIR0 triggered")
            GPIO.output(DIR, GPIO.HIGH)  # Reverse direction to move away from the switch
            pwm.ChangeDutyCycle(50)  # Move away from the switch
            while GPIO.input(DIR0) == GPIO.HIGH:
                sleep(0.01)  # Continue moving until the limit switch is deactivated
            pwm.ChangeDutyCycle(0)  # Stop motor when limit switch is deactivated
            moving = False
            direction = None
        elif GPIO.input(DIR1) == GPIO.HIGH:
            print("Limit switch DIR1 triggered")
            GPIO.output(DIR, GPIO.LOW)  # Reverse direction to move away from the switch
            pwm.ChangeDutyCycle(50)  # Move away from the switch
            while GPIO.input(DIR1) == GPIO.HIGH:
                sleep(0.01)  # Continue moving until the limit switch is deactivated
            pwm.ChangeDutyCycle(0)  # Stop motor when limit switch is deactivated
            moving = False
            direction = None
        sleep(0.01)  # Short delay to prevent high CPU usage

# Start a thread to continuously check the limit switches
limit_switch_thread = threading.Thread(target=check_limit_switch)
limit_switch_thread.daemon = True  # This makes sure the thread exits when the main program does
limit_switch_thread.start()

try:
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

except KeyboardInterrupt:
    pass

finally:
    pwm.stop()
    GPIO.cleanup()
