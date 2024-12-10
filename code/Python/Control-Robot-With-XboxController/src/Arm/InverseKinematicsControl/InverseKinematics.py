import math

def moveToPos(x, y, z):
    """
    Calculate the angles for a robotic arm to move to the specified position.

    Parameters:
    x (float): Target position in the X direction (always 0 here for simplicity).
    y (float): Target position in the Y direction.
    z (float): Target position in the Z direction.

    Returns:
    tuple: (base_angle, arm1_angle, arm2_angle)
    """
    ARM_LENGTH = 265  # Length of each arm segment in mm
    MAX_REACH = 2 * ARM_LENGTH  # Maximum reach in mm

    # Calculate the target distance from the origin
    distance = math.sqrt(y**2 + z**2)

    if distance > MAX_REACH:
        raise ValueError("Target position is beyond the arm's reach.")

    # Base rotation angle (simplified, assuming fixed X-axis position)
    base_angle = math.atan2(y, z) * (180 / math.pi)

    # Compute elevation and bending angles
    phi = math.atan2(z, y) * (180 / math.pi)
    theta = math.acos(distance / (2 * ARM_LENGTH)) * (180 / math.pi)

    arm1_angle = phi + theta  # First arm segment angle
    arm2_angle = phi - theta  # Second arm segment angle

    return base_angle, arm1_angle, arm2_angle


if __name__ == "__main__":
    # Example usage: Test cases
    test_cases = [
        (0, 10, 10),   # Random valid position
        (0, 50, 50),   # Position along the diagonal
        (0, 100, 100), # Near the arm's max reach
        (0, 150, 150), # Beyond arm's reach (will raise ValueError)
        (0, -10, -10)  # Negative inputs for all dimensions
    ]

    for x, y, z in test_cases:
        print(f"\nTesting with X: {x}, Y: {y}, Z: {z}")
        try:
            b, a1, a2 = moveToPos(x, y, z)
            print(f"Calculated Angles - Base: {b:.2f}°, Shoulder: {a1:.2f}°, Elbow: {a2:.2f}°")
        except ValueError as e:
            print(f"Error: {e}")
