import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup( 12 ,GPIO.OUT)
servo = GPIO.PWM( 12, 50)
servo.start(0)

try:
  servo.ChangeDutyCycle(2)
  time.sleep(1)
  servo.ChangeDutyCycle(4)
  time.sleep(1)
  servo.ChangeDutyCycle(6)
  time.sleep(1)
  servo.ChangeDutyCycle(8)
  time.sleep(1)
  servo.ChangeDutyCycle(10)
  time.sleep(1)
  servo.ChangeDutyCycle(12)
  time.sleep(1)
  servo.ChangeDutyCycle(2)
  time.sleep(1)
finally:
  servo.stop()
  GPIO.cleanup