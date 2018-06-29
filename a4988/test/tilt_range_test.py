import RPi.GPIO as GPIO
from stepper import Stepper
import time

tilt_motor = Stepper("Top",16,6,13)
tilt_motor.set_speed(5)
print(tilt_motor.print_info())

try:
    for i in range(1):
        print ("12 steps <--")
        tilt_motor.move_forward(10)
        time.sleep(10)

        print("24 steps -->")
        tilt_motor.move_backwards(20)
        time.sleep(1)


        print ("12 steps <--")
        tilt_motor.move_forward(10)
        time.sleep(1)

finally:
    tilt_motor.off()
    print("DONE. All ok?")
