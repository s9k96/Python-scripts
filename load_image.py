import numpy as np
import cv2

img = cv2.imread('img01.jpg',1)
cv2.imshow('image',img)
k = cv2.waitKey(0)
if k == 27:        
    cv2.destroyAllWindows()
