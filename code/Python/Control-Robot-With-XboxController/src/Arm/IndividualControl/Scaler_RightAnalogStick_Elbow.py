import evdev
from time import sleep
import threading
import numpy as np

# Adjust event file as needed
device = evdev.InputDevice('/dev/input/event4')  # Replace with your specific event file
print(f"Device (Elbow): {device.path}, Name: {device.name}, Phys: {device.phys}")

ELBOW_RAW = 980
current_value = 32768
DEAD_ZONE = 1000
exit_program = False

def update_elbow_raw():
    """Continuously adjust ELBOW_RAW based on the right analog stick."""
    global ELBOW_RAW, current_value, exit_program
    while not exit_program:
        if abs(current_value - 32768) > DEAD_ZONE:
            if current_value > 42768:  
                if current_value > 60535:  
                    ELBOW_RAW -= 7
                elif current_value > 51652: 
                    ELBOW_RAW -= 3
                else:                      
                    ELBOW_RAW -= 1
            elif current_value < 22768: 
                if current_value < 5000:  
                    ELBOW_RAW += 7
                elif current_value < 13883:
                    ELBOW_RAW += 3
                else:
                    ELBOW_RAW += 1

        # Keep ELBOW_RAW within [0, 1000]
        ELBOW_RAW = max(0, min(ELBOW_RAW, 1000))
        sleep(0.05)

def monitor_events():
    """Monitor events for the right analog stick (Elbow)."""
    global current_value, exit_program
    try:
        for event in device.read_loop():
            if event.type == evdev.ecodes.EV_ABS and event.code == evdev.ecodes.ABS_RZ:
                current_value = event.value
    except KeyboardInterrupt:
        exit_program = True

def get_elbow_value():
    global ELBOW_RAW
    # Map [0,1000] → [2,10.8] for Elbow based on your servo range
    return np.interp(ELBOW_RAW, [0, 1000], [500, 2500])

# Start threads
elbow_thread = threading.Thread(target=update_elbow_raw, daemon=True)
event_thread = threading.Thread(target=monitor_events, daemon=True)
elbow_thread.start()
event_thread.start()

if __name__ == "__main__":
    try:
        while True:
            # Debugging: print the current mapped elbow value
            #print(f"Elbow Mapped Value: {get_elbow_value():.2f}")
            sleep(0.1)
    except KeyboardInterrupt:
        exit_program = True
        elbow_thread.join()
        event_thread.join()
        print("Elbow Scaler exited.")
