import evdev
from time import sleep
import threading
import numpy as np

# Adjust the event file as needed for your specific device
device = evdev.InputDevice('/dev/input/event4')  # Replace with your specific event file
print(f"Device (Wrist Rotation): {device.path}, Name: {device.name}, Phys: {device.phys}")

WRIST_RAW = 500    # Initial raw wrist rotation value (0-1000 range)
exit_program = False

# This will store the current speed/direction of wrist movement:
# positive = rotating in one direction, negative = opposite direction
wrist_speed = 0

def monitor_events():
    """
    Monitor input events:
    - BTN_TR: Increase WRIST_RAW continuously while pressed
    - BTN_TL: Decrease WRIST_RAW continuously while pressed

    Pressing a button sets a speed, releasing it sets speed back to 0.
    """
    global WRIST_RAW, wrist_speed, exit_program
    try:
        for event in device.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                # event.value == 1 means button pressed, value == 0 means released
                if event.code == evdev.ecodes.BTN_TR:  # Increase wrist angle
                    if event.value == 1:
                        wrist_speed = +7  # Start rotating forward
                    elif event.value == 0:
                        wrist_speed = 0   # Stop rotating
                elif event.code == evdev.ecodes.BTN_TL: # Decrease wrist angle
                    if event.value == 1:
                        wrist_speed = -7  # Start rotating backward
                    elif event.value == 0:
                        wrist_speed = 0   # Stop rotating
    except KeyboardInterrupt:
        exit_program = True

def apply_wrist_movement():
    """
    Continuously apply the current wrist_speed to WRIST_RAW while exit_program is False.
    If wrist_speed is non-zero, WRIST_RAW changes continuously, simulating continuous motion.
    """
    global WRIST_RAW, wrist_speed, exit_program
    while not exit_program:
        if wrist_speed != 0:
            WRIST_RAW += wrist_speed
            # Clamp WRIST_RAW within [0, 1000]
            WRIST_RAW = max(0, min(WRIST_RAW, 1000))
        sleep(0.05)

def get_wrist_value():
    """
    Convert the raw wrist rotation value (WRIST_RAW) [0,1000] into a PWM duty cycle range.
    Adjust the output range [2,12] as needed for your servo’s specifications.
    """
    global WRIST_RAW
    return np.interp(WRIST_RAW, [0, 1000], [2, 12])

# Start the event monitoring thread
event_thread = threading.Thread(target=monitor_events, daemon=True)
event_thread.start()

# Start the movement application thread
movement_thread = threading.Thread(target=apply_wrist_movement, daemon=True)
movement_thread.start()

if __name__ == "__main__":
    try:
        while not exit_program:
            # Debugging: print the current mapped wrist value
            wrist_value = get_wrist_value()
            print(f"Wrist Mapped Value: {wrist_value:.2f}")
            sleep(0.1)
    except KeyboardInterrupt:
        exit_program = True
        event_thread.join()
        movement_thread.join()
        print("Wrist Rotation Scaler exited.")
