from stepper import Stepper
import time
base_motor = Stepper("Base",12,16,20,21)
base_motor.set_speed(10)
print(base_motor.print_info())

for i in range(5):
    base_motor.move_forward(30)
    print("FORWARD --->")
    time.sleep(1)
    print("BACKWARD <---")
    base_motor.move_backwards(30)
    print("ROUND: " + str(i+1))
    time.sleep(1)
    base_motor.off()
    print("MOTOR OFF\n")
    time.sleep(0.5)

