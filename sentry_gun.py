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
BACKWARD = -1
FORWARD = 1

# Hilos para los motores
pan_thread = threading.Thread()
tilt_thread = threading.Thread()

##### FUNCIONES #####
def load_config():
    config = json.load(open('config.json'))
    global minimum_target_area, frame_width, exit_key, motor_revs, \
        motor_testing_steps, frame_color,center_color, test_base_motor, \
        print_movement_values

    # General config
    minimum_target_area= config['GENERAL']['MINIMUM_TARGET_AREA']
    frame_width = config['GENERAL']['FRAME_WIDTH']
    exit_key = config['GENERAL']['EXIT_KEY']
    frame_color = string_to_rgb(config['GENERAL']['TARGET_FRAME_COLOR'])
    center_color = string_to_rgb(config['GENERAL']['TARGET_CENTER_COLOR'])

    # Motor config
    motor_revs = config['MOTOR']['MOTOR_REVS']
    motor_testing_steps = config['MOTOR']['TESTING_STEPS']

    # Debug
    test_base_motor = config['DEBUG']['TEST_BASE_MOTOR']
    print_movement_values = config['DEBUG']['PRINT_MOVEMENT_VALUES']


def string_to_rgb(rgb_string):  # OpenCV uses BGR
    b,g,r = rgb_string.split(",")
    return (int(b),int(g),int(r))

def find_best_target():
    image, borders, h = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    big_area = 5000
    best_contour = None
    for b in borders:
        area = cv2.contourArea(b)
        if area > big_area:
            big_area = area
            best_contour = b
    return best_contour


def draw_contour(contour):
    # Calculamos las dimensiones del rectángulo
    (x, y, w, h) = cv2.boundingRect(contour)

    # Dibujamos el centro del cuadrado, es decir, el objetivo
    draw_target_center(x,y,w,h)

    # Dibujamos el marco del objetivo
    cv2.rectangle(frame, (x, y), (x + w, y + h), frame_color, 2)

def draw_target_center(x,y,w,h):
    # PARÄMETROS PARA DIBUJAR EL CÍRCULO
    # cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]])

    square_center_x = x + w / 2
    square_center_y = y + h / 2
    cv2.circle(frame, (square_center_x, square_center_y), 5, center_color, -1)
    calculate_moves(square_center_x,square_center_y)

def print_date_on_video():
    # Imprimimos el texto y la fecha en la ventana
    cv2.putText(frame, "Estado: {}".format(text), (10, 25),
        message_font, 1.25, center_color, 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
        (10, frame.shape[0] - 15), message_font, 1, center_color, 1)

def motor_test():
    # Probamos el motor de la base
    print(" [TEST] Probando el motor de la base")
    base_motor.move_forward(motor_testing_steps)
    time.sleep(0.5)
    base_motor.move_backwards(motor_testing_steps)
    time.sleep(0.5)
    #print(" [TEST] Probando el motor del soporte")
    #disablePrint()
    #motor_y_axis.step(motor_testing_steps, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.SINGLE)
    #time.sleep(0.5)
    #motor_y_axis.step(motor_testing_steps, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.SINGLE)
    #time.sleep(0.5)

def move_motor(steps, direction):
    if print_movement_values == "True":
        print(" MOTOR LOCATION  : [" + str(base_motor.get_position())  + "]")
        print("     STEPS: " + str(steps))
        if direction == FORWARD:
            print(" DIRECTION : FORWARD")
            base_motor.move_forward(steps)
        else:
            print(" DIRECTION : BACKWARD")
            base_motor.move_backwards(steps)


def calculate_moves(center_x, center_y):
   global pan_thread

   # Apertura cámara: 60 grados. Equivale a 38 pasos del motor
   target_x_position = (center_x / 15) - 17 # (Pixels / pixels per step) - pasos maximos
   #move_motor(target_x_position)
   #pan_thread = threading.Thread(target=move_motor(target_x_position))

   steps_to_target = target_x_position - base_motor.get_position()

    # Steps == 0, nada que hacer
   if steps_to_target < 0:
     pan_thread = threading.Thread(target=move_motor(abs(steps_to_target), BACKWARD))
   else:
     pan_thread = threading.Thread(target=move_motor(abs(steps_to_target), FORWARD))

   pan_thread.start()
   #pan_thread.join()


## LIMPIEZA ##

def back_to_center():
    calculate_moves(275,0)
    time.sleep(0.5)
    print(" [INFO] Colocado motor en posición inicial")


def vacuum_cleaner():
    # Liberamos la cámara y cerramos las ventanas
    GPIO.cleanup()
    camera.release()
    time.sleep(1)
    cv2.destroyAllWindows()
    print("[DONE] Roomba pasada. Fin del programa")

###### FIN DE FUNCIONES #####

load_config()   # Cargamos el fichero "config.json"

# Empezamos a capturar la webcam
print("[START] Preparando cámara....")
camera_recording = False

while camera_recording is not True:
    camera = cv2.VideoCapture(0)
    time.sleep(1)

    # Esperamos a que la cámara esté preparada
    camera_recording, _ = camera.read()
print("[DONE] Cámara lista!")

# Inicializamos variables para iterar con la cámara
firstFrame = None
actualFrame = None
count = 0


print("[INFO] Inicializamos los motores...")
base_motor = Stepper(12,16,20,21)
print(" PUERTOS MOTOR BASE: " + base_motor.get_gpio_ports())
if test_base_motor == "True":
    motor_test()
    print (" [TEST] Realizado movimiento en base")

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
        draw_contour(best_contour)
        text = "Objetivo detectado!"

    # Mostramos la fecha y hora en el livestream
    print_date_on_video()

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
