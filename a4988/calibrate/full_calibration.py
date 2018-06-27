from stepper import Stepper
import sys, os, atexit, time,curses
pan_motor = Stepper("Base",16,19,26)
tilt_motor = Stepper("Top",16,6,13)
pan_motor.set_speed(10)
tilt_motor.set_speed(10)
print(pan_motor.print_info())
print(tilt_motor.print_info())


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
		elif char == curses.KEY_UP:
			screen.addstr(0, 0, 'ARRIBA')
			tilt_motor.move_forward(1)
		elif char == curses.KEY_RIGHT:
			screen.addstr(0, 0, 'DERECHA')
			pan_motor.move_forward(1)
		elif char == curses.KEY_LEFT:
			screen.addstr(0, 0, 'IZQUIERDA')
			pan_motor.move_backwards(1)
		elif char == curses.KEY_DOWN:
			screen.addstr(0, 0, 'ABAJO')
			tilt_motor.move_backwards(1)


finally:
	curses.nocbreak();
	screen.keypad(0);
	curses.echo()
	curses.endwin()
