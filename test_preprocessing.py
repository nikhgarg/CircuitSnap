import numpy as np
import cv2
import os, os.path

imgstring = "1";
imgtype = ".PNG";

##does not work to close the Ohm sign when broken at the top. 

featurestype = "";

im = cv2.imread("images/" + imgstring + imgtype,cv2.CV_LOAD_IMAGE_COLOR)
im3 = im.copy();

gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(gray,255,1,1,11,2)
#cv2.imshow('norm', gray);
#key = cv2.waitKey(0)
kernel = np.ones((2,2),np.uint8)
dilation= cv2.dilate(thresh,kernel,iterations = 1)
erosion= cv2.erode(dilation,kernel,iterations = 1)

cv2.imshow('dilate', erosion);
key = cv2.waitKey(0)
