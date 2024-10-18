# robot_arm.py
import RPi.GPIO as GPIO
import threading
from time import sleep
import math

class RobotArm:
    def __init__(self):
        # Setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(20, GPIO.OUT)  # Middle arm
        GPIO.setup(21, GPIO.OUT)  # Bottom arm

        self.middle_servo = GPIO.PWM(20, 50)
        self.bottom_servo = GPIO.PWM(21, 50)
        self.middle_servo.start(0)  
        self.bottom_servo.start(0)  

        # Home position angles (Z value from controller will replace x_home)
        self.rotation_home = 7.15
        self.bottom_home = 3.2
        self.middle_home = 10.8

        # Limits
        self.bottom_min = 2.0
        self.bottom_max = 8.5
        self.middle_min = 3.2
        self.middle_max = 10.8

    def Ramp(self, servo, OldDutyCycle, NewDutyCycle):
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
        duty_cycle = 2 + (angle / 180) * 10  # Example conversion formula
        return duty_cycle

    def move_arm(self, x_home):
        # x_home will now be Z value from Controller
        theta1_deg, theta2_deg = self.calculate_angles(x_home, 10, 10)
        if theta1_deg is None or theta2_deg is None:
            return

        bottom_duty_cycle = self.angle_to_duty_cycle(theta1_deg)
        middle_duty_cycle = self.angle_to_duty_cycle(theta2_deg)

        bottom_duty_cycle = max(self.bottom_min, min(self.bottom_max, bottom_duty_cycle))
        middle_duty_cycle = max(self.middle_min, min(self.middle_max, middle_duty_cycle))

        thread_middle = threading.Thread(target=self.Ramp, args=(self.middle_servo, self.middle_home, middle_duty_cycle))
        thread_bottom = threading.Thread(target=self.Ramp, args=(self.bottom_servo, self.bottom_home, bottom_duty_cycle))
        thread_middle.start()
        thread_bottom.start()
        thread_middle.join()
        thread_bottom.join()

    def calculate_angles(self, x, y, L):
        try:
            value = (x**2 + y**2 - 2*L**2) / (2 * L**2)
            value = max(min(value, 1), -1)
            theta2 = math.acos(value)

            theta1 = math.atan2(y, x) - math.atan2(L * math.sin(theta2), L + L * math.cos(theta2))

            theta1_deg = math.degrees(theta1)
            theta2_deg = math.degrees(theta2)

            return theta1_deg, theta2_deg

        except ValueError:
            print("Error in calculating angles: values out of range")
            return None, None

    def cleanup(self):
        self.middle_servo.stop()
        self.bottom_servo.stop()
        GPIO.cleanup()
