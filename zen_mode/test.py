from stepper import Stepper
motor = Stepper(19,26,16,21)

for i in range(0,200):
    motor.one_step_forward()