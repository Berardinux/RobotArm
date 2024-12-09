import evdev
from time import sleep
import threading

# Open the event file for your input device (change to your specific event number)
device = evdev.InputDevice('/dev/input/event4')  # Replace with your specific event file
print(device)

Z = 50
incrementing = False
decrementing = False

def increment_z():
  global Z
  while True:
    if incrementing:
      Z += 1
      Z = max(0, min(Z, 1000))  # Keep Z within bounds
      print(f"Current Z (incrementing): {Z}")
    elif decrementing:
      Z -= 1
      Z = max(0, min(Z, 1000))  # Keep Z within bounds
      print(f"Current Z (decrementing): {Z}")
    sleep(0.1)  # Control the rate of change

# Start a thread to continuously update Z
z_thread = threading.Thread(target=increment_z)
z_thread.daemon = True  # This makes sure the thread exits when the main program does
z_thread.start()

try:
  for event in device.read_loop():
    if event.type == evdev.ecodes.EV_ABS:
      if event.code == evdev.ecodes.ABS_Y:
        current_value = event.value
        
        # Update flags based on the current value
        if current_value > 34768:  # Stick pushed forward
          incrementing = True
          decrementing = False
        elif current_value < 30768:  # Stick pulled backward
          incrementing = False
          decrementing = True
        else:  # Neutral position
          incrementing = False
          decrementing = False

        # Print the event value for debugging
        print(f"Analog Value: {current_value}")

    sleep(0.01)  # Short delay before the next loop iteration

except KeyboardInterrupt:
  pass
finally:
  exit()