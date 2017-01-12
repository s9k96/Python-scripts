import cv2
# from picamera.array import PiRGBArray
# from picamera import PiCamera
import time
# import RPi.GPIO as GPIO
import math
import os

def angle(x,y):
	if x == 0: return None
	return math.fabs(math.degrees(math.atan(y/float(x))))





hand_cascade = cv2.CascadeClassifier('hand.xml')
startx, starty = -1, -1
endx, endy = -1, -1
counter = 0
diffx, diffy = 1, 1
channel = [16, 20, 21] # GPIO channel array
value = [0, 0, 0]
i = 1
time.sleep(0.5)

cap= cv2.VideoCapture(0)

while(cap.isOpened()):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	_, image = cap.read()
 
	# show the frame
	grabbed = False
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.equalizeHist(gray)
	hand = hand_cascade.detectMultiScale(gray, 1.3, 5)
	for (x, y, w, h) in hand:
		cv2.rectangle(image, (x, y), (x,y), (255, 0, 0), 2)
	
		counter = 0
		if startx < 0 and starty < 0:
			startx, starty = x, y
	
		grabbed = True
		endx, endy = x, y
		cv2.rectangle(image, (startx, starty), (endx,endy), (25, 200, 0), 2)
	counter += 1
		# print startx, starty, endx, endy

	
	
	diffy = endy - starty 
	diffx = endx - startx
	
	if counter == 5:
		a = angle(diffx, diffy)
		#print diffx, diffy, a
		if math.fabs(diffx) < 30 and diffy < -30:
			print "north"
			value[i - 1] = 1
			print "channel ", i, value
		elif math.fabs(diffx) < 30 and diffy > 30:
			print "south"
			value[i - 1] = 0
			print "channel ", i, value
		elif diffx < -30 and math.fabs(diffy) < 30:
			print "east"
			i += 1  
			if i > 3: i = 3
			print "channel ", i, value
		elif diffx > 30 and math.fabs(diffy) < 30:
			print "west"
			i -= 1
			if i < 1: i = 1
			print "channel ", i, value

		if counter > 10:
			startx = -1
			starty = -1	
	counter += 1
	if counter > 10:
		startx = -1
		starty = -1		

	cv2.putText(image, "diffx " + str(diffx),(100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2)
	cv2.putText(image, "diffy " + str(diffy),(100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2)
	cv2.imshow("temp", image)
	key = cv2.waitKey(1) & 0xFF
 
 
	if key == ord("q"):
		break
		
cv2.destroyAllWindows()
