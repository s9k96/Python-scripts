import cv2 
import numpy as np

def nothing(x):
	pass

h=0
cap=cv2.VideoCapture(0)
cv2.namedWindow('controls')
cv2.createTrackbar('Hmin','controls',78,255,nothing)
cv2.createTrackbar('Hmax','controls',129,255,nothing)
cv2.createTrackbar('Smin','controls',99,255,nothing)
cv2.createTrackbar('Smax','controls',255,255,nothing)
cv2.createTrackbar('Vmin','controls',81,255,nothing)
cv2.createTrackbar('Vmax','controls',255,255,nothing)

while cap.isOpened():
	ret,frame=cap.read()
	blur=frame#cv2.GaussianBlur(frame, (11,11),0)
	hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
	# cv2.imshow('hsv', hsv)
	# hmin = cv2.getTrackbarPos('H','controls')
	# smin = cv2.getTrackbarPos('S','controls')
	# vmin = cv2.getTrackbarPos('V','controls')
	lower=np.array([cv2.getTrackbarPos('Hmin','controls'),cv2.getTrackbarPos('Smin','controls'),cv2.getTrackbarPos('Vmin','controls')])
	upper=np.array([cv2.getTrackbarPos('Hmax','controls'),cv2.getTrackbarPos('Smax','controls'),cv2.getTrackbarPos('Vmax','controls')])
	# print lower,upper
	mask=cv2.inRange(hsv, lower, upper)
	mask = cv2.erode(mask, None, iterations=1)
	mask = cv2.dilate(mask, None, iterations=1)
	cv2.imshow('mask',mask)
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
	if len(cnts)>0:
		c = max(cnts, key=cv2.contourArea)
		# ((x, y), radius) = cv2.minEnclosingCircle(c)
		(x,y,w,h)=cv2.boundingRect(c)
		# M = cv2.moments(c)
		# center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		if w>10:
			# cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
			cv2.rectangle(frame, (x,y),(x+w,y+h),(0, 255, 255), 2)
			cv2.putText(frame, 'Detecting', (10, 30), cv2.FONT_HERSHEY_DUPLEX,0.65, (0, 0, 255), 2)
			a= x+w/2
			b= y+h/2
			cv2.rectangle(frame,   (a,b)  ,   (a,b)   ,(0, 0, 255), 5)
			print x,y,w,h
	cv2.imshow('frame', frame)

	k = cv2.waitKey(1) & 0xFF
	if k == 27:
		break
	
cap.release()




