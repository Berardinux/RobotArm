import threading
from time import sleep
import pigpio
import numpy as np
from WristControl import get_wrist_value, exit_program
from HandControl import get_hand_value  # Import hand control function

# GPIO pins for the wrist and hand servos
WRIST_PIN = 16
HAND_PIN = 26

# Connect to pigpio daemon
pi = pigpio.pi()
if not pi.connected:
    print("Failed to connect to pigpio daemon.")
    exit(1)

def main():
    global exit_program
    exit_program = False

    try:
        # Main loop to continuously update the servos based on input
        while not exit_program:
            # Retrieve the current duty cycle-like values (e.g., [2,12]) for wrist and hand
            wrist_value = get_wrist_value()  # For example [2,12]
            hand_value = get_hand_value()    # For example [2,10.8] or similar range

            # Debugging prints (optional)
            print(f"Wrist Duty Cycle-like: {wrist_value:.2f}, Hand Duty Cycle-like: {hand_value:.2f}")

            # Map these duty-cycle-like values to pulse widths in microseconds.
            # Adjust these mappings as needed for your specific servo travel range.
            # Example: Map [2,12] to [1000,2000] µs, and [2,10.8] similarly.
            
            # For wrist:
            wrist_pulse = np.interp(wrist_value, [2, 12], [500, 2500])
            # For hand:
            hand_pulse = np.interp(hand_value, [2, 10.8], [500, 2500])

            # Debugging (optional):
            #print(f"Wrist Pulse: {wrist_pulse}µs, Hand Pulse: {hand_pulse}µs")

            # Set servo pulsewidths using pigpio
            pi.set_servo_pulsewidth(WRIST_PIN, wrist_pulse)
            pi.set_servo_pulsewidth(HAND_PIN, hand_pulse)

            sleep(0.05)

    except KeyboardInterrupt:
        print("Exiting program...")
        exit_program = True
    finally:
        # Stop sending pulses to the servos by setting pulsewidth to 0
        pi.set_servo_pulsewidth(WRIST_PIN, 0)
        pi.set_servo_pulsewidth(HAND_PIN, 0)
        pi.stop()  # Disconnect from pigpio
        print("Program exited.")

if __name__ == "__main__":
    main()
