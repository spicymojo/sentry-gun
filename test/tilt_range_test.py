import RPi.GPIO as GPIO
from stepper import Stepper
import time

tilt_motor = Stepper("Top",16,6,13)
tilt_motor.set_speed(5)
print(tilt_motor.print_info())

try:
    for i in range(5):
        print ("7 steps down... DOWN")
        tilt_motor.move_forward(7)
        time.sleep(1)

        print("14 steps up... UP")
        tilt_motor.move_backwards(14)
        time.sleep(1)

        print ("7 steps down... DOWN")
        tilt_motor.move_forward(7)
        time.sleep(1)

finally:
    tilt_motor.off()
    print("DONE. All ok?")
