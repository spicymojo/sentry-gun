# Importamos los paquetes necesarios
import argparse
import datetime
import imutils
import time
import cv2
 
# Construimos el parser y le pasamos los argumentos
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())
 
# Leemos de la webcam
camera = cv2.VideoCapture(0)
time.sleep(0.25)
 
# Capturamos el primer frame [Base]
firstFrame = None

# Loop sobre el video/la cam
while True:
	# Cogemos el frame inicial y ponemos el textot
	(grabbed, frame) = camera.read()
	text = "SecuredZone"
 
	# Si no tenemos frame, es que no hay video
	if not grabbed:
		break
 
	# Resize al frame, convertir a escala de grises
	# y le hacemos el blur 
	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)
 
	# Si no hay primer frame, lo inicializamos
	if firstFrame is None:
		firstFrame = gray
		continue

	#  Calculamos la diferencia absoluta entre el primer frame
	#  y el frame actual 

	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
 
	# Dilatamos la imagen umbralizada para rellenar los huecos, entonces
	# encontramos los contornos de dicha imagen

	thresh = cv2.dilate(thresh, None, iterations=2)
 	(_,cnts, _) = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	
	# Bucle sobre los contornos
	for c in cnts:
		# Contorno pequeno? Pasamos 
		if cv2.contourArea(c) < args["min_area"]:
			continue
 
		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		text = "Danger"

	# draw the text and timestamp on the frame
	cv2.putText(frame, "Estado: {}".format(text), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
 
	# show the frame and record if the user presses a key
	cv2.imshow("Security Feed", frame)
	cv2.imshow("Thresh", thresh)
	cv2.imshow("Frame Delta", frameDelta)
	key = cv2.waitKey(1) & 0xFF
 
	# Q = Escape
	if key == ord("q"):
		break
 
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
