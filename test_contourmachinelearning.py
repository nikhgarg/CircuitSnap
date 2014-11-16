import numpy as np
import cv2
import os, os.path


##adapting from here: https://stackoverflow.com/questions/9413216/simple-digit-recognition-ocr-in-opencv-python
# https://github.com/goncalopp/simple-ocr-opencv also can be a good guide (haven't checked the code out yet)

SIZESMALLSAVED = 10;

#######   training part    ############### 

## need to load from all images/datasets instead of just one dataset
samples = None;
responses = None;
dirtocheck = "./trainingdata/";
responsespath = "responses";
samplespath = "samples";
for root, _, files in os.walk(dirtocheck + responsespath):
    for f in files:
        fullpath = os.path.join(root, f)
        print f
        newResponses = np.loadtxt(fullpath, np.float32)
        newResponses = newResponses.reshape((newResponses.size,1));
        if responses is None:
            responses = newResponses;
        else:
            responses = np.append(responses, newResponses);
for root, _, files in os.walk(dirtocheck + samplespath):
    for f in files:
        fullpath = os.path.join(root, f)
        print f
        newSamples = np.loadtxt(fullpath, np.float32)
        if samples is None:
            samples = [newSamples];
        else:
            samples = np.append(samples, [newSamples]);
samples = samples.reshape(np.size(responses),np.size(samples)/np.size(responses)); 

model = cv2.KNearest()
model.train(samples,responses)

############################# testing part  #########################

imgstring = "12";
imgtype = ".PNG";
im = cv2.imread("images/" + imgstring + imgtype,cv2.CV_LOAD_IMAGE_COLOR)
out = np.zeros(im.shape,np.uint8)
gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(gray,255,1,1,11,2)

contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

print responses
for cnt in contours:
    if cv2.contourArea(cnt)>1:
        [x,y,w,h] = cv2.boundingRect(cnt)
        cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
        roi = thresh[y:y+h,x:x+w]
        roismall = cv2.resize(roi,(SIZESMALLSAVED,SIZESMALLSAVED))
        roismall = roismall.reshape((1,SIZESMALLSAVED*SIZESMALLSAVED))
        roismall = np.float32(roismall)
        retval, results, neigh_resp, dists = model.find_nearest(roismall, k = 1)
        string = str(chr((results[0][0])))
        cv2.putText(out,string,(x,y+h),0,1,(0,255,0))

cv2.imshow('im',im)
cv2.imshow('out',out)
cv2.waitKey(0)