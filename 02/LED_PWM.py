import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)

p = GPIO.PWM(18,60)
p.start(0)

while True:
    for i in range (50):
        p.ChangeDutyCycle(i)
        sleep(0.01)

    for i in range (50):
        p.ChangeDutyCycle(50 - i)
        sleep(0.01)
