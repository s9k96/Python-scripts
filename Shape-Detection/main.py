# -*- coding: utf-8 -*-
import cv2
# import cv2.cv as cv
import numpy as np

def find_box(y,x):
	if x<100:
		if y<100:
			box=1
		elif y>100 and y<200:
			box=2
		else:
			box=3	
	elif x>100 and x<200:
		if y<100:
			box=4
		elif y>100 and y<200:
			box=5
		else:
			box=6
	if x>200:
		if y<100:
			box=7
		elif y>100 and y<200:
			box=8
		else:
			box=9	
	return box								


def find_color(x,y):
	img = cv2.imread("test_images/board_4.jpg")
	variable = img[y,x]
	
	if variable[1]> 200 and int(variable[0])+int(variable[1]) <10:
		return "green"
	elif  variable[2]> 200 and int(variable[1])+int(variable[0]) <10:
		return 'red'	
	elif   variable[2]> 200 and variable[1]>200:
		return 'yellow'	
	else:
		return 'blue'	

	# return variable	




def main(board_filepath, container_filepath):

	board 	 =	cv2.imread("test_images/board_4.jpg")
	container=	cv2.imread("test_images/container_1.jpg")
	cv2.imshow('board', board)
	cv2.imshow('cont', container)
				############ FOR SHAPE #####################
	bcopy1		=	board.copy()
	gray_bcopy1 =	cv2.cvtColor(bcopy1, cv2.COLOR_BGR2GRAY)
	circles = cv2.HoughCircles(gray_bcopy1, cv2.HOUGH_GRADIENT, 5, 1000)
	# print "circles",circles

	ret,thresh = cv2.threshold(gray_bcopy1,127,255,1)
	# cv2.imshow('bagg', gray_bcopy1)

	l=[]
	_,contours,h = cv2.findContours(thresh,1,2)
	for cnt in contours:
	    approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)

	    if len(approx)==3:
			
			cv2.drawContours(board,[cnt],0,(100,100,10),-1)
			x,y,w,h = cv2.boundingRect(cnt)
	   		cv2.rectangle(board,(x,y),(x+w,y+h),(0,255,0),2)
	   		# print find_color(x+(w/2), y+(h/2)) ,"Triangle", find_box(x,y)
	   		tup=(find_box(x,y),find_color(x+(w/2), y+(h/2)) ,"Triangle ", )
	   		l.append(tup)

	    elif len(approx)==4:
	    	
	    	if cv2.contourArea(cnt)<5183:
	    		x,y,w,h = cv2.boundingRect(cnt)
	    		# mask = np.zeros(.shape,np.uint8)
	    		#, cv2.mean(cnt, mask=mask)
	    		# cv2.drawContours(board,[cnt],0,(100,100,10),-1)	
	    		cv2.rectangle(board,(x, y),(x+w,y+h),(0,255,0),2)
	    		# print find_color(x+(w/2), y+(h/2))," 4- sided", find_box(x+(w/2),y+(h/2))
	    		tup=(find_box(x+(w/2),y+(h/2)), find_color(x+(w/2), y+(h/2))," 4- sided ", )
	    		l.append(tup)
	    
	    elif len(approx) > 15:
			cv2.drawContours(board,[cnt],0,(100,100,10),-1)
			x,y,w,h = cv2.boundingRect(cnt)
			cv2.rectangle(board,(x,y),(x+w,y+h),(0,255,0),2)
			# print find_color(x+(w/2), y+(h/2)) ,"circle", find_box(x,y)
			tup=(find_box(x,y), find_color(x+(w/2), y+(h/2)) ,"circle ", )
			l.append(tup)


	cv2.imshow('boarda', board)
	s=set(l)
	l=list(s)
	l.sort(key=lambda tup: tup[0])
	print l








	board_objects = []		# List to store output of board -- DO NOT CHANGE VARIABLE NAME
	output_list = []		# List to store final output 	-- DO NOT CHANGE VARIABLE NAME
	
	return board_objects, output_list	



if __name__ == '__main__':
    

	board_filepath = "test_images/board_4.jpg"    			# change filename of board provided to you 
	container_filepath = "test_images/container_1.jpg"		# change filename of container as required for testing

	main(board_filepath,container_filepath)

	cv2.waitKey(0)
	cv2.destroyAllWindows()    
