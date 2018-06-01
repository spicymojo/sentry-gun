import cv2 
cap = cv2.VideoCapture(0)

while(True):
	f,frame=cap.read()
	cv2.circle(frame, (320,240), 8, (0,0,255), -1)
	cv2.imshow('Video',frame)
	ch = cv2.waitKey(20)

	if ch == 27:
		break
cap.release()
cv2.destroyAllWindows()
