import threading
from time import sleep
import pigpio
import numpy as np
from Scaler_LeftAnalogStick_Shoulder import get_shoulder_value
from Scaler_RightAnalogStick_Elbow import get_elbow_value

# Global variables
shoulder_value = 150  # Initial shoulder position (0-1000 mapped later to duty cycles)
elbow_value = 980     # Initial elbow position (0-1000 mapped later to duty cycles)
exit_program = False  # Flag to stop threads

# Servo GPIO pins
SHOULDER_PIN = 21
ELBOW_PIN = 20

# Connect to pigpio daemon
pi = pigpio.pi()
if not pi.connected:
    print("Failed to connect to pigpio daemon.")
    exit(1)

def update_shoulder():
    global shoulder_value, exit_program
    while not exit_program:
        try:
            shoulder_value = get_shoulder_value()  
            # Debugging print (optional)
            print(f"Shoulder Value: {shoulder_value:.2f} /\\ Elbow Value: {elbow_value:.2f}")  
        except Exception as e:
            print(f"Error fetching shoulder value: {e}")
        sleep(0.05)

def update_elbow():
    global elbow_value, exit_program
    while not exit_program:
        try:
            elbow_value = get_elbow_value()  
        except Exception as e:
            print(f"Error fetching elbow value: {e}")
        sleep(0.05)

def map_to_pulsewidth(value, in_min, in_max, out_min, out_max):
    """
    Map the given servo duty cycle value (e.g. [2,12]) to a pulse width in microseconds.
    Adjust the ranges as needed.
    """
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def main():
    global exit_program
    exit_program = False

    # Start threads to update shoulder and elbow values
    thread_shoulder = threading.Thread(target=update_shoulder, daemon=True)
    thread_elbow = threading.Thread(target=update_elbow, daemon=True)
    thread_shoulder.start()
    thread_elbow.start()

    try:
        # Main loop to drive servos
        while not exit_program:
            try:
                # Set servo pulsewidths using pigpio
                pi.set_servo_pulsewidth(SHOULDER_PIN, shoulder_value)
                pi.set_servo_pulsewidth(ELBOW_PIN, elbow_value)
                return shoulder_value, elbow_value

            except ValueError as e:
                print(f"Error in servo update: {e}")
            sleep(0.05)

    except KeyboardInterrupt:
        print("Exiting program...")
        exit_program = True

    finally:
        # Stop sending pulses to the servos by setting pulsewidth to 0
        pi.set_servo_pulsewidth(SHOULDER_PIN, 0)
        pi.set_servo_pulsewidth(ELBOW_PIN, 0)
        thread_shoulder.join()
        thread_elbow.join()
        pi.stop()  # Disconnect from pigpio
        print("Program exited.")

if __name__ == "__main__":
    main()

# Added functions to interface with ProgramChanger.py
def get_positions():
    # Return the current known servo positions
    global shoulder_value, elbow_value
    return shoulder_value, elbow_value

def start():
    # Start main in a new thread so it doesn't block
    threading.Thread(target=main, daemon=True).start()

def stop():
    global exit_program
    exit_program = True
