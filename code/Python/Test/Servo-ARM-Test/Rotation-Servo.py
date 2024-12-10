import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup( 12 ,GPIO.OUT)
servo = GPIO.PWM( 12, 50)
servo.start(0)

def Ramp(OldDutyCycle, NewDutyCycle):
    if OldDutyCycle < NewDutyCycle:
        # Ramp up
        i = OldDutyCycle
        while i <= NewDutyCycle:
            servo.ChangeDutyCycle(i)
            i += 0.03  # Increment by 0.1
            sleep(.01)
    elif OldDutyCycle > NewDutyCycle:
        # Ramp down
        i = OldDutyCycle
        while i >= NewDutyCycle:
            servo.ChangeDutyCycle(i)
            i -= 0.03  # Decrement by 0.1
            sleep(.01)
            
# - = back + forward
# 7.15 is the middle
CCW_End = 2
Middle = 7.15
CW_End = 12

try:
  while True:
    Ramp(Middle, CCW_End)
    #sleep(1)

    #sleep(1)
    Ramp(CCW_End, Middle)
    #sleep(1)

    Ramp(Middle, CW_End)
    #sleep(1)

    #sleep(1)
    Ramp(CW_End, Middle)
    #sleep(1)
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