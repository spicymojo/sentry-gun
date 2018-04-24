# -*- coding: UTF-8 -*-
# En este proyecto se utilizan OpenCV 3.1.0 y Python 2.7.13

#####  LIBRERÍAS  #####

# Parseador de argumentos de consola
import argparse

# Librerías para fechas y tiempo
import datetime
import time

# Librerias de OpenCV y auxiliares para tratamiento de imagen
import cv2
import imutils
import numpy as np

# Librerias para los motores
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_StepperMotor

# Opciones de configuración
parser = argparse.ArgumentParser()
parser.add_argument("-s","--size", nargs='?', default=500)
args = vars(parser.parse_args())

# Parseo de las opciones (Tamaño de objetivo)
if 500 == args["size"]:
    minimum_target_area = 500
    print("[CONFIG] Minumum_target_area: 500")
else:
    minimum_target_area = args["size"]
    print("[CONFIG] Minimum_target_area:" + str(args["size"]))


# Valores RGB de los colores utilizados
red = (0,0,255)
green = (0,255,0)

##### FUNCIONES #####

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

    # Creamos un círculo para el centro del cuadrado
    img = np.zeros((512, 512, 3), np.uint8)

    # Dibujamos el centro del cuadrado, es decir, el objetivo
    draw_center_circle(x,y,w,h)

    # Dibujamos el marco del objetivo
    cv2.rectangle(frame, (x, y), (x + w, y + h), green, 2)

def draw_center_circle(x,y,w,h):
    # PARÄMETROS PARA DIBUJAR EL CÍRCULO
    # cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]])

    square_center_x = x + w / 2
    square_center_y = y + h / 2
    cv2.circle(frame, (square_center_x, square_center_y), 5, red, -1)

def write_date_on_video():
    # Imprimimos el texto y la fecha en la ventana
    cv2.putText(frame, "Estado: {}".format(text), (10, 25),
        cv2.FONT_HERSHEY_PLAIN, 1.25, red, 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
        (10, frame.shape[0] - 15), cv2.FONT_HERSHEY_PLAIN, 1, red, 1)

def motor_test():
    # Probamos el motor de la base
    print(" [TEST] Probando el motor de la base")
    motor_x_axis.step(25, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.SINGLE)
    motor_x_axis.step(25, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.SINGLE)


###### FIN DE FUNCIONES #####

# Empezamos a capturar la webcam
print("[START] Preparando cámara....")
camera_recording = False

while camera_recording is not True:
    camera = cv2.VideoCapture(0)
    time.sleep(1)

    # Esperamos a que la cámara esté preparada
    camera_recording, _ = camera.read()

# Inicializamos variables para iterar con la cámara
firstFrame = None
actualFrame = None
count = 0
print("[DONE] Cámara lista!")

print("[INFO] Inicializamos los motores...")
mh = Adafruit_MotorHAT(addr = 0x60)
motor_x_axis = mh.getStepper(200,1)
motor_y_axis = mh.getStepper(200,2)
#motor_test()

# Loop sobre la camara
while True:
    # Cogemos el frame inicial y ponemos el texto
    (video_signal, frame) = camera.read()

    text = "No hay objetivos"

    # Redimensionamos el frame, lo convertimos a escala de grises
    # y lo desenfocamos (Blur)
    frame = imutils.resize(frame, width=500)
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

    # compute the absolute difference between the current frame and
    # first frame
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
    write_date_on_video()

    # Mostramos el frame actual, y comprobamos si el usuario quiere salir
    cv2.imshow("Cámara", frame)
    cv2.imshow("Umbralizado", thresh)
    cv2.imshow("Frame Delta", frameDelta)
    key = cv2.waitKey(1) & 0xFF

    # Q = Salir del programa
    if key == ord("q"):
        print("[END] Apagando el sistema...")
        break

# Liberamos la cámara y cerramos las ventanas
camera.release()
time.sleep(1)  # Liberamos correctamente la cámara
cv2.destroyAllWindows()

