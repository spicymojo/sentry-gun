from stepper import Stepper
import sys, os, atexit, time,curses
pan_motor = Stepper("Base",16,20,21)
pan_motor.set_speed(10)
print(pan_motor.print_info())
#pan_motor.off()


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
			screen.addstr(0, 0, 'Vuelta...')
			ç
			pan_motor.round_forward()
		elif char == curses.KEY_RIGHT:
			screen.addstr(0, 0, 'Moviendo a derecha...  ')

		elif char == curses.KEY_LEFT:
			screen.addstr(0, 0, 'Moviendo a izquierda...')
			pan_motor.move_backwards(1)
		elif char == curses.KEY_DOWN:
			screen.addstr(0, 0, 'Vuelta...')
			pan_motor.round_backwards()


finally:
	pan_motor.off()
	curses.nocbreak();
	screen.keypad(0);
	curses.echo()
	curses.endwin()
