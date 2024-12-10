import threading
from time import sleep
import RPi.GPIO as GPIO
from Scaler_LeftAnalogStick_XboxBoxController import get_z_value
from Scaler_RightAnalogStick_XboxBoxController import get_y_value
from InverseKinematics import moveToPos
from ControlArm import convert_angles_to_pwm

# Global variables for Z and Y values
z_value = 500  # Initial Z-axis position
y_value = 500  # Initial Y-axis position
exit_program = False  # Flag to stop threads

# Servo GPIO pins
SHOULDER_PIN = 21
ELBOW_PIN = 20

def update_z():
    global z_value, exit_program
    while not exit_program:
        try:
            z_value = get_z_value()  # Fetch Z value (scaled)
            print(f"Z Value: {z_value:.2f} mm")  # Debugging
        except Exception as e:
            print(f"Error fetching Z value: {e}")
        sleep(0.05)

def update_y():
    global y_value, exit_program
    while not exit_program:
        try:
            y_value = get_y_value()  # Fetch Y value (scaled)
            print(f"Y Value: {y_value:.2f} mm")  # Debugging
        except Exception as e:
            print(f"Error fetching Y value: {e}")
        sleep(0.05)

def initialize_servos():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SHOULDER_PIN, GPIO.OUT)
    GPIO.setup(ELBOW_PIN, GPIO.OUT)
    shoulder_servo = GPIO.PWM(SHOULDER_PIN, 50)  # 50 Hz frequency
    elbow_servo = GPIO.PWM(ELBOW_PIN, 50)        # 50 Hz frequency
    shoulder_servo.start(0)
    elbow_servo.start(0)
    return shoulder_servo, elbow_servo

def main():
    global exit_program

    # Initialize servos
    shoulder_servo, elbow_servo = initialize_servos()

    try:
        # Create threads to fetch Z and Y values
        thread_z = threading.Thread(target=update_z, daemon=True)
        thread_y = threading.Thread(target=update_y, daemon=True)
        thread_z.start()
        thread_y.start()

        # Main loop to calculate angles and drive servos
        while not exit_program:
            try:
                # Calculate angles from inverse kinematics
                base_angle, arm1_angle, arm2_angle = moveToPos(0, y_value, z_value)
                print(f"Base: {base_angle:.2f}°, Shoulder: {arm1_angle:.2f}°, Elbow: {arm2_angle:.2f}°")

                # Convert shoulder and elbow angles to PWM signals
                shoulder_pwm, elbow_pwm = convert_angles_to_pwm(arm1_angle, arm2_angle)
                print(f"Shoulder PWM: {shoulder_pwm:.2f}, Elbow PWM: {elbow_pwm:.2f}")

                # Note: If your servo expects duty cycles in a certain range (like 2%-12%),
                # and the PWM values are not in that range, you may need to rescale them.
                # For example, if shoulder_pwm and elbow_pwm are already in [1.7, 9.0] range,
                # that might correspond directly to duty cycles for your servo.
                # If needed, apply a mapping here:
                # duty_cycle_shoulder = map_value(shoulder_pwm, MIN_PWM, MAX_PWM, 2, 12)
                # duty_cycle_elbow = map_value(elbow_pwm, MIN_PWM, MAX_PWM, 2, 12)

                # For now, assume the PWM values from convert_angles_to_pwm are appropriate duty cycles:
                shoulder_servo.ChangeDutyCycle(shoulder_pwm)
                elbow_servo.ChangeDutyCycle(elbow_pwm)

            except ValueError as e:
                print(f"Error in angle calculation: {e}")
            sleep(0.05)

    except KeyboardInterrupt:
        print("Exiting program...")
        exit_program = True  # Signal threads to stop

    finally:
        thread_z.join()
        thread_y.join()
        shoulder_servo.stop()
        elbow_servo.stop()
        GPIO.cleanup()
        print("Program exited.")

if __name__ == "__main__":
    main()
