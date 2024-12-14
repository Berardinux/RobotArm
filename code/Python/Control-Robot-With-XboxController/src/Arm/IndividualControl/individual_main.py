import threading
from time import sleep
import pigpio
import numpy as np
from .Scaler_LeftAnalogStick_Shoulder import get_shoulder_value
from .Scaler_RightAnalogStick_Elbow import get_elbow_value

# Global variables
shoulder_value = 150   # Initial shoulder position (e.g. raw value)
elbow_value = 980      # Initial elbow position (e.g. raw value)
exit_program = False   # Flag to stop threads

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
            # Debug print (optional)
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

def main():
    global exit_program
    exit_program = False

    # Start threads to update shoulder and elbow values
    thread_shoulder = threading.Thread(target=update_shoulder, daemon=True)
    thread_elbow = threading.Thread(target=update_elbow, daemon=True)
    thread_shoulder.start()
    thread_elbow.start()

    try:
        # Main loop to continuously update servos
        while not exit_program:
            try:
                pi.set_servo_pulsewidth(SHOULDER_PIN, shoulder_value)
                pi.set_servo_pulsewidth(ELBOW_PIN, elbow_value)
            except ValueError as e:
                print(f"Error in servo update: {e}")
            sleep(0.05)

    except KeyboardInterrupt:
        print("Exiting program...")
        exit_program = True

    finally:
        # Stop sending pulses to the servos
        pi.set_servo_pulsewidth(SHOULDER_PIN, 0)
        pi.set_servo_pulsewidth(ELBOW_PIN, 0)
        thread_shoulder.join()
        thread_elbow.join()
        pi.stop()  # Disconnect from pigpio
        print("Program exited.")

if __name__ == "__main__":
    main()

# Functions for ProgramChanger.py
def get_positions():
    # Return current known servo positions
    global shoulder_value, elbow_value
    return shoulder_value, elbow_value

def start():
    # Start main in a new thread so it doesn't block
    threading.Thread(target=main, daemon=True).start()

def stop():
    global exit_program
    exit_program = True
