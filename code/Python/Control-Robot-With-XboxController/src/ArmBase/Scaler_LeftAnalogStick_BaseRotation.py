import evdev
from time import sleep
import threading
import numpy as np

# Adjust the event file as needed for your specific device
device = evdev.InputDevice('/dev/input/event4')  # Replace with your specific event file
print(f"Device (Base Rotation): {device.path}, Name: {device.name}, Phys: {device.phys}")

BASE_RAW = 150   # Initial raw base rotation value (0-1000 range)
current_value = 32768  # Neutral stick position
DEAD_ZONE = 1000
exit_program = False

def update_base_raw():
    """
    Continuously adjust the BASE_RAW value based on the left analog stick input.
    This raw value (0-1000) will later be mapped to a servo-friendly duty cycle range.
    """
    global BASE_RAW, current_value, exit_program
    while not exit_program:
        # Only update if stick movement exceeds the dead zone
        if abs(current_value - 32768) > DEAD_ZONE:
            # Determine direction and speed of adjustment based on stick value
            if current_value > 42768:  # Stick pushed in one direction (e.g., backward)
                if current_value > 60535:
                    BASE_RAW -= 7
                elif current_value > 51652:
                    BASE_RAW -= 3
                else:
                    BASE_RAW -= 1
            elif current_value < 22768:  # Stick pushed in the opposite direction (e.g., forward)
                if current_value < 5000:
                    BASE_RAW += 7
                elif current_value < 13883:
                    BASE_RAW += 3
                else:
                    BASE_RAW += 1

        # Clamp BASE_RAW within [0, 1000]
        BASE_RAW = max(0, min(BASE_RAW, 1000))
        sleep(0.05)

def monitor_events():
    """
    Monitor the input events from the device to update 'current_value'
    based on the left analog stick’s horizontal axis (ABS_X).
    """
    global current_value, exit_program
    try:
        for event in device.read_loop():
            if event.type == evdev.ecodes.EV_ABS and event.code == evdev.ecodes.ABS_X:
                current_value = event.value
    except KeyboardInterrupt:
        exit_program = True

def get_base_value():
    """
    Convert the raw base rotation value (BASE_RAW) [0,1000] into a PWM duty cycle range.
    Adjust the output range [2, 12] as needed for your servo’s specifications.
    """
    global BASE_RAW
    return np.interp(BASE_RAW, [0, 1000], [2, 12])

# Start threads to update base rotation and monitor events
base_thread = threading.Thread(target=update_base_raw, daemon=True)
event_thread = threading.Thread(target=monitor_events, daemon=True)
base_thread.start()
event_thread.start()

if __name__ == "__main__":
    try:
        while True:
            # Debugging: print the current mapped base rotation value in duty cycle form
            #print(f"Base Mapped Value: {get_base_value():.2f}")
            sleep(0.1)
    except KeyboardInterrupt:
        exit_program = True
        base_thread.join()
        event_thread.join()
        print("Base Rotation Scaler exited.")
