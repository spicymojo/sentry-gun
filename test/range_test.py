import RPi.GPIO as GPIO
from stepper import Stepper
import time

motor_base = Stepper("Base", 12,16,20,21)
motor_base.set_delay(0.015)
print("Motor: " + motor_base.get_name() + "\nPorts: " + motor_base.get_gpio_ports())
motor_base.off()
try:
    print ("17 steps -->")
    motor_base.move_forward(17)
    time.sleep(1)
    
    print("34 steps <--")
    motor_base.move_backwards(34)
    time.sleep(1)

    print("17 steps -->")
    motor_base.move_forward(17)
    time.sleep(1)

finally:
    motor_base.off()
    print("DONE. All ok?")
