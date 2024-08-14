from time import sleep
import RPi.GPIO as GPIO

# Setup GPIO
GPIO.setmode(GPIO.BCM)  # Use GPIO numbers
GPIO.setup(20, GPIO.OUT)  # Direction pin
GPIO.setup(21, GPIO.OUT)  # Step pin (PWM)
GPIO.setup(26, GPIO.IN)   # Input pin to change direction
GPIO.setup(19, GPIO.IN)   # Input pin to change direction

# Initialize PWM on pin 21 with a frequency of 1000 Hz
pwm = GPIO.PWM(21, 100)  # 1000 Hz frequency
pwm.start(50)  # Start PWM with a 50% duty cycle

# Set initial direction
GPIO.output(20, GPIO.HIGH)

try:
    while True:
        # Print the state of pin 20
        pin20_state = GPIO.input(20)
        print(f"Pin 20 is {'HIGH' if pin20_state == GPIO.HIGH else 'LOW'}")

        # Run the motor with PWM
        pwm.ChangeDutyCycle(50)  # You can adjust the duty cycle as needed

        # Check if either pin 26 or 19 goes high
        if GPIO.input(26) == GPIO.HIGH:
            print("GPIO 26 went HIGH")
            GPIO.output(20, GPIO.LOW)  # Switch direction
            sleep(0.5)  # Small delay to debounce the input
        elif GPIO.input(19) == GPIO.HIGH:
            print("GPIO 19 went HIGH")
            GPIO.output(20, GPIO.HIGH)  # Switch direction
            sleep(0.5)  # Small delay to debounce the input

        sleep(0.1)  # Short delay before next loop iteration

except KeyboardInterrupt:
    pass

finally:
    pwm.stop()
    GPIO.cleanup()
