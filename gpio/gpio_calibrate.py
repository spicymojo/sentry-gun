from stepper import Stepper
import sys, os, atexit, time,curses
motor_base = Stepper(19,26,16,21)
motor_base.print_data()
motor_base.off()

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
            motor_base.move_forward(1)
        elif char == curses.KEY_LEFT:
            screen.addstr(0, 0, 'Moviendo a izquierda...')
            motor_base.move_backwards(1)
        elif char == curses.KEY_DOWN:
            screen.addstr(0, 0, 'OFF...')
            motor_base.off()


finally:
    motor_base.off()
    curses.nocbreak();
    screen.keypad(0);
    curses.echo()
    curses.endwin()