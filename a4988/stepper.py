import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

FORWARD = 1
BACKWARDS = 0
HIGH = 1
LOW = 0

class Stepper:
    def __init__(self, name,direction_pin, step_pin):
        self.name = name
        self.position = 0
        self.delay = 60000
        self.direction_pin = direction_pin
        self.step_pin = step_pin
        self.direction = 0
        self.set_gpio_out()
        self.off()

    # NOTE: step_delay = [(1000 *1000 * 60)/200] / rpm , if revs != 200, change this number
    def set_speed(self,rpm):
        microseconds = 300000.0/rpm
        self.delay = microseconds / 1000000.0  # Seconds
        print self.delay

    def get_speed(self):
        return int(((300000 / self.delay) / 1000000))

    def get_delay(self):
        return str(self.delay)

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_gpio_out(self):
        GPIO.setup(self.direction_pin, GPIO.OUT)
        GPIO.setup(self.step_pin, GPIO.OUT)

    # Motor Info
    def print_info(self):
        return "Motor: " + self.get_name() +" \nSpeed: " + str(self.get_speed()) \
                + " rpm \nStep pin: " + str(self.step_pin) + "\nDirection pin: " + str (self.direction_pin) + "\n"

    # Steps from center
    def get_position(self):
        return self.position

    def round_forward(self):
        self.move_forward(200)


    def round_backwards(self):
        self.move_backwards(200)

    def move_forward(self,steps):
        GPIO.output(self.direction_pin, FORWARD)
        for i in range(steps):
            self.do_step()
            self.position += 1

    def move_backwards(self,steps):
        GPIO.output(self.direction_pin, BACKWARDS)
        for i in range(steps):
            self.do_step()
            self.position -= 1

    def do_step(self):
        GPIO.output(self.step_pin, GPIO.HIGH)
        sleep(self.delay)
        GPIO.output(self.step_pin, GPIO.LOW)
        sleep(self.delay)

    def off(self):
        GPIO.output(self.step_pin, LOW)
        GPIO.output(self.direction_pin, LOW)


