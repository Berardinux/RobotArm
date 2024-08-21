import RPi.GPIO as GPIO
from time import sleep
import threading
import math
import os

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.OUT)  # Middle arm
GPIO.setup(21, GPIO.OUT)  # Bottom arm

# Initialize servos
middle_servo = GPIO.PWM(20, 50)
bottom_servo = GPIO.PWM(21, 50)
middle_servo.start(0)
bottom_servo.start(0)
rotation_home = 7.15
bottom_home = 3.2
middle_home = 10.8

def Ramp(servo, OldDutyCycle, NewDutyCycle):
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

# Function to calculate angles
def calculate_angles(x, y, L):
    # Inverse kinematics calculations
    theta2 = math.acos((x**2 + y**2 - 2*L**2) / (2 * L**2))
    theta1 = math.atan2(y, x) - math.atan2(L * math.sin(theta2), L + L * math.cos(theta2))
    
    # Convert radians to degrees
    theta1_deg = math.degrees(theta1)
    theta2_deg = math.degrees(theta2)
    
    return theta1_deg, theta2_deg

# Convert angles to duty cycles
def angle_to_duty_cycle(angle):
    # Example conversion, needs to be calibrated for your servos
    return 2 + (angle / 180) * 10

# Home position in terms of x, y coordinates
x_home = -5  # Set this to your desired home x-coordinate
y_home = -5  # Set this to your desired home y-coordinate
L = 10  # Length of each arm segment (assuming both arms have the same length)

# Calculate the angles for the home position
theta1_deg, theta2_deg = calculate_angles(x_home, y_home, L)

# Convert angles to duty cycles
bottom_duty_cycle = angle_to_duty_cycle(theta1_deg)
middle_duty_cycle = angle_to_duty_cycle(theta2_deg)

# Move both arms to the home position
try:
    threading.Thread(target=Ramp, args=(middle_servo, middle_home, middle_duty_cycle)).start()
    threading.Thread(target=Ramp, args=(bottom_servo, bottom_home, bottom_duty_cycle)).start()
    sleep(2)

finally:
    middle_servo.stop()
    bottom_servo.stop()
    GPIO.cleanup()
    print(f"{bottom_duty_cycle} {middle_duty_cycle}")
    os.system(f"python3 ServoHome.py 7.15 {bottom_duty_cycle} {middle_duty_cycle}")

