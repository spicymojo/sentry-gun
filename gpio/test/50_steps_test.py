from stepper import Stepper
import time
base_motor = Stepper(12,16,20,21)

print("[ MOTOR TESTING]")
print("Base motor... ports: " + base_motor.get_gpio_ports())
print("50 steps forward:")
base_motor.move_forward(50)
print("[DONE]")
time.sleep(0.5)
print("50 steps backwards:")
base_motor.move_backwards(50)
print("[DONE]")
time.sleep(0.5)
base_motor.off()
time.sleep(0.5)
print("The end. Ciao!")

