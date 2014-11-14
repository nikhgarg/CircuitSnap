import numpy as np
import cv2

############# does a pretty good job of finding all the elements besides resistors. Could probably do some machine learning to characterize the elements
# from the rectangles that this generates.

##adapting from here: https://stackoverflow.com/questions/9413216/simple-digit-recognition-ocr-in-opencv-python
# https://github.com/goncalopp/simple-ocr-opencv also can be a good guide (haven't checked the code out yet)
im = cv2.imread('images/3.PNG',cv2.CV_LOAD_IMAGE_COLOR)
im3 = im.copy();

gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(gray,255,1,1,11,2)

#################      Now finding Contours         ###################

contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

print thresh
print np.shape(thresh)
print np.shape(im);
samples =  np.empty((0,100))
responses = []
keys = [i for i in range(48,58)]

for cnt in contours:
    if cv2.contourArea(cnt)>1:
        [x,y,w,h] = cv2.boundingRect(cnt)
        #element_only = thresh[range(y, y+h)]
        #element_only = element_only[:, range(x, x+w)]
        #cv2.imshow('norm', element_only);
        cv2.rectangle(im,(x,y),(x+w,y+h),(0,0,255),2)
        roi = thresh[y:y+h,x:x+w]
        roismall = cv2.resize(roi,(10,10))
        #cv2.imshow('norm',roi)
        #key = cv2.waitKey(0)
        cv2.imshow('norm', im);
        key = cv2.waitKey(0);
        #raw_input("press enter for next element");
key = cv2.waitKey(0)