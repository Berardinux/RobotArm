import threading
from time import sleep
import RPi.GPIO as GPIO
from Scaler_LeftAnalogStick_Shoulder import get_shoulder_value
from Scaler_RightAnalogStick_Elbow import get_elbow_value

# Global variables for shoulder and elbow values
shoulder_value = 150  # Initial shoulder position (0-1000 mapped later)
elbow_value = 980     # Initial elbow position (0-1000 mapped later)
exit_program = False  # Flag to stop threads

# Servo GPIO pins
SHOULDER_PIN = 21
ELBOW_PIN = 20

def update_shoulder():
    global shoulder_value, exit_program
    while not exit_program:
        try:
            shoulder_value = get_shoulder_value()  # Fetch shoulder value (scaled)
            print(f"Shoulder Value: {shoulder_value:.2f} /\\ Elbow Value: {elbow_value:.2f}")  # Debugging
        except Exception as e:
            print(f"Error fetching shoulder value: {e}")
        sleep(0.05)

def update_elbow():
    global elbow_value, exit_program
    while not exit_program:
        try:
            elbow_value = get_elbow_value()  # Fetch elbow value (scaled)
            #print(f"Elbow Value: {elbow_value:.2f}")  # Debugging
        except Exception as e:
            print(f"Error fetching elbow value: {e}")
        sleep(0.05)

def initialize_servos():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SHOULDER_PIN, GPIO.OUT)
    GPIO.setup(ELBOW_PIN, GPIO.OUT)
    shoulder_servo = GPIO.PWM(SHOULDER_PIN, 50)  # 50 Hz frequency
    elbow_servo = GPIO.PWM(ELBOW_PIN, 50)        # 50 Hz frequency
    shoulder_servo.start(0)
    elbow_servo.start(0)
    return shoulder_servo, elbow_servo

def main():
    global exit_program

    # Initialize servos
    shoulder_servo, elbow_servo = initialize_servos()

    try:
        # Create threads to fetch shoulder and elbow values
        thread_shoulder = threading.Thread(target=update_shoulder, daemon=True)
        thread_elbow = threading.Thread(target=update_elbow, daemon=True)
        thread_shoulder.start()
        thread_elbow.start()

        # Main loop to drive servos based on shoulder_value and elbow_value
        # The shoulder_value and elbow_value already represent PWM-compatible duty cycles
        # as mapped in the scaler scripts. If needed, further adjustments can be made here.
        while not exit_program:
            try:
                shoulder_servo.ChangeDutyCycle(shoulder_value)
                elbow_servo.ChangeDutyCycle(elbow_value)

            except ValueError as e:
                print(f"Error in servo update: {e}")
            sleep(0.05)

    except KeyboardInterrupt:
        print("Exiting program...")
        exit_program = True  # Signal threads to stop

    finally:
        thread_shoulder.join()
        thread_elbow.join()
        shoulder_servo.stop()
        elbow_servo.stop()
        GPIO.cleanup()
        print("Program exited.")

if __name__ == "__main__":
    main()
