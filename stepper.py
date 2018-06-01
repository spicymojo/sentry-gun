import RPi.GPIO as GPIO
import time

delay = 0.05
actual_step = 0
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

full_step = [[1,0,1,0],[0,1,1,0],[0,1,0,1],[1,0,0,1]]
reverse_step = [[1,0,0,1],[0,1,0,1],[0,1,1,0],[1,0,1,0]]


class Stepper:
    def __init__(self, motor_name, port1,port2,port3,port4):
        self.name = motor_name
        self.coil_1_pin_1 = port1
        self.coil_1_pin_2 = port2
        self.coil_2_pin_1 = port3
        self.coil_2_pin_2 = port4
        self.position = 0
        self.set_gpio_out()

    def set_gpio_out(self):
        GPIO.setup(self.coil_1_pin_1, GPIO.OUT)
        GPIO.setup(self.coil_1_pin_2, GPIO.OUT)
        GPIO.setup(self.coil_2_pin_1, GPIO.OUT)
        GPIO.setup(self.coil_2_pin_2, GPIO.OUT)

    def get_gpio_ports(self):
        return "[" + str(self.coil_1_pin_1) + "," + str(self.coil_1_pin_2) + "," \
               + str(self.coil_2_pin_1) + "," + str(self.coil_2_pin_2) + "]"

    # Steps from center
    def get_position(self):
        return self.position

    def get_name(self):
        return self.name

    def update_position(self,step):
        self.position += step
        if (self.position >= 100 or self.position <= -100):
            self.position = 0

    def round_forward(self):
        for i in range(200):
            self.move_forward(1)

    def round_backwards(self):
        for i in range(200):
            self.move_forward(1)


    def move_forward(self,steps):
        global  actual_step, steps_from_center
        for i in range(steps):
            if actual_step == 0:
                self.do_step(full_step[0])
                actual_step += 1
            elif actual_step == 1:
                self.do_step(full_step[1])
                actual_step += 1
            elif actual_step == 2:
                actual_step += 1
                self.do_step(full_step[2])
            elif actual_step == 3:
                self.do_step(full_step[3])
                actual_step = 0
            self.update_position(1)
            time.sleep(delay)

    def move_backwards(self,steps):
        global  actual_step
        for i in range(steps):
            if actual_step == 0:
                self.do_step(reverse_step[0])
                actual_step += 1
            elif actual_step == 1:
                self.do_step(reverse_step[1])
                actual_step += 1
            elif actual_step == 2:
                actual_step += 1
                self.do_step(reverse_step[2])
            elif actual_step == 3:
                self.do_step(reverse_step[3])
                actual_step = 0
            self.update_position(-1)
            time.sleep(delay)

    def do_step(self, gpio):
        GPIO.output(self.coil_1_pin_1, gpio[0])
        GPIO.output(self.coil_1_pin_2, gpio[1])
        GPIO.output(self.coil_2_pin_1, gpio[2])
        GPIO.output(self.coil_2_pin_2, gpio[3])

    def off(self):
        GPIO.output(self.coil_1_pin_1, 0)
        GPIO.output(self.coil_1_pin_2, 0)
        GPIO.output(self.coil_2_pin_1, 0)
        GPIO.output(self.coil_2_pin_2, 0)



