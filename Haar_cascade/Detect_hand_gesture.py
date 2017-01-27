import cv2
import numpy as np
import math
import os
import csv

hand_cascade = cv2.CascadeClassifier('hand.xml')
cap = cv2.VideoCapture(0)

startx, starty = -1, -1
endx, endy = -1, -1
counter = 0
grabbed = False
diffx = 0
diffy = 0
channel=0
while cap.isOpened():
    data=['KEY_POWER 0 1 NIL NIL 0 ', 
    'KEY_TEMP_UP 17 34 NIL NIL 17', 
    'KEY_TEMP_DOWN 17 34 NIL NIL 34', 
    'KEY_DIRECT 0 1 NIL NIL 0', 
    'KEY_FAN 0 1 NIL NIL 0']


    _, frame = cap.read()
    frame1 = frame.copy()
    gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    hand = hand_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in hand:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        counter = 0
        if startx < 0 and starty < 0:
            startx, starty = x, y
        endx, endy = x, y
    diffx = endx - startx
    diffy = endy - starty


    if counter==5 and abs(diffx)>100:
        if(endx-startx)>0:
            channel -=1
        else:
            channel +=1    
    cv2.putText(frame, str(channel), (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 3,(255,200,255),2,cv2.LINE_AA)

    if channel==1:
        cv2.putText(frame, 'channel 1: volume', (450, 100), cv2.FONT_HERSHEY_SIMPLEX, 1,(20,0,255),2,cv2.LINE_AA)
        cv2.putText(frame, str(abs(diffy/70)), (450, 130), cv2.FONT_HERSHEY_SIMPLEX, 1,(200,200,255),2,cv2.LINE_AA)
        string= 'KEY_TEMP_UP 17 34 NIL NIL '+ str(abs(diffy/70))
        data[1]= string
        print data
    out=open('params.csv', 'w+')
    out.write(str(data))
    out.close()

    counter += 1
    if counter > 10:
        startx = -1
        starty = -1
    cv2.imshow('temp', frame)

    k = cv2.waitKey(10)
    if k == 27 & 0xFF:
        break

cap.release()
cv2.destroyAllWindows()

