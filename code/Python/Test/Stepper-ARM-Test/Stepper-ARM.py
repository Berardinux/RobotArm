from time import sleep
import RPi.GPIO as GPIO

DIR = 14
STEP = 15
LIMIT_SWITCH_0 = 18
LIMIT_SWITCH_1 = 23
PPS = 1000
SUB = -20
ADD = 20
i = 0  # Start with i = 0

# Setup GPIO
GPIO.setmode(GPIO.BCM)  # Use GPIO numbers
GPIO.setup(DIR, GPIO.OUT)  # Direction pin
GPIO.setup(STEP, GPIO.OUT)  # Step pin (PWM)
GPIO.setup(LIMIT_SWITCH_0, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   # Input pin to change direction
GPIO.setup(LIMIT_SWITCH_1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   # Input pin to change direction

# Initialize PWM on STEP pin with a frequency of 1000 Hz
pwm = GPIO.PWM(STEP, PPS)  # 1000 Hz frequency
pwm.start(50)  # Start PWM with a 50% duty cycle

# Set initial direction
GPIO.output(DIR, GPIO.HIGH)

def Ramp(actuatedSwitch):
    global PPS
    start = int(PPS / 1.5)  # Calculate starting point and convert to integer
    end = 100

    if actuatedSwitch == 0:
        rampDownDir = GPIO.LOW
        rampUpDir = GPIO.HIGH
        previousDir = "Right"
        currentDir = "Left"
    elif actuatedSwitch == 1:
        rampDownDir = GPIO.HIGH
        rampUpDir = GPIO.LOW
        previousDir = "Left"
        currentDir = "Right"

    # Ramp down loop
    for r in range(start, end, SUB):
        pwm.ChangeFrequency(r)
        GPIO.output(DIR, rampDownDir)
        sleep(0.0005)  # Adjust delay for smoother ramping

    # Ramp up loop
    for r in range(end, start, ADD):
        pwm.ChangeFrequency(r)
        GPIO.output(DIR, rampUpDir)
        sleep(0.0005)  # Adjust delay for smoother ramping

    PPS = 1000
    pwm.ChangeFrequency(PPS)

    print("Previous Direction:", previousDir)
    print("Current Direction:", currentDir)
    print("Ramp complete")

try:
    while True:
        # Print the state of pin DIR every 20 iterations
        i += 1
        if i == 20:
            i = 0
            pinDIR_state = GPIO.input(DIR)
            print(f"Pin DIR is {'HIGH' if pinDIR_state == GPIO.HIGH else 'LOW'}")

        # Run the motor with PWM
        pwm.ChangeDutyCycle(50)  # You can adjust the duty cycle as needed

        # Check if either pin LIMIT_SWITCH_0 or LIMIT_SWITCH_1 goes high
        if GPIO.input(LIMIT_SWITCH_0) == GPIO.HIGH:
            print("GPIO LIMIT_SWITCH_0 went HIGH")
            Ramp(0)
            GPIO.output(DIR, GPIO.HIGH)  # Switch direction
            sleep(0.5)  # Small delay to debounce the input
        elif GPIO.input(LIMIT_SWITCH_1) == GPIO.HIGH:
            print("GPIO LIMIT_SWITCH_1 went HIGH")
            Ramp(1)
            GPIO.output(DIR, GPIO.LOW)  # Switch direction
            sleep(0.5)  # Small delay to debounce the input

        sleep(0.01)  # Short delay before the next loop iteration

except KeyboardInterrupt:
    pass

finally:
    pwm.stop()
    GPIO.cleanup()
