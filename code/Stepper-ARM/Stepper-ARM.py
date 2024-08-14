from time import sleep
import RPi.GPIO as GPIO

DIR = 14
STEP = 15
DIR0 = 18
DIR1 = 23

# Setup GPIO
GPIO.setmode(GPIO.BCM)  # Use GPIO numbers
GPIO.setup(DIR, GPIO.OUT)  # Direction pin
GPIO.setup(STEP, GPIO.OUT)  # Step pin (PWM)
GPIO.setup(DIR0, GPIO.IN)   # Input pin to change direction
GPIO.setup(DIR1, GPIO.IN)   # Input pin to change direction

# Initialize PWM on STEP pin with a frequency of 100 Hz
pwm = GPIO.PWM(STEP, 400)  # 100 Hz frequency
pwm.start(50)  # Start PWM with a 50% duty cycle

# Set initial direction
GPIO.output(DIR, GPIO.HIGH)

try:
    while True:
        # Print the state of pin DIR
        pinDIR_state = GPIO.input(DIR)
        print(f"Pin DIR is {'HIGH' if pinDIR_state == GPIO.HIGH else 'LOW'}")

        # Run the motor with PWM
        pwm.ChangeDutyCycle(50)  # You can adjust the duty cycle as needed

        # Check if either pin DIR0 or DIR1 goes high
        if GPIO.input(DIR0) == GPIO.HIGH:
            print("GPIO DIR0 went HIGH")
            GPIO.output(DIR, GPIO.HIGH)  # Switch direction
            sleep(0.5)  # Small delay to debounce the input
        elif GPIO.input(DIR1) == GPIO.HIGH:
            print("GPIO DIR1 went HIGH")
            GPIO.output(DIR, GPIO.LOW)  # Switch direction
            sleep(0.5)  # Small delay to debounce the input

        sleep(0.1)  # Short delay before next loop iteration

except KeyboardInterrupt:
    pass

finally:
    pwm.stop()
    GPIO.cleanup()
