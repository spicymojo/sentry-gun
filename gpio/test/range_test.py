import RPi.GPIO as GPIO
from stepper import Stepper
import time

motor_base = Stepper(12,16,20,21)
print("Ports: " + str(motor_base.get_gpio_ports()))
motor_base.off()
try:
    print ("FORWARD")
    motor_base.move_forward(17)
    time.sleep(1)
    
    print("BACKWARD")
    motor_base.move_backwards(34)
    time.sleep(1)

    print("RETURN")
    motor_base.move_forward(17)
    time.sleep(1)

finally:
    motor_base.off()
