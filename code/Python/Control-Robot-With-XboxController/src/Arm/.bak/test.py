import evdev
import threading
import RPi.GPIO as GPIO
from time import sleep
import math

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
                        
                        # Update flags based on the current value
                        if current_value > 34768:  # Stick pushed forward
                            self.incrementing = True
                            self.decrementing = False
                        elif current_value < 30768:  # Stick pulled backward
                            self.incrementing = False
                            self.decrementing = True
                        else:  # Neutral position
                            self.incrementing = False
                            self.decrementing = False

                        # Print the event value for debugging
                        print(f"Analog Value: {current_value}")

                sleep(0.01)  # Short delay before the next loop iteration

        except KeyboardInterrupt:
            pass
        finally:
            exit()


class RobotArm:
    def __init__(self):
        # Setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(20, GPIO.OUT)  # Middle arm
        GPIO.setup(21, GPIO.OUT)  # Bottom arm

        # Initialize servos
        self.middle_servo = GPIO.PWM(20, 50)
        self.bottom_servo = GPIO.PWM(21, 50)
        self.middle_servo.start(0)  # Start at 0 duty cycle
        self.bottom_servo.start(0)  # Start at 0 duty cycle

        # Home position angles
        self.rotation_home = 7.15
        self.bottom_home = 3.2
        self.middle_home = 10.8

        # Limits
        self.bottom_min = 2.0
        self.bottom_max = 8.5
        self.middle_min = 3.2
        self.middle_max = 10.8

    def Ramp(self, servo, OldDutyCycle, NewDutyCycle):
        # Clamp NewDutyCycle to valid range
        if NewDutyCycle < 0:
            NewDutyCycle = 0
        elif NewDutyCycle > 100:
            NewDutyCycle = 100
        
        if OldDutyCycle < NewDutyCycle:
            i = OldDutyCycle
            while i <= NewDutyCycle:
                servo.ChangeDutyCycle(i)
                i += 0.01
                sleep(0.01)
        elif OldDutyCycle > NewDutyCycle:
            i = OldDutyCycle
            while i >= NewDutyCycle:
                servo.ChangeDutyCycle(i)
                i -= 0.01
                sleep(0.01)

    def angle_to_duty_cycle(self, angle):
        # Convert an angle to a corresponding duty cycle (this will need to be calibrated for your servos)
        duty_cycle = 2 + (angle / 180) * 10  # Example conversion formula
        return duty_cycle

    def move_arm(self, z_value):
        # Example movement logic using Z value
        # Calculate angles based on Z
        theta1_deg, theta2_deg = self.calculate_angles(z_value, 10, 10)
        if theta1_deg is None or theta2_deg is None:
            return  # Skip if angles are not valid

        bottom_duty_cycle = self.angle_to_duty_cycle(theta1_deg)
        middle_duty_cycle = self.angle_to_duty_cycle(theta2_deg)

        # Clamp duty cycles to within servo limits
        bottom_duty_cycle = max(self.bottom_min, min(self.bottom_max, bottom_duty_cycle))
        middle_duty_cycle = max(self.middle_min, min(self.middle_max, middle_duty_cycle))

        # Move servos
        thread_middle = threading.Thread(target=self.Ramp, args=(self.middle_servo, self.middle_home, middle_duty_cycle))
        thread_bottom = threading.Thread(target=self.Ramp, args=(self.bottom_servo, self.bottom_home, bottom_duty_cycle))
        thread_middle.start()
        thread_bottom.start()
        thread_middle.join()
        thread_bottom.join()

    def calculate_angles(self, x, y, L):
        try:
            # Ensure the value inside acos is clamped between -1 and 1
            value = (x**2 + y**2 - 2*L**2) / (2 * L**2)
            value = max(min(value, 1), -1)  # Clamp to [-1, 1]
            theta2 = math.acos(value)
            
            theta1 = math.atan2(y, x) - math.atan2(L * math.sin(theta2), L + L * math.cos(theta2))
            
            # Convert radians to degrees
            theta1_deg = math.degrees(theta1)
            theta2_deg = math.degrees(theta2)
            
            return theta1_deg, theta2_deg
        
        except ValueError:
            print("Error in calculating angles: values out of range")
            return None, None

    def cleanup(self):
        # Cleanup GPIO resources when done
        self.middle_servo.stop()
        self.bottom_servo.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    controller = Controller('/dev/input/event4')
    robot_arm = RobotArm()

    try:
        while True:
            # Move the robot arm based on the Z value from the controller
            if controller.Z is not None:  # Ensure Z is valid
                robot_arm.move_arm(controller.Z)
            sleep(0.5)
    except KeyboardInterrupt:
        pass
    finally:
        robot_arm.cleanup()
