from stepper import Stepper
import sys, os, atexit, time,curses
tilt_motor = Stepper(18,23,24,25)
print("Motor 1 (Base): " + tilt_motor.get_gpio_ports())
tilt_motor.off()


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
			tilt_motor.move_forward(1)
		elif char == curses.KEY_LEFT:
			screen.addstr(0, 0, 'Moviendo a izquierda...')
			tilt_motor.move_backwards(1)
		elif char == curses.KEY_DOWN:
			tilt_motor.round_forward()


finally:
	tilt_motor.off()
	curses.nocbreak();
	screen.keypad(0);
	curses.echo()
	curses.endwin()
