import evdev
from time import sleep
import threading
import numpy as np

# Adjust the event file as needed for your specific device
device = evdev.InputDevice('/dev/input/event4')  # Replace with your specific event file
print(f"Device (Wrist Rotation): {device.path}, Name: {device.name}, Phys: {device.phys}")

WRIST_RAW = 500    # Initial raw wrist rotation value (0-1000 range)
exit_program = False

def monitor_events():
    """
    Monitor the input events from the device to update 'WRIST_RAW'
    based on button presses. For example:
    - BTN_TR: increment WRIST_RAW
    - BTN_TL: decrement WRIST_RAW
    Adjust increments as needed.
    """
    global WRIST_RAW, exit_program
    try:
        for event in device.read_loop():
            # Check if we got a key (button) event
            if event.type == evdev.ecodes.EV_KEY:
                # When button is pressed (event.value == 1)
                if event.value == 1:
                    if event.code == evdev.ecodes.BTN_TR:
                        # Increase WRIST_RAW when BTN_TR is pressed
                        WRIST_RAW += 7
                    elif event.code == evdev.ecodes.BTN_TL:
                        # Decrease WRIST_RAW when BTN_TL is pressed
                        WRIST_RAW -= 7

                    # Clamp WRIST_RAW within [0, 1000]
                    WRIST_RAW = max(0, min(WRIST_RAW, 1000))
    except KeyboardInterrupt:
        exit_program = True

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

if __name__ == "__main__":
    try:
        while not exit_program:
            # Debugging: print the current mapped wrist value
            print(f"Wrist Mapped Value: {get_wrist_value():.2f}")
            sleep(0.1)
    except KeyboardInterrupt:
        exit_program = True
        event_thread.join()
        print("Wrist Rotation Scaler exited.")
