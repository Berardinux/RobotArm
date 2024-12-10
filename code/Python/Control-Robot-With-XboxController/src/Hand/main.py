import RPi.GPIO as GPIO
from time import sleep
import threading
from WristControl import get_wrist_value, exit_program
from HandControl import get_hand_value  # Import hand control function

# GPIO pins for the wrist and hand servos
WRIST_PIN = 16
HAND_PIN = 26  # Update this to the correct pin for your hand servo

def initialize_wrist_servo():
    """
    Initialize the wrist servo by setting up the GPIO pin and starting PWM.
    Assumes a standard servo frequency of 50 Hz.
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(WRIST_PIN, GPIO.OUT)
    wrist_servo = GPIO.PWM(WRIST_PIN, 50)  # 50 Hz frequency
    wrist_servo.start(0)
    return wrist_servo

def initialize_hand_servo():
    """
    Initialize the hand servo by setting up the GPIO pin and starting PWM.
    Also assumes a standard servo frequency of 50 Hz.
    """
    GPIO.setmode(GPIO.BCM)  # Ensures BCM mode is set (redundant but safe)
    GPIO.setup(HAND_PIN, GPIO.OUT)
    hand_servo = GPIO.PWM(HAND_PIN, 50)
    hand_servo.start(0)
    return hand_servo

def main():
    global exit_program
    exit_program = False

    # Initialize both wrist and hand servos
    wrist_servo = initialize_wrist_servo()
    hand_servo = initialize_hand_servo()

    try:
        # Main loop to continuously update the servos based on input
        while not exit_program:
            # Retrieve the current duty cycle values
            wrist_value = get_wrist_value()  # e.g., [2,12]
            hand_value = get_hand_value()    # e.g., [2,10.8] or as configured

            # Debugging prints (optional)
            print(f"Wrist Duty Cycle: {wrist_value:.2f}, Hand Duty Cycle: {hand_value:.2f}")

            # Update the servo duty cycles
            wrist_servo.ChangeDutyCycle(wrist_value)
            hand_servo.ChangeDutyCycle(hand_value)

            sleep(0.05)

    except KeyboardInterrupt:
        print("Exiting program...")
        exit_program = True
    finally:
        # Stop PWM signals and clean up GPIO
        wrist_servo.stop()
        hand_servo.stop()
        GPIO.cleanup()
        print("Program exited.")

if __name__ == "__main__":
    main()
