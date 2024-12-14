import threading
import pigpio
from time import sleep
from .X_Scaler import get_x_value, start_x_updates, set_x_locks
from .Y_Scaler import get_y_value, start_y_updates, set_y_locks
from .InverseKinematics import moveToPos, SHOULDER_LENGTH, ELBOW_LENGTH

SHOULDER_PIN = 21
ELBOW_PIN = 20
exit_program = False
main_thread = None

old_shoulder_pwm = 1200
old_elbow_pwm = 1200

def main():
    global exit_program, old_shoulder_pwm, old_elbow_pwm

    # Initialize pigpio here (fresh each time main runs)
    pi = pigpio.pi()
    if not pi.connected:
        print("Failed to connect to pigpio daemon.")
        return

    try:
        x_update_thread = threading.Thread(target=start_x_updates, daemon=True)
        y_update_thread = threading.Thread(target=start_y_updates, daemon=True)
        x_update_thread.start()
        y_update_thread.start()

        max_reach = SHOULDER_LENGTH + ELBOW_LENGTH

        while not exit_program:
            x_val = get_x_value()
            y_val = get_y_value()

            result = moveToPos(x_val, y_val)
            if result is None:
                shoulder_angle, elbow_angle, shoulder_pwm, elbow_pwm = None, None, None, None
            else:
                shoulder_angle, elbow_angle, shoulder_pwm, elbow_pwm = result

            out_of_range = (shoulder_angle is None or elbow_angle is None)
            radius = (x_val**2 + y_val**2)**0.5

            if out_of_range and radius > max_reach:
                x_lock_positive = (x_val > 0)
                x_lock_negative = (x_val < 0)
                y_lock_positive = (y_val > 0)
                y_lock_negative = (y_val < 0)
                set_x_locks(x_lock_positive, x_lock_negative)
                set_y_locks(y_lock_positive, y_lock_negative)
            else:
                set_x_locks(False, False)
                set_y_locks(False, False)

            if not out_of_range and shoulder_pwm is not None and elbow_pwm is not None:
                pi.set_servo_pulsewidth(SHOULDER_PIN, shoulder_pwm)
                pi.set_servo_pulsewidth(ELBOW_PIN, elbow_pwm)
                print(f"(X: {x_val}, Y: {y_val}) // Shoulder angle: {shoulder_angle} // Elbow angle: {elbow_angle} // SPW {shoulder_pwm} // EPW {elbow_pwm}")
                old_shoulder_pwm = shoulder_pwm
                old_elbow_pwm = elbow_pwm
            else:
                pi.set_servo_pulsewidth(SHOULDER_PIN, old_shoulder_pwm)
                pi.set_servo_pulsewidth(ELBOW_PIN, old_elbow_pwm)
                print(f"(X: {x_val}, Y: {y_val}) // SPW {old_shoulder_pwm} // EPW {old_elbow_pwm} - Out of range, no valid servo command")

            sleep(0.01)

    except KeyboardInterrupt:
        print("Exiting program...")
        exit_program = True
    finally:
        # Reset locks
        set_x_locks(False, False)
        set_y_locks(False, False)

        # Stop servos
        pi.set_servo_pulsewidth(SHOULDER_PIN, 0)
        pi.set_servo_pulsewidth(ELBOW_PIN, 0)
        pi.stop()
        print("Program exited.")

def get_positions():
    global old_shoulder_pwm, old_elbow_pwm
    return old_shoulder_pwm, old_elbow_pwm

def start():
    global main_thread, exit_program
    exit_program = False
    main_thread = threading.Thread(target=main, daemon=True)
    main_thread.start()

def stop():
    global exit_program, main_thread
    exit_program = True
    if main_thread is not None:
        main_thread.join()
        main_thread = None
