import RPi.GPIO as GPIO
from stepper import Stepper
import time

# Variables

delay = 0.0055

motor_base = Stepper(19,26,16,21)
motor_base.print_data()
motor_base.off()
try:
    print ("FORWARD")
    motor_base.move_forward(17)
    time.sleep(0.1)
    print("BACKWARD")
    motor_base.move_backwards(34)
    print("RETURN")
    motor_base.move_forward(17)


finally:
    motor_base.off()