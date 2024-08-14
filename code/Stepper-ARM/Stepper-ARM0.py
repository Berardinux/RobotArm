# Voltage supplyed was 10V and the VREF was .45V

from time import sleep
import RPi.GPIO as GPIO

# Setup GPIO
GPIO.setmode(GPIO.BCM) # "BCM" is used to select GPIO number "BOARD" is used to select pin number
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)# 21 Step pin

GPIO.output(20, GPIO.LOW)

# Step the motor
for _ in range(800):
    GPIO.output(21, GPIO.HIGH)
    sleep(.005)
    GPIO.output(21, GPIO.LOW)
    sleep(.005)

GPIO.cleanup()
