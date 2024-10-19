import math
import sys

class InverseKinematics:

    def __init__(self):
        # Initialize any constants or parameters you need
        self.L1 = 10  # Length of the first arm segment
        self.L2 = 10  # Length of the second arm segment
        self.X = 0
        self.Y = 10
        self.L = 10

    def calculate_duty_cycles(self, X, Y):
        # Convert the x, y inputs (which are in the range -10 to 10)
        # to the actual desired end effector position
        x_pos = X * 5  # Assuming a workspace of -50 to 50 cm
        y_pos = Y * 5  # Assuming a workspace of -50 to 50 cm

        # Calculate the angles using inverse kinematics
        theta2 = math.acos((x_pos**2 + y_pos**2 - self.L1**2 - self.L2**2) / (2 * self.L1 * self.L2))
        theta1 = math.atan2(y_pos, x_pos) - math.atan2(self.L2 * math.sin(theta2), self.L1 + self.L2 * math.cos(theta2))

        # Convert angles to degrees
        theta1_deg = math.degrees(theta1)
        theta2_deg = math.degrees(theta2)

        # Convert angles to duty cycles (this will depend on your specific servo setup)
        bottom_duty = self.angle_to_duty_cycle(theta1_deg)
        middle_duty = self.angle_to_duty_cycle(theta2_deg)

        return theta1_deg, theta2_deg, bottom_duty, middle_duty

    def angle_to_duty_cycle(self, angle):
        # This is a placeholder function. You'll need to implement this
        # based on your specific servo motors and how they respond to duty cycle inputs
        # For example:
        return (angle + 90) / 180 * (12 - 2) + 2  # Assuming servo range of 2-12% duty cycle for 0-180 degrees

    def set_parameters_from_args(self):
        if len(sys.argv) != 4:
            self.X = 0
            self.Y = 10
            self.L = 10
        else:
            self.X = float(sys.argv[1])
            self.Y = float(sys.argv[2])
            self.L = float(sys.argv[3])

    def calculate_and_print_results(self):
        # Calculate the angles for the home position
        theta1_deg, theta2_deg, bottom_duty, middle_duty = self.calculate_duty_cycles(self.X, self.Y)

        print(f"Calculated Degree - Theta1: {theta1_deg} // Theta2: {theta2_deg}")

        # Print duty cycles for debugging
        print(f"Calculated Duty Cycles - Bottom: {bottom_duty}, Middle: {middle_duty}")

# Example usage
if __name__ == "__main__":
    ik = InverseKinematics()
    ik.set_parameters_from_args()
    ik.calculate_and_print_results()
