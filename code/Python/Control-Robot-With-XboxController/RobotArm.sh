#!/bin/bash

# Is the Xbox Controller connected?
isControllerConnected=$(ls /dev/input | grep event4)

# Check if the Xbox Controller is connected.
if [ -n "$isControllerConnected" ]; then
    echo "Command produced isControllerConnected: $isControllerConnected"
    /usr/bin/python3 /home/berardinux/RobotArm/code/Python/Control-Robot-With-XboxController/src/Arm/IndividualControl/main.py &
    /usr/bin/python3 /home/berardinux/RobotArm/code/Python/Control-Robot-With-XboxController/src/ArmBase/main.py &
    /usr/bin/python3 /home/berardinux/RobotArm/code/Python/Control-Robot-With-XboxController/src/Hand/main.py &
    /usr/bin/python3 /home/berardinux/RobotArm/code/Python/Control-Robot-With-XboxController/src/Stepper/StepperController.py &
    while [ -n "$isControllerConnected" ]; do
      isControllerConnected=$(ls /dev/input | grep event4)
      echo "The Xbox Controller is still connected"
      sleep 1
    done
    echo "The Xbox Controller is no longer connected."
else
    echo "The Xbox Controller is not connected."
fi
