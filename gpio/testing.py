from stepper import Stepper
import sys, os, atexit, curses
motor1 = Stepper(19,26,16,21)
motor1.print_data()
motor1.off()

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
            screen.addstr(0, 0, 'Moviendo a derecha...')
            motor1.move_forward(1)
            motor1.off()
        elif char == curses.KEY_LEFT:
            screen.addstr(0, 0, 'Moviendo a izquierda...')
            motor1.move_backwards(1)
            motor1.off()
        elif char == curses.KEY_DOWN:
            screen.addstr(0, 0, 'OFF...')
            motor1.off()


finally:
    curses.nocbreak();
    screen.keypad(0);
    curses.echo()
    curses.endwin()