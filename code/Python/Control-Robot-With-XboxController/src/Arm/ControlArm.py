def angle_to_pwm(angle, points):
    """
    Interpolate the PWM value for a given angle using known angle/PWM points.
    'points' is a list of tuples defining key angle-PWM relationships.
    
    For example:
    - For the shoulder (0°, 90°, 180°): [(0, p0), (90, p90), (180, p180)]
    - For the elbow (-90°, 0°, 90°): [(-90, p_neg), (0, p_zero), (90, p_pos)]
    """
    # Assume points are given in ascending order of angle
    # For 3 points, we have 2 segments:
    # segment 1: between points[0] and points[1]
    # segment 2: between points[1] and points[2]

    (a_start, p_start), (a_mid, p_mid), (a_end, p_end) = points

    # Clamp angle to the range defined by the given points
    angle = max(a_start, min(a_end, angle))

    if angle <= a_mid:
        # Interpolate between the start and mid points
        return p_start + ((angle - a_start) * (p_mid - p_start) / (a_mid - a_start))
    else:
        # Interpolate between the mid and end points
        return p_mid + ((angle - a_mid) * (p_end - p_mid) / (a_end - a_mid))


def convert_angles_to_pwm(shoulder_angle, elbow_angle):
    """
    Convert the shoulder and elbow angles (in degrees) to corresponding PWM signals.
    
    Shoulder (0°–180°):
    0° → 7.7, 90° → 4.5, 180° → 1.7
    
    Elbow (-90°–90°):
    -90° → 2.0, 0° → 6.2, 90° → 10.8
    """

    # Known points for shoulder servo
    shoulder_points = [(0, 7.7), (90, 4.5), (180, 1.7)]

    # Known points for elbow servo (now using -90° to +90° range)
    elbow_points = [(-90, 2.0), (0, 6.2), (90, 10.8)]

    # Ensure the shoulder angle is in [0,180]
    shoulder_angle = max(0, min(180, shoulder_angle))

    # If the elbow angle can be negative, and currently is calculated differently,
    # we must ensure the elbow angle falls within [-90,90].
    # If your inverse kinematics code can produce angles outside this range,
    # you must adjust them before calling this function.
    elbow_angle = max(-90, min(90, elbow_angle))

    shoulder_pwm = angle_to_pwm(shoulder_angle, shoulder_points)
    elbow_pwm = angle_to_pwm(elbow_angle, elbow_points)

    return shoulder_pwm, elbow_pwm


if __name__ == "__main__":
    # Example usage:
    # Suppose we get these angles from inverse kinematics
    # Test with a shoulder angle >180 or <0 and elbow angle outside [-90,90] to see clamping
    shoulder_angle_test = 95.0   # Slightly more than 90°
    elbow_angle_test = -30.0     # A negative angle for elbow

    shoulder_pwm, elbow_pwm = convert_angles_to_pwm(shoulder_angle_test, elbow_angle_test)
    print(f"Shoulder Angle: {shoulder_angle_test}° → PWM: {shoulder_pwm:.2f}")
    print(f"Elbow Angle: {elbow_angle_test}° → PWM: {elbow_pwm:.2f}")
