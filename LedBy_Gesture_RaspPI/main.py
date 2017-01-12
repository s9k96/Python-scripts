import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import RPi.GPIO as GPIO
import math
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT) # On if hand detected
GPIO.setup(16, GPIO.OUT) # channel 1
GPIO.setup(20, GPIO.OUT) # channel 2
GPIO.setup(21, GPIO.OUT) # channel 3
GPIO.setup(19, GPIO.OUT) # High
GPIO.setup(26, GPIO.OUT) # LOW

def angle(x,y):
	if x == 0: return None
	return math.fabs(math.degrees(math.atan(y/float(x))))

def updateChannel(i):
	if i == 1:
		GPIO.output(16, GPIO.HIGH)
		GPIO.output(20, GPIO.LOW)
		GPIO.output(21, GPIO.LOW)
	elif i == 2:
		GPIO.output(16, GPIO.LOW)
		GPIO.output(20, GPIO.HIGH)
		GPIO.output(21, GPIO.LOW)
	elif i == 3:
		GPIO.output(16, GPIO.LOW)
		GPIO.output(20, GPIO.LOW)
		GPIO.output(21, GPIO.HIGH)

def updateValue(i, value):
	if value[i - 1] == 0:
		GPIO.output(26, GPIO.HIGH)
		GPIO.output(19, GPIO.LOW)
	if value[i - 1] == 1:
		GPIO.output(26, GPIO.LOW)
		GPIO.output(19, GPIO.HIGH)
	

camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 20
rawCapture = PiRGBArray(camera)

hand_cascade = cv2.CascadeClassifier('hand.xml')
startx, starty = -1, -1
endx, endy = -1, -1
counter = 0
diffx, diffy = 1, 1
channel = [16, 20, 21] # GPIO channel array
value = [0, 0, 0]
i = 1
time.sleep(0.5)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array
 
	# show the frame
	grabbed = False
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.equalizeHist(gray)
	hand = hand_cascade.detectMultiScale(gray, 1.3, 5)
	for (x, y, w, h) in hand:
		cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
	
		counter = 0
		if startx < 0 and starty < 0:
			startx, starty = x, y
	
		grabbed = True
		endx, endy = x, y
	
	counter += 1
	
	diffy = endy - starty 
	diffx = endx - startx
	
	if counter == 5:
		a = angle(diffx, diffy)
		#print diffx, diffy, a
		if math.fabs(diffx) < 30 and diffy < -30:
			print "north"
			value[i - 1] = 1
			updateValue(i, value)
			print "channel ", i, value
		elif math.fabs(diffx) < 30 and diffy > 30:
			print "south"
			value[i - 1] = 0
			updateValue(i, value)
			print "channel ", i, value
		elif diffx < -30 and math.fabs(diffy) < 30:
			print "east"
			i += 1  
			if i > 3: i = 3
			updateChannel(i)
			updateValue(i, value)
			print "channel ", i, value
		elif diffx > 30 and math.fabs(diffy) < 30:
			print "west"
			i -= 1
			if i < 1: i = 1
			updateChannel(i)
			updateValue(i, value)
			print "channel ", i, value

	cv2.putText(image, "diffx " + str(diffx),(100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2,cv2.CV_AA)
	cv2.putText(image, "diffy " + str(diffy),(100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2,cv2.CV_AA)
	if grabbed:
		GPIO.output(18, GPIO.HIGH)
	else:
		GPIO.output(18, GPIO.LOW)
	# print "channel ", i, value
	cv2.imshow("temp", image)
	key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
		
cv2.destroyAllWindows()
camera.close()

