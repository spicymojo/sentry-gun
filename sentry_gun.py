# -*- coding: UTF-8 -*-

# Este proyecto utiliza OpenCV 3.1.0 y Python 2.7.13

# Importamos los paquetes necesarios
import argparse
import datetime
import imutils
import time
import cv2
import numpy as np
import argparse

# Opciones de configuración
parser = argparse.ArgumentParser()
parser.add_argument("-s","--size", nargs='?', default=500)
args = vars(parser.parse_args())

# Definimos el tamaño mínimo que debe tener el obetivo para ser detectado
if 500 == args["size"]:
    minimum_target_area = 500
    print("Minumum_target_area: 500")
else:
    minimum_target_area = args["size"]
    print("Minimum_target_area:" + str(args["size"]))

print("[START] Arrancando cámara")

# Empezamos la captura del vídeo de la webcam
camera = cv2.VideoCapture(0)

# Dejamos tiempo para que la cámara arranque (Si no, da errores de compilación)
time.sleep(2.5)
print("[DONE] Cámara ready")

# Capturamos el primer frame [Base]
firstFrame = None

# Inicializamos las variables para almacenar el último objetivo detectado
last_target_x = 0
last_target_y = 0

# Loop sobre la camara
while True:
    # Cogemos el frame inicial y ponemos el texto
    (video_signal, frame) = camera.read()
    text = "No hay objetivos"

    # Si no tenemos frame, es que no hay video
    if not video_signal:
        break

    # Resize al frame, convertir a escala de grises
    # y le hacemos el blur
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # Si no hay primer frame, lo inicializamos
    if firstFrame is None:
        firstFrame = gray
        print("INICIALIZADO PRIMER FRAME")
        continue

    #  Calculamos la diferencia absoluta entre el primer frame
    #  y el frame actual (Es decir, el frame delta)

    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

    # Dilatamos la imagen umbralizada para rellenar los huecos, entonces
    # encontramos los contornos de dicha imagen

    thresh = cv2.dilate(thresh, None, iterations=2)

    # Esta cadena es en Python 2.7
    #(cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
    #	cv2.CHAIN_APPROX_SIMPLE)
    (_,cnts, _) = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    # Bucle sobre los contornos
    for c in cnts:
        # Contorno pequeno (menor de 500)? Pasamos
        if cv2.contourArea(c) < minimum_target_area:
            continue

        # Calcular el cuadrado, dibujarlo y actualizar el texto
        (x, y, w, h) = cv2.boundingRect(c)

        # Creamos un círculo para el centro del cuadrado
        img = np.zeros((512, 512, 3), np.uint8)

        # Dibujamos el centro del cuadrado
        center_x = x + w/2
        center_y = y+h/2
        cv2.circle(frame, (center_x,center_y ), 5, (0, 0, 255), -1)
        if center_x != last_target_x or center_y != last_target_y:
            last_target_x = center_x
            last_target_y = center_y
            print("NEW TARGET: [" + str(last_target_x) + "," + str(last_target_y) + "]")

        # PARÄMETROS DE DIBUJAR EL CÍRCULO
        # cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]])
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
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
        print("APAGANDO SISTEMA...")
        break

# Liberamos la cámara y cerramos las ventanas
camera.release()
cv2.destroyAllWindows()
