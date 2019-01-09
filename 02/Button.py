import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    state = GPIO.input(13)
    if state == False:
        print "Maaaaack"
        sleep(0.2)
