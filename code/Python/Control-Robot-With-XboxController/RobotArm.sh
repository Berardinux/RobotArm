#!/bin/bash

pigpiod

# Cleanup function to kill Python scripts and exit
cleanup() {
    echo "Ctrl-C pressed. Stopping Python scripts..."
    kill $pid1 $pid2 $pid3 $pid4 2>/dev/null
    wait $pid1 $pid2 $pid3 $pid4 2>/dev/null
    echo "Python scripts stopped."
    exit 0
}

# Trap SIGINT (Ctrl-C)
trap cleanup INT

# Is the Xbox Controller connected?
isControllerConnected=$(ls /dev/input | grep event4)

# Check if the Xbox Controller is connected.
if [ -n "$isControllerConnected" ]; then
    echo "Command produced isControllerConnected: $isControllerConnected"

    # Start the Python scripts in the background and store their PIDs
    /usr/bin/python3 /home/berardinux/RobotArm/code/Python/Control-Robot-With-XboxController/src/Arm/ProgramChanger.py &
    pid1=$!
    /usr/bin/python3 /home/berardinux/RobotArm/code/Python/Control-Robot-With-XboxController/src/ArmBase/main.py &
    pid2=$!
    /usr/bin/python3 /home/berardinux/RobotArm/code/Python/Control-Robot-With-XboxController/src/Hand/main.py &
    pid3=$!
    /usr/bin/python3 /home/berardinux/RobotArm/code/Python/Control-Robot-With-XboxController/src/Stepper/StepperController.py &
    pid4=$!

    echo "Python scripts started with PIDs: $pid1, $pid2, $pid3, $pid4"

    # Monitor the connection status
    while [ -n "$isControllerConnected" ]; do
        isControllerConnected=$(ls /dev/input | grep event4)
        echo "The Xbox Controller is still connected."
        sleep 1
    done

    # Controller disconnected
    echo "The Xbox Controller is no longer connected. Stopping Python scripts."

    # Kill the Python scripts
    kill $pid1 $pid2 $pid3 $pid4 2>/dev/null
    wait $pid1 $pid2 $pid3 $pid4 2>/dev/null

    echo "Python scripts stopped."
else
    echo "The Xbox Controller is not connected."
fi
