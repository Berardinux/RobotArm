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
middle_servo.start(0)  # Start at 0 duty cycle
bottom_servo.start(0)  # Start at 0 duty cycle

# Home position angles (in degrees)
rotation_home = 7.15
bottom_home = 3.2
middle_home = 10.8

# Define travel limits for the bottom and middle servos
bottom_min = 2.0
bottom_max = 8.5
middle_min = 3.2
middle_max = 10.8

def Ramp(servo, OldDutyCycle, NewDutyCycle):
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

# Function to calculate angles
def calculate_angles(x, y, L):
    # Inverse kinematics calculations
    try:
        theta2 = math.acos((x**2 + y**2 - 2*L**2) / (2 * L**2))
    except ValueError:
        print("Error in calculating angles: values out of range")
        return None, None

    theta1 = math.atan2(y, x) - math.atan2(L * math.sin(theta2), L + L * math.cos(theta2))
    
    # Convert radians to degrees
    theta1_deg = math.degrees(theta1)
    theta2_deg = math.degrees(theta2)
    
    return theta1_deg, theta2_deg

# Convert angles to duty cycles
def angle_to_duty_cycle(angle):
    # Example conversion, needs to be calibrated for your servos
    duty_cycle = 2 + (angle / 180) * 10  # Adjust based on your servo specs
    
    # Clamp the duty cycle to the range [0.0, 100.0]
    if duty_cycle < 0:
        duty_cycle = 0
    elif duty_cycle > 100:
        duty_cycle = 100

    return duty_cycle

# Home position in terms of x, y coordinates
x_home = -0  # Set this to your desired home x-coordinate
y_home = 10  # Set this to your desired home y-coordinate
L = 10  # Length of each arm segment (assuming both arms have the same length)

# Calculate the angles for the home position
theta1_deg, theta2_deg = calculate_angles(x_home, y_home, L)

# Check for valid angles
if theta1_deg is None or theta2_deg is None:
    print("Invalid angles calculated. Exiting.")
    GPIO.cleanup()
    exit()

# Convert angles to duty cycles
bottom_duty_cycle = angle_to_duty_cycle(theta1_deg)
middle_duty_cycle = angle_to_duty_cycle(theta2_deg)

# Print duty cycles for debugging
print(f"Calculated Duty Cycles - Bottom: {bottom_duty_cycle}, Middle: {middle_duty_cycle}")

# Clamp duty cycles to within servo limits
if bottom_duty_cycle < bottom_min:
    print(f"Bottom duty cycle {bottom_duty_cycle} is below minimum, clamping to {bottom_min}.")
    bottom_duty_cycle = bottom_min
elif bottom_duty_cycle > bottom_max:
    print(f"Bottom duty cycle {bottom_duty_cycle} is above maximum, clamping to {bottom_max}.")
    bottom_duty_cycle = bottom_max

if middle_duty_cycle < middle_min:
    print(f"Middle duty cycle {middle_duty_cycle} is below minimum, clamping to {middle_min}.")
    middle_duty_cycle = middle_min
elif middle_duty_cycle > middle_max:
    print(f"Middle duty cycle {middle_duty_cycle} is above maximum, clamping to {middle_max}.")
    middle_duty_cycle = middle_max

# Move both arms to the home position
try:
    # Create threads for the ramp movement
    thread_middle = threading.Thread(target=Ramp, args=(middle_servo, middle_home, middle_duty_cycle))
    thread_bottom = threading.Thread(target=Ramp, args=(bottom_servo, bottom_home, bottom_duty_cycle))
    
    # Start threads
    thread_middle.start()
    thread_bottom.start()
    
    # Wait for threads to complete
    thread_middle.join()
    thread_bottom.join()

    sleep(5)
    #bottom_duty_cycle = round(bottom_duty_cycle, 2)
    #middle_duty_cycle = round(middle_duty_cycle, 2)
    # Optionally call another script here
    #os.system(f"python3 ServoHome.py {rotation_home} {bottom_duty_cycle} {middle_duty_cycle}")

finally:
    # Cleanup
    middle_servo.stop()
    bottom_servo.stop()
    GPIO.cleanup()
