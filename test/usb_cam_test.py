import cv2 
cap = cv2.VideoCapture(0)

while(True):
	f,frame=cap.read()
	frame=cv2.resize(frame,(800,600))
	cv2.imshow('Video',frame)
	ch = cv2.waitKey(20)

	if ch == 27:
		break
cap.release()
cv2.destroyAllWindows()
