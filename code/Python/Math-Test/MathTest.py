import math
import sys

class MathTest:

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

    if len(sys.argv) != 4:
        x_home = 0
        y_home = 10
        L = 10
    else:
        x_home = float(sys.argv[1])
        y_home = float(sys.argv[2])
        L = float(sys.argv[3])

    # Calculate the angles for the home position
    theta1_deg, theta2_deg = calculate_angles(x_home, y_home, L)

    print(f"Calculated Degree - Theta1: {theta1_deg} // Theta2: {theta2_deg}")

    # Convert angles to duty cycles
    bottom_duty_cycle = angle_to_duty_cycle(theta1_deg)
    middle_duty_cycle = angle_to_duty_cycle(theta2_deg)

    # Print duty cycles for debugging
    print(f"Calculated Duty Cycles - Bottom: {bottom_duty_cycle}, Middle: {middle_duty_cycle}")


    

