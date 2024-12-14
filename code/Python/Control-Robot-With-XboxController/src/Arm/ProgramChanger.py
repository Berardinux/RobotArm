#!/usr/bin/env python3
import evdev
import subprocess
from time import sleep
import pigpio

from IndividualControl.individual_main import start as start_individual, stop as stop_individual, get_positions as get_individual_positions
from InverseKinematicsControl.ik_main import start as start_ik, stop as stop_ik, get_positions as get_ik_positions

DEVICE_PATH = "/dev/input/event4"
BTN_MODE_CODE = 316  # main Xbox button code
SHOULDER_PIN = 21
ELBOW_PIN = 20
pi = pigpio.pi()
if not pi.connected:
    print("Failed to connect to pigpio daemon.")
    exit(1)

program_number = 0  # 0 = IndividualControl, 1 = InverseKinematicsControl
home_shoulder_val = 1500
home_elbow_val = 1500

def Ramp(old_shoulder, old_elbow, new_shoulder, new_elbow):
    # Ramp shoulder
    step = 1 if new_shoulder > old_shoulder else -1
    for val in range(old_shoulder, new_shoulder, step):
        pi.set_servo_pulsewidth(SHOULDER_PIN, val)
        sleep(0.01)
    # Ramp elbow
    step = 1 if new_elbow > old_elbow else -1
    for val in range(old_elbow, new_elbow, step):
        pi.set_servo_pulsewidth(ELBOW_PIN, val)
        sleep(0.01)

# Start the initial program
start_individual()

try:
    device = evdev.InputDevice(DEVICE_PATH)
    print(f"Listening to {device.name} at {DEVICE_PATH}...")

    for event in device.read_loop():
        if event.type == evdev.ecodes.EV_KEY and event.code == BTN_MODE_CODE:
            if event.value == 1:  # Button pressed
                # Get current positions from the active program
                if program_number == 0:
                    old_shoulder, old_elbow = get_individual_positions()
                    print("Switching to InverseKinematicsControl...")
                    # Ramp to home
                    Ramp(old_shoulder, old_elbow, home_shoulder_val, home_elbow_val)
                    stop_individual()
                    start_ik()
                    program_number = 1
                else:
                    old_shoulder, old_elbow = get_ik_positions()
                    print("Switching to IndividualControl...")
                    # Ramp to home
                    Ramp(old_shoulder, old_elbow, home_shoulder_val, home_elbow_val)
                    stop_ik()
                    start_individual()
                    program_number = 0

            elif event.value == 0:  # Button released
                print("BTN_MODE released.")

except FileNotFoundError:
    print(f"Device {DEVICE_PATH} not found. Ensure the controller is connected.")
except PermissionError:
    print(f"Permission denied for {DEVICE_PATH}. Try running as root.")
except KeyboardInterrupt:
    print("Exiting program...")
finally:
    # Stop whichever program is running
    if program_number == 0:
        stop_individual()
    else:
        stop_ik()
    pi.set_servo_pulsewidth(SHOULDER_PIN, 0)
    pi.set_servo_pulsewidth(ELBOW_PIN, 0)
    pi.stop()
    print("Program exited.")
