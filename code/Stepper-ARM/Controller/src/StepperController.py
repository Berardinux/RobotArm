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
pwm.start(50)  # Start PWM with a 50% duty cycle

# Set initial direction
GPIO.output(DIR, GPIO.HIGH)

# Open the event file for your input device (replace with your actual event number)
gamepad = InputDevice('/dev/input/event0')  # Change to your specific event file

try:
    for event in gamepad.read_loop():
        if event.type == ecodes.EV_ABS:
            absevent = categorize(event)
            if absevent.event.code == ecodes.ABS_HAT0X:
                if absevent.event.value == -1:  # Left
                    print("D-pad left")
                    GPIO.output(DIR, GPIO.LOW)  # Switch direction
                elif absevent.event.value == 1:  # Right
                    print("D-pad right")
                    GPIO.output(DIR, GPIO.HIGH)  # Switch direction
                elif absevent.event.value == 0:  # Center
                    print("D-pad center")
                    # Stop motor or keep direction
                    pwm.ChangeDutyCycle(0)  # Optionally stop PWM if needed

        # Run the motor with PWM
        pwm.ChangeDutyCycle(50)  # Adjust duty cycle as needed

        sleep(0.1)  # Short delay before next loop iteration

except KeyboardInterrupt:
    pass

finally:
    pwm.stop()
    GPIO.cleanup()
