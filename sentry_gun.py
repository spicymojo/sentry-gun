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
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_StepperMotor

# Lectura de configuración
import json

# Multihilo para los motores
import thread
import threading

# Librerias para evitar que los driver del motor impriman por consola
import sys, os

# Fuente para la interfaz
message_font = cv2.FONT_HERSHEY_PLAIN
pan_motor_position= 16

# Hilos para los motores
pan_thread = threading.Thread()
tilt_thread = threading.Thread()

##### FUNCIONES #####
def load_config():
    config = json.load(open('config.json'))
    global minimum_target_area, frame_width, exit_key, motor_revs, \
        motor_testing_steps, maximum_right_steps, maximum_left_steps,\
        frame_color,center_color

    minimum_target_area= config['GENERAL']['MINIMUM_TARGET_AREA']
    frame_width = config['GENERAL']['FRAME_WIDTH']
    exit_key = config['GENERAL']['EXIT_KEY']
    motor_revs = config['MOTOR']['MOTOR_REVS']
    motor_testing_steps = config['MOTOR']['TESTING_STEPS']
    maximum_right_steps = config['MOTOR']['MAXIMUM_RIGHT_STEPS']
    maximum_left_steps = config['MOTOR']['MAXIMUM_LEFT_STEPS']
    frame_color = string_to_rgb(config['GENERAL']['TARGET_FRAME_COLOR'])
    center_color = string_to_rgb(config['GENERAL']['TARGET_CENTER_COLOR'])
    maximum_right_steps = config['MOTOR']['MAXIMUM_RIGHT_STEPS']

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
    # Calcular el cuadrado, dibujarlo y actualizar el texto
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
    # pan_thread = threading.Thread(target=calculate_moves(abs(steps_to_target), direction))
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
    motor_x_axis.step(motor_testing_steps, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.SINGLE)
    motor_x_axis.step(motor_testing_steps, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.SINGLE)

def move_motor(target_x_position, direction):
    global pan_motor_position

    print(" MOTOR LOCATION  : [" + str(pan_motor_position) + "]")
    print(" TARGET LOCATION : [" + str(target_x_position) + "]")
    steps_number = target_x_position-pan_motor_position
    print("     STEPS: " + str(steps_number))

    disablePrint()
    motor_x_axis.step(abs(steps_number), direction, Adafruit_MotorHAT.INTERLEAVE)
    enablePrint()
    pan_motor_position = pan_motor_position + steps_number

def calculate_moves(center_x, center_y):
   global pan_thread, pan_motor_position, steps_to_target

   # La lente de la cámara, 60 grados, equivale a 33 pasos del motor
   target_x_position = (center_x / 15) # (Pixels / pixels per step)
   steps_to_target = target_x_position - pan_motor_position

   if steps_to_target < 0:
     #pan_motor_position += 1
     direction = Adafruit_MotorHAT.FORWARD
     pan_thread = threading.Thread(target=move_motor(target_x_position, direction))
   elif steps_to_target >= 0:
     #pan_motor_position -= 1
     direction = Adafruit_MotorHAT.BACKWARD
     pan_thread = threading.Thread(target=move_motor(target_x_position, direction))

   pan_thread.start()
       #pan_thread.join()

   #pan_thread.start()


def disablePrint():
    sys.stdout = open(os.devnull, 'w')

# Activamos de nuevo
def enablePrint():
    sys.stdout = sys.__stdout__

def vacuum_cleaner():
    # Liberamos la cámara y cerramos las ventanas
    camera.release()
    time.sleep(1)
    cv2.destroyAllWindows()
    print("[DONE] Roomba pasada. Fin del programa")

###### FIN DE FUNCIONES #####

# Cargamos la configuración del archivo JSON
load_config()
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
mh = Adafruit_MotorHAT(addr = 0x60)
motor_x_axis = mh.getStepper(motor_revs,1)
motor_y_axis = mh.getStepper(motor_revs,2)
#motor_test()

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
            print(" [INFO] Empezando captura de vídeo... ")
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
                print(" [INFO] Esperando movimiento...")
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
        print("[END] Apagando el sistema...")
        break

# Limpiamos todo
vacuum_cleaner()
