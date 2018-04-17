# -*- coding: UTF-8 -*-

# Este proyecto utiliza OpenCV 3.1.0 y Python 2.7.13

import argparse
# Importamos los paquetes necesarios
import datetime
import time
import cv2
import imutils
import numpy as np

# Opciones de configuración
parser = argparse.ArgumentParser()
parser.add_argument("-s","--size", nargs='?', default=500)
args = vars(parser.parse_args())

# Definimos los colores utilizados, para facilitar la lectura
red = (0,0,255)
green = (0,255,0)

# FUNCIONES
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
    # Inicializamos las variables para almacenar el último objetivo detectado
    last_target_x = 0
    last_target_y = 0

    # Calcular el cuadrado, dibujarlo y actualizar el texto
    (x, y, w, h) = cv2.boundingRect(contour)

    # Creamos un círculo para el centro del cuadrado
    img = np.zeros((512, 512, 3), np.uint8)

    # Dibujamos el centro del cuadrado
    center_x = x + w / 2
    center_y = y + h / 2
    cv2.circle(frame, (center_x, center_y), 5, red, -1)

    if center_x != last_target_x or center_y != last_target_y:
        last_target_x = center_x
        last_target_y = center_y
        print("NEW TARGET: [" + str(last_target_x) + "," + str(last_target_y) + "]")

    # PARÄMETROS PARA DIBUJAR EL CÍRCULO
    # cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]])

    # Dibujamos el marco del objetivo
    cv2.rectangle(frame, (x, y), (x + w, y + h), green, 2)

# CONFIGURACIÓN DEL PROGRAMA

# Tamaño mínimo de objetivo
if 500 == args["size"]:
    minimum_target_area = 500
    print("[CONFIG] Minumum_target_area: 500")
else:
    minimum_target_area = args["size"]
    print("[CONFIG] Minimum_target_area:" + str(args["size"]))

print("[START] Preparando cámara....")

# Empezamos la captura del vídeo de la webcam
camera_recording = False

while camera_recording is not True:
    camera = cv2.VideoCapture(0)
    time.sleep(1)

    # El primer parámetro será True cuando la cámara esté preparada
    camera_recording, _ = camera.read()

print("[DONE] Cámara lista!")

# Definimos los frames a utilizar
firstFrame = None
actualFrame = None
count = 0

# Loop sobre la camara
while True:
    # Cogemos el frame inicial y ponemos el texto
    (video_signal, frame) = camera.read()

    text = "No hay objetivos"

    # Resize al frame, convertir a escala de grises
    # y le hacemos el blur
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
            #  Calculamos la diferencia absoluta entre el primer frame
            #  y el frame actual (Es decir, el frame delta)
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

    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)

    # Buscamos el contorno del mayor objetivo
    best_contour = find_best_target()

    # Bucle sobre los contornos
    if best_contour is not None:
        draw_contour(best_contour)
        text = "Objetivo detectado!"

    # Imprimimos el texto y la fecha en la ventana
    cv2.putText(frame, "Estado: {}".format(text), (10, 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
        (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

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
cv2.destroyAllWindows()

