import time
from ControllerLeftAnalog import ControllerLeftAnalog
from ControllerRightAnalog import ControllerRightAnalog
from InverseKinematics import InverseKinematics

# Debug imports
print("Imported ControllerLeftAnalog:", ControllerLeftAnalog)
print("Imported ControllerRightAnalog:", ControllerRightAnalog)

def main():
    controllerL = ControllerLeftAnalog()
    controllerR = ControllerRightAnalog()
    ik = InverseKinematics()

    try:
        while True:
            x = controllerL.process_events()
            y = controllerR.process_events()
            print(f"X: {x}, Y: {y}")
            
            #theta1, theta2, bottom_duty, middle_duty = ik.calculate_duty_cycles(x, y) 
            #print(f"Theta1: {theta1:.2f}, Theta2: {theta2:.2f}")
            #print(f"Bottom Duty Cycle: {bottom_duty:.2f}, Middle Duty Cycle: {middle_duty:.2f}")
            
            #print("---")
            time.sleep(0.01)  # Adjust as needed
    except KeyboardInterrupt:
        print("\nExiting gracefully...")
    finally:
        controllerL.close()
        controllerR.close()

if __name__ == "__main__":
    main()
