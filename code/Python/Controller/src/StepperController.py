from time import sleep
import RPi.GPIO as GPIO
from evdev import InputDevice, categorize, ecodes

# Initialize GPIO
DIR = 14
STEP = 15

# Setup GPIO
GPIO.setmode(GPIO.BCM)  # Use GPIO numbers
GPIO.setup(DIR, GPIO.OUT)  # Direction pin
GPIO.setup(STEP, GPIO.OUT)  # Step pin (PWM)

# Initialize PWM on STEP pin with a frequency of 1000 Hz
pwm = GPIO.PWM(STEP, 1000)  # 1000 Hz frequency
pwm.start(0)  # Start PWM with a 0% duty cycle (motor stopped)

# Set initial direction
GPIO.output(DIR, GPIO.HIGH)

# Open the event file for your input device (replace with your actual event number)
gamepad = InputDevice('/dev/input/event4')  # Change to your specific event file

moving = False  # Track whether the motor should be moving

try:
    for event in gamepad.read_loop():
        if event.type == ecodes.EV_ABS:
            absevent = categorize(event)
            if absevent.event.code == ecodes.ABS_HAT0X:
                if absevent.event.value == -1:  # D-pad left
                    print("D-pad left pressed")
                    GPIO.output(DIR, GPIO.LOW)  # Set direction to LOW
                    pwm.ChangeDutyCycle(50)  # Start motor
                    moving = True
                elif absevent.event.value == 1:  # D-pad right
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
