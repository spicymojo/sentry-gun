import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

full_step = [[1,0,1,0],[0,1,1,0],[0,1,0,1],[1,0,0,1]]
reverse_step = [[1,0,0,1],[0,1,0,1],[0,1,1,0],[1,0,1,0]]
actual_step = 0
steps_from_center = 0

class Stepper:
    def __init__(self, name, port1,port2,port3,port4):
        self.name = name
        self.coil_1_pin_1 = port1
        self.coil_1_pin_2 = port2
        self.coil_2_pin_1 = port3
        self.coil_2_pin_2 = port4
        self.position = 0
        self.delay = 0.01
        self.set_gpio_out()
        self.off()

    # NOTE: step_delay = [(1000 *1000 * 60)/200] / rpm , if revs != 200, change this number
    def set_speed(self,rpm):
        microseconds = 300000.0/rpm
        self.delay = microseconds / 1000000.0  # Seconds

    def get_speed(self):
        return int(((300000 / self.delay) / 1000000))

    def get_delay(self):
        return str(self.delay)

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_gpio_out(self):
        GPIO.setup(self.coil_1_pin_1, GPIO.OUT)
        GPIO.setup(self.coil_1_pin_2, GPIO.OUT)
        GPIO.setup(self.coil_2_pin_1, GPIO.OUT)
        GPIO.setup(self.coil_2_pin_2, GPIO.OUT)

    def get_gpio_ports(self):
        return "[" + str(self.coil_1_pin_1) + "," + str(self.coil_1_pin_2) + "," \
               + str(self.coil_2_pin_1) + "," + str(self.coil_2_pin_2) + "]"

    # Motor Info
    def print_info(self):
        return "Motor: " + self.get_name() +" \nSpeed: " + str(self.get_speed()) \
                + " rpm \nPorts: " + self.get_gpio_ports() + "\n"

    # Steps from center
    def get_position(self):
        return self.position

    def update_position(self,step):
        self.position += step
        if (self.position >= 100 or self.position <= -100):
            self.position = 0

    def round_forward(self):
        for i in range(200):
            self.move_forward(1)

    def round_backwards(self):
        for i in range(200):
            self.move_backwards(1)


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
            time.sleep(self.delay)
        self.off()

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
            time.sleep(self.delay)
        self.off()


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



