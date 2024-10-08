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
            i += 0.01  # Increment by 0.1
            sleep(.01)
    elif OldDutyCycle > NewDutyCycle:
        # Ramp down
        i = OldDutyCycle
        while i >= NewDutyCycle:
            servo.ChangeDutyCycle(i)
            i -= 0.01  # Decrement by 0.1
            sleep(.01)
            
# - = back + forward
# 7.15 is the middle

try:
  servo.ChangeDutyCycle(6.3)
  sleep(1)
  Ramp(6.3, 6.3)
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