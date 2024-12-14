import evdev
from time import sleep
import threading
import numpy as np

# Adjust event file as needed
device = evdev.InputDevice('/dev/input/event4')  # Replace with your specific event file
print(f"Device (Shoulder): {device.path}, Name: {device.name}, Phys: {device.phys}")

SHOULDER_RAW = 226   # Initial shoulder raw position
current_value = 32768
DEAD_ZONE = 1000
exit_program = False

def update_shoulder_raw():
    """Continuously adjust SHOULDER_RAW based on the left analog stick."""
    global SHOULDER_RAW, current_value, exit_program
    while not exit_program:
        if abs(current_value - 32768) > DEAD_ZONE:
            if current_value > 42768:  # Stick pulled backward
                if current_value > 60535:  
                    SHOULDER_RAW -= 7
                elif current_value > 51652: 
                    SHOULDER_RAW -= 3
                else:                      
                    SHOULDER_RAW -= 1
            elif current_value < 22768:  # Stick pushed forward
                if current_value < 5000: 
                    SHOULDER_RAW += 7
                elif current_value < 13883:
                    SHOULDER_RAW += 3
                else:
                    SHOULDER_RAW += 1

        # Keep SHOULDER_RAW within [0, 1000]
        SHOULDER_RAW = max(0, min(SHOULDER_RAW, 1000))
        sleep(0.05)

def monitor_events():
    """Monitor events for the left analog stick (Shoulder)."""
    global current_value, exit_program
    try:
        for event in device.read_loop():
            if event.type == evdev.ecodes.EV_ABS and event.code == evdev.ecodes.ABS_Y:
                current_value = event.value
    except KeyboardInterrupt:
        exit_program = True

def get_shoulder_value():
    global SHOULDER_RAW
    # Map [0,1000] → [2,8.5] for Shoulder based on your servo range
    return np.interp(SHOULDER_RAW, [0, 1000], [500, 2500])

# Start threads
shoulder_thread = threading.Thread(target=update_shoulder_raw, daemon=True)
event_thread = threading.Thread(target=monitor_events, daemon=True)
shoulder_thread.start()
event_thread.start()

if __name__ == "__main__":
    try:
        while True:
            # Debugging: print the current mapped shoulder value
            #print(f"Shoulder Mapped Value: {get_shoulder_value():.2f}")
            sleep(0.1)
    except KeyboardInterrupt:
        exit_program = True
        shoulder_thread.join()
        event_thread.join()
        print("Shoulder Scaler exited.")
