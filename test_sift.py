import cv2
import numpy as np


imgstring = "2";
imgtype = ".PNG";
img = cv2.imread("images/" + imgstring + imgtype,cv2.CV_LOAD_IMAGE_COLOR)
gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(gray,255,1,1,11,2)


#sift = cv2.SIFT()
surf = cv2.SURF(400)

# Initiate FAST object with default values
fast = cv2.FastFeatureDetector()

## find and draw the keypoints
#fast.setBool('nonmaxSuppression',0)
#kp = fast.detect(thresh,None)
#img2 = cv2.drawKeypoints(thresh, kp, color=(255,0,0))

## Print all default params
#print "Threshold: ", fast.getInt('threshold')
#print "nonmaxSuppression: ", fast.getBool('nonmaxSuppression')
##print "neighborhood: ", fast.getInt('type')
#print "Total Keypoints with nonmaxSuppression: ", len(kp)
#cv2.imshow('norm',img2);


kp, des = surf.detectAndCompute(img,None)
print kp
img=cv2.drawKeypoints(img,kp,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
cv2.imshow('key', img);
key = cv2.waitKey(0)
