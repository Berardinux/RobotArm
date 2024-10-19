import evdev
import select
import signal
import sys
import time

class ControllerRightAnalog:

    def __init__(self):
        self.device = evdev.InputDevice('/dev/input/event4')  # Replace with your specific event file
        print(self.device)

        self.Y = 500  # Start in the middle of the 0-999 range
        self.stick_position = 0  # 0 for neutral, 1 for forward, -1 for backward
        self.running = True

    def map_value(self, Y, min1, max1, min2, max2):
        return ((Y - min1) / (max1 - min1)) * (max2 - min2) + min2

    def process_events(self):
        r, w, x = select.select([self.device], [], [], 0.01)
        if r:
            for event in self.device.read():
                if event.type == evdev.ecodes.EV_ABS:
                    if event.code == evdev.ecodes.ABS_RZ:  # Assuming ABS_RZ for right analog stick
                        if event.value > 34768:
                            self.stick_position = 1
                        elif event.value < 30768:
                            self.stick_position = -1
                        else:
                            self.stick_position = 0
        
        # Update Y based on stick position
        if self.stick_position == 1:
            self.Y = min(self.Y + 1, 999)
        elif self.stick_position == -1:
            self.Y = max(self.Y - 1, 0)
        
        # Map Y from 0-999 range to -10 to 10 range before returning
        return self.map_value(self.Y, 0, 999, -10, 10)

    def close(self):
        self.device.close()

def signal_handler(sig, frame):
    print("\nEYiting gracefully...")
    sys.eYit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    controller = ControllerRightAnalog()
    while controller.running:
        controller.process_events()
        print(f"Y: {controller.Y}, Stick Position: {controller.stick_position}")
        time.sleep(0.01)  # Small delay to control update rate
