import RPi.GPIO as GPIO
import time
ON = 1
OFF = 0

GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)
GPIO.setup(3, GPIO.OUT)

while True:
	GPIO.output(3, ON)
	print("ON")
	time.sleep(1)
	GPIO.output(3,OFF)
	print("OFF")


