from stepper import Stepper
import sys, os, atexit, time,curses
tilt_motor = Stepper("Top",16,12,16)
tilt_motor.set_speed(10)
print(tilt_motor.print_info())
#tilt_motor.off()


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
			screen.addstr(0, 0, 'Moviendo arriba...  ')
			tilt_motor.move_forward(1)
		elif char == curses.KEY_RIGHT:
			screen.addstr(0, 0, 'Vuelta arriba...')
			tilt_motor.round_forward()
		elif char == curses.KEY_LEFT:
			screen.addstr(0, 0, 'Vuelta abajo...')
			tilt_motor.round_backwards()
		elif char == curses.KEY_DOWN:
			screen.addstr(0, 0, 'Moviendo abajo...')
			tilt_motor.move_backwards(1)


finally:
	tilt_motor.off()
	curses.nocbreak();
	screen.keypad(0);
	curses.echo()
	curses.endwin()
