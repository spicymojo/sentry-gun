from stepper import Stepper
import sys, os, atexit, time,curses
pan_motor = Stepper("Base",6,13,19,26)
print("Motor 1 (Base): " + pan_motor.get_gpio_ports())
pan_motor.set_delay(0.01)
print("Motor delay: " + pan_motor.get_delay())
pan_motor.off()


# Activamos curses para controlar la impresion
screen = curses.initscr()     # Cogemos el cursor
curses.noecho()               # Desactivamos el echo del input
curses.cbreak()               # Reconocemos inmediatamente las teclas
screen.keypad(True)           # Reconocemos teclas "especiales"

try:
	while True:
		char = screen.getch()
		if char == ord('q'):
			break
		elif char == curses.KEY_RIGHT:
			screen.addstr(0, 0, 'Moviendo a derecha...  ')
			pan_motor.move_forward(1)
		elif char == curses.KEY_LEFT:
			screen.addstr(0, 0, 'Moviendo a izquierda...')
			pan_motor.move_backwards(1)
		elif char == curses.KEY_DOWN:
			pan_motor.round_forward()


finally:
	pan_motor.off()
	curses.nocbreak();
	screen.keypad(0);
	curses.echo()
	curses.endwin()
