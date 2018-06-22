# -*- coding: UTF-8 -*-
# En este proyecto se utilizan OpenCV 3.1.0 y Python 2.7.13

#####  LIBRERÍAS  #####

# Parseador de argumentos de consola
# Librerías para fechas y tiempo
import datetime
import time

# Librerias de OpenCV y auxiliares para tratamiento de imagen
import cv2
import imutils
import numpy as np

# Librerias para los motores
from stepper import Stepper
import RPi.GPIO as GPIO

# Lectura de configuración
import json

# Multihilo para los motores
import thread
import threading

# Librerias para evitar que los driver del motor impriman por consola
import sys, os

# Fuente para la interfaz
message_font = cv2.FONT_HERSHEY_PLAIN

# Variables utilizadas en el programa
BACKWARD = -1
FORWARD = 1

# Variables para iterar ocn la camara
firstFrame = None
actualFrame = None
count = 0

# Hilos para los motores
pan_thread = threading.Thread()
tilt_thread = threading.Thread()

##### FUNCIONES #####
def load_config():
    config = json.load(open('config.json'))
    global minimum_target_area, frame_width, exit_key, motor_delay, \
        motor_testing_steps, frame_color,center_color, test_motors, \
        print_movement_values

    # General config
    minimum_target_area= config['GENERAL']['MINIMUM_TARGET_AREA']
    frame_width = config['GENERAL']['FRAME_WIDTH']
    exit_key = config['GENERAL']['EXIT_KEY']
    frame_color = string_to_rgb(config['GENERAL']['TARGET_FRAME_COLOR'])
    center_color = string_to_rgb(config['GENERAL']['TARGET_CENTER_COLOR'])

    # Motor config
    motor_delay = config['MOTOR']['MOTOR_DELAY']
    motor_testing_steps = config['MOTOR']['TESTING_STEPS']


    # Debug
    test_motors = config['DEBUG']['TEST_MOTORS']
    print_movement_values = config['DEBUG']['PRINT_MOVEMENT_VALUES']


def string_to_rgb(rgb_string):  # OpenCV uses BGR
    b,g,r = rgb_string.split(",")
    return (int(b),int(g),int(r))


def find_best_target():
    image, borders, h = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    minimum_target_area = 5000
    best_contour = None
    for b in borders:
        area = cv2.contourArea(b)
        if area > minimum_target_area:
            minimum_target_area = area
            best_contour = b
    return best_contour


def draw_targets(contour):
    # Calculamos y dibujamos el marco y su centro
    (x, y, w, h) = cv2.boundingRect(contour)
    cv2.rectangle(frame, (x, y), (x + w, y + h), frame_color, 2)
    draw_target_center(x, y, w, h)


def draw_target_center(x,y,w,h):
    # PARÄMETROS PARA DIBUJAR EL CÍRCULO
    # cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]])

    square_center_x = x + w / 2
    square_center_y = y + h / 2
    cv2.circle(frame, (square_center_x, square_center_y), 5, center_color, -1)
    calculate_moves(square_center_x,square_center_y)


# Mostramos por pantalla el estado y la fecha
def print_info_on_video():
    cv2.putText(frame, "Estado: {}".format(text), (10, 25),
        message_font, 1.25, center_color, 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
        (10, frame.shape[0] - 15), message_font, 1, center_color, 1)


def motor_test():
    print("  [TEST] Probando el motor de la base")
    pan_motor.move_forward(motor_testing_steps)
    time.sleep(0.5)
    pan_motor.move_backwards(motor_testing_steps)
    time.sleep(0.5)
    print("  [TEST] Probando el motor del soporte")
    tilt_motor.move_forward(motor_testing_steps)
    time.sleep(0.5)
    tilt_motor.move_backwards(motor_testing_steps)
    time.sleep(0.5)


def move_motor(motor, steps, direction):
    if print_movement_values == "True":
        print("\n" + "MOTOR: " + motor.get_name() + ". LOCATION  : [" + str(motor.get_position())  + "]. STEPS: " + str(steps))

    # Movemos motores
    if direction == FORWARD:
        if motor.get_name() == "BASE":
            motor.move_forward(steps)
            print("   --->")
        else:
            motor.move_forward(steps)
            print(" UP ")
    else:
        if motor.get_name() == "BASE":
            motor.move_backwards(steps)
            print("   <---")
        else:
            motor.move_backwards(steps)
            print(" DOWN ")



