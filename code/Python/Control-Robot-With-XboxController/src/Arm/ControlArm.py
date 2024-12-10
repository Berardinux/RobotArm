def angle_to_pwm(angle, points):
    """
    Interpolate the PWM value for a given angle using known (angle, pwm) points.
    points: A list of tuples [(angle0, pwm0), (angle90, pwm90), (angle180, pwm180)]
    """
    # Unpack the known points
    (a0, p0), (a90, p90), (a180, p180) = points

    # Ensure angle is within 0-180 range
    angle = max(0, min(180, angle))

    if angle <= 90:
        # Interpolate between 0° and 90°
        return p0 + ( (angle - a0) * (p90 - p0) / (a90 - a0) )
    else:
        # Interpolate between 90° and 180°
        return p90 + ( (angle - a90) * (p180 - p90) / (a180 - a90) )

def convert_angles_to_pwm(shoulder_angle, elbow_angle):
    """
    Convert the shoulder and elbow angles (in degrees) to corresponding PWM signals.
    """

    # Known points for shoulder servo
    # 0° → 7.7, 90° → 4.5, 180° → 1.7
    shoulder_points = [(0, 7.7), (90, 4.5), (180, 1.7)]

    # Known points for elbow servo
    # 0° → 9.0, 90° → 6.2, 180° → 3.2
    elbow_points = [(0, 9.0), (90, 6.2), (180, 3.2)]

    shoulder_pwm = angle_to_pwm(shoulder_angle, shoulder_points)
    elbow_pwm = angle_to_pwm(elbow_angle, elbow_points)

    return shoulder_pwm, elbow_pwm

if __name__ == "__main__":
    # Example usage:
    # Suppose we get these angles from inverse kinematics
    shoulder_angle_test = 95.0
    elbow_angle_test = 50.0

    shoulder_pwm, elbow_pwm = convert_angles_to_pwm(shoulder_angle_test, elbow_angle_test)
    print(f"Shoulder Angle: {shoulder_angle_test}° → PWM: {shoulder_pwm:.2f}")
    print(f"Elbow Angle: {elbow_angle_test}° → PWM: {elbow_pwm:.2f}")
