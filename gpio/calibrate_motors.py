from stepper import Stepper
import sys, os, atexit, time,curses
pan_motor = Stepper(18,23,24,25)
print("Motor 1 (Base): " +pan_motor.get_gpio_ports())
pan_motor.off()

#tilt_motor = Stepper(12,16,20,21)
#print("Motor 2 (Soporte): " + str(pan_motor.print_data()))
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
        elif char == curses.KEY_RIGHT:
            screen.addstr(0, 0, 'Moviendo a derecha...  ')
            pan_motor.move_forward(1)
        elif char == curses.KEY_LEFT:
            screen.addstr(0, 0, 'Moviendo a izquierda...')
            pan_motor.move_backwards(1)
        elif char == curses.KEY_UP:
            screen.addstr(0, 0, 'Moviendo arriba...     ')
            #tilt_motor.move_forward(1)
        elif char == curses.KEY_DOWN:
            screen.addstr(0, 0, 'Moviendo abajo...       ')
            #tilt_motor.move_backwards(1)

finally:
    pan_motor.off()
#    tilt_motor.off()
    curses.nocbreak();
    screen.keypad(0);
    curses.echo()
    curses.endwin()
