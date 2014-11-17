import numpy as np
import cv2

############# does a pretty good job of finding all the elements besides resistors. Could probably do some machine learning to characterize the elements
# from the rectangles that this generates.

#things to add/change
    #different SIZESMALLSAVED - increase
    #start saving other information, such as the original area of the contour
        #that will definitely help with things, as elements tend to remain the same size
        #will have to decode as a ratio of max/min though, as size changes

##adapting from here: https://stackoverflow.com/questions/9413216/simple-digit-recognition-ocr-in-opencv-python
# https://github.com/goncalopp/simple-ocr-opencv also can be a good guide (haven't checked the code out yet)

<<<<<<< HEAD
im = cv2.imread('images/5.PNG',cv2.CV_LOAD_IMAGE_COLOR)
=======
imgstring = "1";
imgtype = ".PNG";

im = cv2.imread("images/" + imgstring + imgtype,cv2.CV_LOAD_IMAGE_COLOR)
>>>>>>> 969811f8cd95402d6e29c485e4957112e8c43108
im3 = im.copy();

gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(gray,255,1,1,11,2)

SIZESMALLSAVED = 10;

#################      Now finding Contours         ###################

contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

print thresh
print np.shape(thresh)
print np.shape(im);
samples =  np.empty((0,100))
responses = []
#keys = [i for i in range(48,58)]

for cnt in contours:
    if cv2.contourArea(cnt)>15 :
        [x,y,w,h] = cv2.boundingRect(cnt)
        im = im3.copy();
        #element_only = thresh[range(y, y+h)]
        #element_only = element_only[:, range(x, x+w)]
        #cv2.imshow('norm', element_only);
        cv2.rectangle(im,(x,y),(x+w,y+h),(0,0,255),2)
        roi = thresh[y:y+h,x:x+w]
        roismall = cv2.resize(roi,(SIZESMALLSAVED,SIZESMALLSAVED))
        #cv2.imshow('norm',roi)
        #key = cv2.waitKey(0)
        cv2.imshow('norm', im);
        key = cv2.waitKey(0);
        #raw_input("press enter for next element");
        if key == 27:  # (escape to quit)
            sys.exit()
        else:
        #elif key in keys:
            responses.append(ord(chr(key)))
            sample = roismall.reshape((1,SIZESMALLSAVED*SIZESMALLSAVED))
            samples = np.append(samples,sample,0)
            print sample
            print responses

responses = np.array(responses,np.float32)
responses = responses.reshape((responses.size,1))
print "training complete"

path = "./trainingdata/";

np.savetxt(path + imgstring+"generalsamples.data",samples)
np.savetxt(path + imgstring+"generalresponses.data",responses)
key = cv2.waitKey(0)

#key for printing stuff:
#numbers (obvious)
#ohm - O
#entire voltage source - S
#mesh loop - M
#entire circuit - C
#other, uncategorible - space
#V - V
#A, R 