def calculate_moves(center_x, center_y):

   # Apertura cámara: 60 grados. Equivale a 38 pasos del motor
   target_x_position = (center_x / 15) - 15 # (Pixels / pixels per step) - pasos maximos
   target_y_position = (center_y / 15) - 15

   steps_to_target_in_x = target_x_position - pan_motor.get_position()

   #TILT
#   steps_to_target_in_y = target_y_position + tilt_motor.get_position()

   launch_threads(steps_to_target_in_x,0)
   #launch_threads(steps_to_target_in_x,steps_to_target_in_y)


def launch_threads(steps_to_target_in_x,steps_to_target_in_y):
    global pan_thread,tilt_thread
    if steps_to_target_in_x < 0:
        pan_thread = threading.Thread(target=move_motor(pan_motor, abs(steps_to_target_in_x), BACKWARD))
    else:
        pan_thread = threading.Thread(target=move_motor(pan_motor, abs(steps_to_target_in_x), FORWARD))

"""
    TILT
    if steps_to_target_in_y > 0:
        tilt_thread = threading.Thread(target=move_motor(tilt_motor, abs(steps_to_target_in_y), BACKWARD))
    else:
        tilt_thread = threading.Thread(target=move_motor(tilt_motor, abs(steps_to_target_in_y), FORWARD))

    pan_thread.start()
    tilt_thread.start()
"""
    #pan_thread.join()
    #tilt_thread.join()
##### LIMPIEZA #####

def back_to_center():
    calculate_moves(320,240)
    time.sleep(0.5)
    print(" [INFO] Colocados motores en posición inicial")

# Liberamos cámara, GPIO y cerramos ventanas
def vacuum_cleaner():
    GPIO.cleanup()
    camera.release()
    time.sleep(1)
    cv2.destroyAllWindows()
    print("[DONE] Roomba pasada. Fin del programa")

###### FIN DE FUNCIONES #####

load_config()   # Cargamos "config.json"

# Capturamos webcam
print("[START] Preparando cámara....")
camera_recording = False

while camera_recording is not True:
    camera = cv2.VideoCapture(0)
    time.sleep(1)

    # Esperamos a que la cámara esté preparada
    camera_recording, _ = camera.read()
print("[DONE] Cámara lista!")


print("[INFO] Inicializamos los motores...")
pan_motor = Stepper("BASE", 20,21)
pan_motor.set_speed(3)
print(pan_motor.print_info())
#tilt_motor = Stepper("SOPORTE",18,23,24,25)
#print(tilt_motor.get_name() + "    PUERTOS: " + tilt_motor.get_gpio_ports())


if test_motors == "True":
    motor_test()

# Loop sobre la camara
while True:
    # Cogemos el frame inicial y ponemos el texto
    (video_signal, frame) = camera.read()

    text = "No hay objetivos"

    # center_colorimensionamos el frame, lo convertimos a escala de grises
    # y lo desenfocamos (Blur)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # Si no hay primer frame, lo inicializamos
    if firstFrame is None:
        if actualFrame is None:
            print("[INFO] Empezando captura de vídeo... ")
            actualFrame = gray
            continue
        else:
            #  Calculamos el frame Delta (Diferencia absoluta entre
            # primer frame y # el frame actual)
            abs_difference = cv2.absdiff(actualFrame, gray)
            actualFrame = gray
            thresh = cv2.threshold(abs_difference,5, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)

            if count > 30:
                print("[INFO] Esperando movimiento...")
                if not cv2.countNonZero(thresh) > 0:
                    firstFrame = gray
                else:
                    continue
            else:
                count += 1
                continue

    # Calculamos la diferencia absoluta entre el frame actual
    # y el primer frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

    # Dilatamos la imagen umbralizado, para asi buscar sus contornos
    thresh = cv2.dilate(thresh, None, iterations=2)

    # Buscamos el contorno del mayor objetivo
    best_contour = find_best_target()

    # Bucle sobre los contornos
    if best_contour is not None:
        draw_targets(best_contour)
        text = "Objetivo detectado!"

    # Mostramos la fecha y hora en el livestream
    print_info_on_video()

    # Mostramos las diferentes vistas de la cámara
    cv2.imshow("Cámara", frame)
    cv2.imshow("Umbralizado", thresh)
    cv2.imshow("Frame Delta", frameDelta)

    # Comprobamos si el usuario quiere salir
    key = cv2.waitKey(1) & 0xFF
    # Q = Salir del programa
    if key == ord(exit_key):
        print(" [INFO] Apagando el sistema...")
        break

# Liberamos recursos, cerramos ventanas y colocamos el motor
back_to_center()
vacuum_cleaner()
