import threading
from time import sleep
from Scaler_LeftAnalogStick_XboxBoxController import get_z_value
from Scaler_RightAnalogStick_XboxBoxController import get_y_value
from InverseKinematics import moveToPos

# Global variables for Z and Y values
z_value = 500  # Initial Z-axis position
y_value = 500  # Initial Y-axis position
exit_program = False  # Flag to stop threads

# Function to continuously fetch Z value
def update_z():
    global z_value, exit_program
    while not exit_program:
        try:
            z_value = get_z_value()  # Fetch Z value
            print(f"Z Value: {z_value:.2f} mm")  # Debugging
        except Exception as e:
            print(f"Error fetching Z value: {e}")
        sleep(0.05)

# Function to continuously fetch Y value
def update_y():
    global y_value, exit_program
    while not exit_program:
        try:
            y_value = get_y_value()  # Fetch Y value
            print(f"Y Value: {y_value:.2f} mm")  # Debugging
        except Exception as e:
            print(f"Error fetching Y value: {e}")
        sleep(0.05)

# Main function to run the threads
def main():
    global exit_program

    try:
        # Create threads to fetch Z and Y values
        thread_z = threading.Thread(target=update_z, daemon=True)
        thread_y = threading.Thread(target=update_y, daemon=True)
        thread_z.start()
        thread_y.start()

        # Main loop to calculate angles
        while not exit_program:
            try:
                # Pass Z and Y values to calculate angles
                base_angle, arm1_angle, arm2_angle = moveToPos(0, y_value, z_value)
                print(f"Base: {base_angle:.2f}°, Shoulder: {arm1_angle:.2f}°, Elbow: {arm2_angle:.2f}°")
            except ValueError as e:
                print(f"Error in angle calculation: {e}")
            sleep(0.05)  # Adjust responsiveness here

    except KeyboardInterrupt:
        print("Exiting program...")
        exit_program = True  # Signal threads to stop

    finally:
        thread_z.join()
        thread_y.join()
        print("Program exited.")

if __name__ == "__main__":
    main()
