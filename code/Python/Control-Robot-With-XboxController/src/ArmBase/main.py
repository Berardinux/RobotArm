import threading
from time import sleep
import RPi.GPIO as GPIO
from Scaler_LeftAnalogStick_BaseRotation import get_base_value

# Global variables
base_value = 500  # Initial base position (0-1000 range, mapped to servo duty cycle)
exit_program = False  # Flag to stop threads

# Servo GPIO pin
BASE_PIN = 12

def update_base():
    """
    Continuously fetch and update the base rotation value using the left analog stick.
    The get_base_value() function from Scaler_LeftAnalogStick_BaseRotation.py
    returns a duty cycle value appropriate for the servo.
    """
    global base_value, exit_program
    while not exit_program:
        try:
            base_value = get_base_value()  
            print(f"Base Rotation Value (PWM): {base_value:.2f}")  # Debugging
        except Exception as e:
            print(f"Error fetching base rotation value: {e}")
        sleep(0.05)

def initialize_servo():
    """
    Initialize the servo connected to BASE_PIN.
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BASE_PIN, GPIO.OUT)
    base_servo = GPIO.PWM(BASE_PIN, 50)  # 50 Hz frequency for standard RC servo
    base_servo.start(0)
    return base_servo

def main():
    global exit_program

    # Initialize the base rotation servo
    base_servo = initialize_servo()

    try:
        # Create a thread to update the base rotation value from the analog stick
        thread_base = threading.Thread(target=update_base, daemon=True)
        thread_base.start()

        # Main loop to apply the base_value to the servo
        while not exit_program:
            try:
                # base_value already represents a PWM duty cycle in the servo's valid range.
                base_servo.ChangeDutyCycle(base_value)
            except ValueError as e:
                print(f"Error updating servo duty cycle: {e}")
            sleep(0.05)

    except KeyboardInterrupt:
        print("Exiting program...")
        exit_program = True  # Signal threads to stop

    finally:
        thread_base.join()
        base_servo.stop()
        GPIO.cleanup()
        print("Program exited.")

if __name__ == "__main__":
    main()
