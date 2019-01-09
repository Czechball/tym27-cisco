import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)

p = GPIO.PWM(18,500)
p.start(0)

while True:
    for i in range (100):
        p.ChangeDutyCycle(i)
        sleep(0.1)

    for i in range (100):
        p.ChangeDutyCycle(100 - i)
        sleep(0.1)
