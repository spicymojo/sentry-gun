from stepper import Stepper
import time
base_motor = Stepper(12,16,20,21)

print("[ MOTOR TESTING]")
print("Base motor... ports: " + base_motor.get_gpio_ports())
print("30 steps forward:")
base_motor.move_forward(30)
print("[DONE]")
time.sleep(1)
print("30 steps backwards:")
base_motor.move_backwards(30)
print("[DONE]")
time.sleep(1)
base_motor.off()
print("MOTOR OFF")
time.sleep(0.5)
print("The end. Ciao!")

