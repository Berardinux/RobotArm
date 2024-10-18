# controller.py
import evdev
import threading
from time import sleep

class Controller:
    def __init__(self, event_file):
        self.device = evdev.InputDevice(event_file)
        print(f"Controller initialized: {self.device}")
        self.Z = 50
        self.incrementing = False
        self.decrementing = False
        self.z_thread = threading.Thread(target=self.increment_z)
        self.z_thread.daemon = True
        self.z_thread.start()

    def increment_z(self):
        while True:
            if self.incrementing:
                self.Z += 1
                self.Z = max(0, min(self.Z, 1000))  # Keep Z within bounds
                print(f"Current Z (incrementing): {self.Z}")
            elif self.decrementing:
                self.Z -= 1
                self.Z = max(0, min(self.Z, 1000))  # Keep Z within bounds
                print(f"Current Z (decrementing): {self.Z}")
            sleep(0.1)  # Control the rate of change

    def listen_for_input(self):
        try:
            for event in self.device.read_loop():
                if event.type == evdev.ecodes.EV_ABS:
                    if event.code == evdev.ecodes.ABS_Y:
                        current_value = event.value

                        if current_value > 34768:  # Stick pushed forward
                            self.incrementing = True
                            self.decrementing = False
                        elif current_value < 30768:  # Stick pulled backward
                            self.incrementing = False
                            self.decrementing = True
                        else:  # Neutral position
                            self.incrementing = False
                            self.decrementing = False

                        print(f"Analog Value: {current_value}")

                sleep(0.01)

        except KeyboardInterrupt:
            pass
        finally:
            exit()
