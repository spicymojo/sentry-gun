import RPi.GPIO as GPIO
import time

delay = 0.0055
steps = 200
coil_1_pin_1 = 0
coil_1_pin_2 = 0
coil_2_pin_1 = 0
coil_2_pin_2 = 0
position = 0
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

half_stepping = [[1,0,0,0],[1,0,1,0],[0,0,1,0],[0,1,1,0],
				[0,1,0,0],[0,1,0,1],[0,0,0,1],[1,0,0,1]]

full_step = [[1,0,1,0],[0,1,1,0],[0,1,0,1],[1,0,0,1],
		     [1,0,1,0],[0,1,1,0],[0,1,0,1],[1,0,0,1]]

wave = [[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]]


class Stepper:
    def __init__(self, port1, port2, port3, port4):
        global coil_1_pin_1, coil_1_pin_2, coil_2_pin_1, coil_2_pin_2
        coil_1_pin_1 = port1
        coil_1_pin_2 = port2
        coil_2_pin_1 = port3
        coil_2_pin_2 = port4
        self.position = 0
        self.set_gpio_out()

    def set_gpio_out(self):
        GPIO.setup(coil_1_pin_1, GPIO.OUT)
        GPIO.setup(coil_1_pin_2, GPIO.OUT)
        GPIO.setup(coil_2_pin_1, GPIO.OUT)
        GPIO.setup(coil_2_pin_2, GPIO.OUT)

    def get_gpio_ports(self):
        return "[" + str(coil_1_pin_1) + "," + str(coil_1_pin_2) + "," \
               + str(coil_2_pin_1) + "," + str(coil_2_pin_2) + "]"

    def print_steps(self):
        print("Pasos: " + str(self.pasos / 4))

    @property
    def return_steps(self):
        return self.position

    def add_steps(self, step):
        self.position += step

    def move_forward(self, steps):
        while steps > 0:
            for i in half_stepping:
                self.do_step(i)
                time.sleep(delay)
                steps -=1

    def move_backwards(self, steps):
        while steps > 0:
            for i in reversed(half_stepping):
                self.do_step(i)
                time.sleep(delay)
                steps -=1

    def do_step(self, values):
        GPIO.output(coil_1_pin_1, values[0])
        GPIO.output(coil_1_pin_2, values[1])
        GPIO.output(coil_2_pin_1, values[2])
        GPIO.output(coil_2_pin_2, values[3])

    def off(self):
        GPIO.output(coil_1_pin_1, 0)
        GPIO.output(coil_1_pin_2, 0)
        GPIO.output(coil_2_pin_1, 0)
        GPIO.output(coil_2_pin_2, 0)


