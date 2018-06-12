from stepper import Stepper
import time
base_motor = Stepper("Base",12,16,20,21)
base_motor.set_delay(0.02)
print("Motor base. Puertos: " + base_motor.get_gpio_ports())
print("30 steps --->")
base_motor.move_forward(30)
print("[DONE]")
time.sleep(1)
print("30 steps <---")
base_motor.move_backwards(30)
print("[DONE]")
time.sleep(1)
base_motor.off()
print("MOTOR OFF")
time.sleep(0.5)

