import threading
from time import sleep
import pigpio
import numpy as np
from Scaler_LeftAnalogStick_BaseRotation import get_base_value

# Global variables
base_value = 500  # Initial base position (0-1000 range, mapped to servo duty cycle)
exit_program = False  # Flag to stop threads

# Servo GPIO pin for base rotation
BASE_PIN = 12

# Connect to pigpio daemon
pi = pigpio.pi()
if not pi.connected:
    print("Failed to connect to pigpio daemon.")
    exit(1)

def update_base():
    """
    Continuously fetch and update the base rotation value using the left analog stick.
    The get_base_value() function returns a duty cycle-like value (e.g., [2,12]).
    We'll map this later to a pulse width for the servo.
    """
    global base_value, exit_program
    while not exit_program:
        try:
            base_value = get_base_value()
            print(f"Base Rotation Value (duty-like): {base_value:.2f}")  # Debugging
        except Exception as e:
            print(f"Error fetching base rotation value: {e}")
        sleep(0.05)

def main():
    global exit_program
    exit_program = False

    # Start the thread to update the base rotation value
    thread_base = threading.Thread(target=update_base, daemon=True)
    thread_base.start()

    try:
        # Main loop to apply the base_value to the servo via pigpio
        while not exit_program:
            try:
                # Example mapping: If base_value is in [2,12], map it to [1000,2000] µs pulse width
                # Adjust the range as needed for your servo.
                base_pulse = np.interp(base_value, [2, 12], [1000, 2000])
                
                # Debugging print (optional):
                #print(f"Base Pulse Width: {base_pulse} µs")

                # Set the servo pulse width using pigpio
                pi.set_servo_pulsewidth(BASE_PIN, base_pulse)

            except ValueError as e:
                print(f"Error updating servo pulse width: {e}")
            sleep(0.05)

    except KeyboardInterrupt:
        print("Exiting program...")
        exit_program = True

    finally:
        thread_base.join()
        # Stop sending pulses to the servo by setting pulsewidth to 0
        pi.set_servo_pulsewidth(BASE_PIN, 0)
        pi.stop()  # Disconnect from pigpio
        print("Program exited.")

if __name__ == "__main__":
    main()
