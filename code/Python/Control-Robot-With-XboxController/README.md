# Connect Xbox Controller to bluetooth
bluetoothctl

scan on

pair XX:XX:XX:XX:XX:XX

trust XX:XX:XX:XX:XX:XX

connect XX:XX:XX:XX:XX:XX

# Look at Controller raw output
sudo evtest /dev/input/event0

# udev rules
sudo nano /etc/udev/rules.d/60-RobotArm.rules {


SUBSYSTEM=="input", ATTRS{address}=="EC:83:50:5E:E2:8E", ACTION=="add", RUN+="/bin/systemctl start RobotArm.service"

}

sudo udevadm control --reload-rules


# Systemd
sudo nano /etc/systemd/system/RobotArm.service {

[Unit]
Description=RobotArm Monitor Service
After=udev.service

[Service]
Type=simple
ExecStart=/home/berardinux/RobotArm/code/Python/Control-Robot-With-XboxController/RobotArm.sh

[Install]
WantedBy=multi-user.target

}

sudo systemctl daemon-reload

sudo systemctl status blackbriar-monitor.service
