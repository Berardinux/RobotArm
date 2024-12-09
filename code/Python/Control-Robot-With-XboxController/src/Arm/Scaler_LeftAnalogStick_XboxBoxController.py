import evdev
from time import sleep
import threading
import numpy as np

# Open the event file for your input device (change to your specific event number)
device = evdev.InputDevice('/dev/input/event25')  # Replace with your specific event file
print(f"Device: {device.path}, Name: {device.name}, Phys: {device.phys}")

Z = 500  # Initial Z-axis position
current_value = 32768  # Current analog stick position (neutral value)
DEAD_ZONE = 1000  # Define a dead zone for minor stick movements
exit_program = False  # Flag to stop threads

def update_z():
    """Continuously adjust Z based on the analog stick value."""
    global Z, current_value, exit_program
    while not exit_program:
        if abs(current_value - 32768) > DEAD_ZONE:
            if current_value > 42768:  # Stick pulled backward
                if current_value > 60535:  # Fast speed
                    Z -= 7
                elif current_value > 51652:  # Medium speed
                    Z -= 3
                else:  # Slow speed
                    Z -= 1
            elif current_value < 22768:  # Stick pushed forward
                if current_value < 5000:  # Fast speed
                    Z += 7
                elif current_value < 13883:  # Medium speed
                    Z += 3
                else:  # Slow speed
                    Z += 1

        # Keep Z within bounds
        Z = max(0, min(Z, 1000))
        sleep(0.05)  # Adjust as needed for smoother response

def monitor_events():
    """Monitor events to update the current analog stick value."""
    global current_value, exit_program
    try:
        for event in device.read_loop():
            if event.type == evdev.ecodes.EV_ABS:
                if event.code == evdev.ecodes.ABS_Y:  # Change this to the correct axis for left stick
                    current_value = event.value
    except KeyboardInterrupt:
        exit_program = True

# Function to return the mapped Z value as z_coordinates
def get_z_value():
    global Z
    # Map Z from [0, 1000] to [0, 10]
    z_coordinates = np.interp(Z, [0, 1000], [0, 530])
    return z_coordinates

# Start threads
z_thread = threading.Thread(target=update_z, daemon=True)
monitor_thread = threading.Thread(target=monitor_events, daemon=True)

z_thread.start()
monitor_thread.start()

if __name__ == "__main__":
    try:
        while True:
            # Debugging: print the current mapped Z value
            print(f"Z Coordinates: {get_z_value()}")
            sleep(0.1)
    except KeyboardInterrupt:
        exit_program = True
        z_thread.join()
        monitor_thread.join()
        print("Program exited.")
