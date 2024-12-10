import evdev
from time import sleep
import threading
import numpy as np

# Adjust the event file as needed for your specific device
device = evdev.InputDevice('/dev/input/event4')  # Replace with your specific event file
print(f"Device (Hand): {device.path}, Name: {device.name}, Phys: {device.phys}")

HAND_RAW = 980  # Initial raw hand position (0-1000 range)
exit_program = False

def map_value(x, in_min, in_max, out_min, out_max):
    """
    Map a value x from range [in_min, in_max] to [out_min, out_max].
    """
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def monitor_events():
    """
    Monitor input events for triggers:
    - ABS_GAS: opening the hand (decrease HAND_RAW)
    - ABS_BRAKE: closing the hand (increase HAND_RAW)
    Each trigger value is 0 to 1023, mapped to speed [0, 10].
    """
    global HAND_RAW, exit_program
    try:
        for event in device.read_loop():
            if event.type == evdev.ecodes.EV_ABS:
                if event.code == evdev.ecodes.ABS_GAS:
                    # Map trigger value [0,1023] to speed [0,10]
                    openSpeed = round(map_value(event.value, 0, 1023, 0, 10))
                    HAND_RAW -= openSpeed
                elif event.code == evdev.ecodes.ABS_BRAKE:
                    closeSpeed = round(map_value(event.value, 0, 1023, 0, 10))
                    HAND_RAW += closeSpeed

                # Clamp HAND_RAW within [0, 1000]
                HAND_RAW = max(0, min(HAND_RAW, 1000))
    except KeyboardInterrupt:
        exit_program = True

def get_hand_value():
    """
    Convert the raw hand position (HAND_RAW [0,1000]) into a PWM duty cycle range.
    Adjust [2,10.8] as needed for your servo's specifications.
    """
    global HAND_RAW
    return np.interp(HAND_RAW, [0, 1000], [2, 10.8])

# Start the event monitoring thread
event_thread = threading.Thread(target=monitor_events, daemon=True)
event_thread.start()

if __name__ == "__main__":
    try:
        while not exit_program:
            # Debugging: print the current mapped hand value (duty cycle)
            hand_value = get_hand_value()
            print(f"Hand Duty Cycle: {hand_value:.2f}")
            sleep(0.1)
    except KeyboardInterrupt:
        exit_program = True
        event_thread.join()
        print("Hand control exited.")
