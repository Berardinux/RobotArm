# main.py
from controller import Controller
from robot_arm import RobotArm
from time import sleep

if __name__ == "__main__":
    controller = Controller('/dev/input/event4')
    robot_arm = RobotArm()

    try:
        while True:
            if controller.Z is not None:
                robot_arm.move_arm(controller.Z)  # Pass Z value as x_home
            sleep(0.5)
    except KeyboardInterrupt:
        pass
    finally:
        robot_arm.cleanup()
