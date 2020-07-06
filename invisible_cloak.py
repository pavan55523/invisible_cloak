import cv2
import numpy as np
import time

print("""Wind up a Red Cloak to become invisible """)


cap = cv2.VideoCapture(0)
time.sleep(3)
background=0
for i in range(30):
	ret,background = cap.read()

background = np.flip(background,axis=1)

while(cap.isOpened()):
	ret, img = cap.read()
	
	# Flipping the image (Can be uncommented if needed)
	img = np.flip(img,axis=1)
	
	# Converting image to HSV color space.
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	value = (35, 35)
	
	blurred = cv2.GaussianBlur(hsv, value,0)
	
	# Defining lower range for red color detection.
	lower_red = np.array([0,120,70])
	upper_red = np.array([10,255,255])
	mask1 = cv2.inRange(hsv,lower_red,upper_red)
	
	# Defining upper range for red color detection
	lower_red = np.array([170,120,70])
	upper_red = np.array([180,255,255])
	mask2 = cv2.inRange(hsv,lower_red,upper_red)
	
	# Addition of the two masks to generate the final mask.
	mask1 = mask1+mask2
	mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3,3),np.uint8),iterations=2)
	mask1 = cv2.dilate(mask1,np.ones((3,3),np.uint8),iterations=1)
	mask2 = cv2.bitwise_not(mask1)
        
        # Replacing pixels
	res1 = cv2.bitwise_and(background,background,mask=mask1)
	res2 = cv2.bitwise_and(img,img,mask=mask2)
	img= cv2.addWeighted(res1,1,res2,1,0)
	cv2.imshow('Display',img)
	k = cv2.waitKey(10)
	if k == 27:
		break

