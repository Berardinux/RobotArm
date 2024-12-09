import evdev
from time import sleep
import threading
import numpy as np

# Open the event file for your input device (change to your specific event number)
device = evdev.InputDevice('/dev/input/event25')  # Replace with your specific event file
print(f"Device: {device.path}, Name: {device.name}, Phys: {device.phys}")

Y = 500  # Initial Y-axis position
current_value = 32768  # Current analog stick position (neutral value)
DEAD_ZONE = 1000  # Define a dead zone for minor stick movements
exit_program = False  # Flag to stop threads

def update_y():
    """Continuously adjust Y based on the analog stick value."""
    global Y, current_value, exit_program
    while not exit_program:
        # Skip updates if the stick is in the dead zone
        if abs(current_value - 32768) > DEAD_ZONE:
            if current_value > 42768:  # Stick pulled backward
                if current_value > 60535:  # Fast speed
                    Y -= 7
                elif current_value > 51652:  # Medium speed
                    Y -= 3
                else:  # Slow speed
                    Y -= 1
            elif current_value < 22768:  # Stick pushed forward
                if current_value < 5000:  # Fast speed
                    Y += 7
                elif current_value < 13883:  # Medium speed
                    Y += 3
                else:  # Slow speed
                    Y += 1

        # Keep Y within bounds
        Y = max(0, min(Y, 1000))
        sleep(0.05)  # Adjust as needed for smoother response

def monitor_events():
    """Monitor events to update the current analog stick value."""
    global current_value, exit_program
    try:
        for event in device.read_loop():
            if event.type == evdev.ecodes.EV_ABS:
                if event.code == evdev.ecodes.ABS_RZ:  # Right analog stick's vertical axis
                    current_value = event.value
    except KeyboardInterrupt:
        exit_program = True

# Function to return the mapped Y value as y_coordinates
def get_y_value():
    global Y
    # Map Y from [0, 1000] to [0, 10]
    y_coordinates = np.interp(Y, [0, 1000], [0, 530])
    return y_coordinates

# Start threads
y_thread = threading.Thread(target=update_y, daemon=True)
event_thread = threading.Thread(target=monitor_events, daemon=True)

y_thread.start()
event_thread.start()

if __name__ == "__main__":
    try:
        while True:
            # Debugging: print the current mapped Y value
            print(f"Y Coordinates: {get_y_value()}")
            sleep(0.1)
    except KeyboardInterrupt:
        exit_program = True
        y_thread.join()
        event_thread.join()
        print("Program exited.")
