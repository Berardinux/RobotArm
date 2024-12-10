import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup( 21 ,GPIO.OUT)
servo = GPIO.PWM( 21, 50)
servo.start(0)

def Ramp(OldDutyCycle, NewDutyCycle):
    if OldDutyCycle < NewDutyCycle:
        # Ramp up
        i = OldDutyCycle
        while i <= NewDutyCycle:
            servo.ChangeDutyCycle(i)
            i += 0.01  # Increment by 0.1
            sleep(.01)
    elif OldDutyCycle > NewDutyCycle:
        # Ramp down
        i = OldDutyCycle
        while i >= NewDutyCycle:
            servo.ChangeDutyCycle(i)
            i -= 0.01  # Decrement by 0.1
            sleep(.01)

# (- = back, end of travel is 2) (+ = forward, end of travel is 8.5)

# Shoulder
# 7.7 is 0 degrees
# 4.5 is 90 degrees
# 1.7 is 180 degrees

# Home = (RotationServo = 7.15) (BottomServo = 3.2) (MiddleServo = 10.8)

try:
  #servo.ChangeDutyCycle(3.2)
  #sleep(1)
  Ramp(7.7, 4.5)
  sleep(1)
  #servo.ChangeDutyCycle(4)
  #time.sleep(1)
  #servo.ChangeDutyCycle(6)
  #time.sleep(1)
  #servo.ChangeDutyCycle(8)
  #time.sleep(1)
  #servo.ChangeDutyCycle(10)
  #time.sleep(1)
  #servo.ChangeDutyCycle(12)
  #time.sleep(1)
  #servo.ChangeDutyCycle(2)
  #time.sleep(1)
finally:
  servo.stop()
  GPIO.cleanup
