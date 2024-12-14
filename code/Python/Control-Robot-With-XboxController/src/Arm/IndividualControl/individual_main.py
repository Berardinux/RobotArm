import threading
from time import sleep
import pigpio
import numpy as np
from .Scaler_LeftAnalogStick_Shoulder import get_shoulder_value
from .Scaler_RightAnalogStick_Elbow import get_elbow_value

shoulder_value = 33    # Initial shoulder position
elbow_value = 880      # Initial elbow position
exit_program = False
main_thread = None

SHOULDER_PIN = 21
ELBOW_PIN = 20

def update_shoulder():
    global shoulder_value, exit_program
    while not exit_program:
        try:
            shoulder_value = get_shoulder_value()
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

    # Initialize pigpio each time main runs
    pi = pigpio.pi()
    if not pi.connected:
        print("Failed to connect to pigpio daemon.")
        return

    thread_shoulder = threading.Thread(target=update_shoulder, daemon=True)
    thread_elbow = threading.Thread(target=update_elbow, daemon=True)
    thread_shoulder.start()
    thread_elbow.start()

    try:
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
        # Wait for the threads to finish
        thread_shoulder.join()
        thread_elbow.join()

        # Stop sending pulses to the servos
        pi.set_servo_pulsewidth(SHOULDER_PIN, 0)
        pi.set_servo_pulsewidth(ELBOW_PIN, 0)
        pi.stop()
        print("Program exited.")

def get_positions():
    global shoulder_value, elbow_value
    return shoulder_value, elbow_value

def start():
    global main_thread, exit_program
    exit_program = False
    main_thread = threading.Thread(target=main, daemon=True)
    main_thread.start()

def stop():
    global exit_program, main_thread
    exit_program = True
    if main_thread is not None:
        main_thread.join()
        main_thread = None
