import math

def calculate_angles(z, y, L):
    """Calculate the angles needed for the given Z and Y positions."""
    # Clamp inputs to ensure they are within the arm's physical reach
    max_reach = 2 * L
    distance = math.sqrt(z**2 + y**2)

    if distance > max_reach:
        # Scale z and y to fit within the reachable area
        scale_factor = max_reach / distance
        z *= scale_factor
        y *= scale_factor
        print(f"Inputs scaled: Z={z}, Y={y}")

    try:
        # Compute cos(theta2): Angle between the two arms
        cos_theta2 = (z**2 + y**2 - 2 * L**2) / (2 * L**2)
        cos_theta2 = max(-1.0, min(1.0, cos_theta2))  # Clamp to valid range
        theta2 = math.acos(cos_theta2)

        # Compute sin(theta2) for stability
        sin_theta2 = math.sqrt(1 - cos_theta2**2)

        # Compute theta1: Base angle
        theta1 = math.atan2(y, z) - math.atan2(L * sin_theta2, L + L * cos_theta2)

        # Debug intermediate values
        print(f"cos_theta2: {cos_theta2}, sin_theta2: {sin_theta2}, theta1: {math.degrees(theta1)}, theta2: {math.degrees(theta2)}")

    except ValueError as e:
        print(f"Error in calculating angles: {e}")
        return None, None

    # Convert radians to degrees
    theta1_deg = math.degrees(theta1)
    theta2_deg = math.degrees(theta2)

    # Ensure non-zero contribution from theta2
    if theta2_deg < 1e-3:  # Near-zero angle correction
        theta2_deg = 1.0  # Add minimal bending for realistic simulation

    return theta1_deg, theta2_deg




if __name__ == "__main__":
    # Example usage: Test cases
    L = 10  # Length of each arm segment

    test_cases = [
        (5, 5),   # Inside reachable area
        (10, 10), # On the edge of maximum reach
        (15, 15), # Beyond maximum reach
        (0, 20),  # Purely vertical input
        (-5, 5),  # Negative Z input
    ]

    for z, y in test_cases:
        print(f"\nTesting with Z: {z}, Y: {y}")
        theta1, theta2 = calculate_angles(z, y, L)
        if theta1 is not None and theta2 is not None:
            print(f"Calculated Angles - Theta1: {theta1}°, Theta2: {theta2}°")
        else:
            print("Angles could not be calculated.")
