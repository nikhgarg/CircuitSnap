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

imgstring = "sadiku1";
isPhoto = False;
if isPhoto:
    imgtype = ".jpg";   
    featurestype = "photo/";
else:
    imgtype = ".PNG";
    featurestype = "fft/";

im = cv2.imread("images/" + imgstring + imgtype,cv2.CV_LOAD_IMAGE_COLOR)
resized = []
if isPhoto:
    im = cv2.resize(im, dsize = (0,0), fx = .1, fy = .1, interpolation = cv2.INTER_CUBIC);
im3 = im.copy();
out = np.zeros(im.shape,np.uint8)
gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
if isPhoto:
    thresh = cv2.GaussianBlur(gray,(5,5),1)
else:
    thresh = gray;
thresh = cv2.adaptiveThreshold(thresh,255,adaptiveMethod = cv2.ADAPTIVE_THRESH_GAUSSIAN_C,thresholdType = cv2.THRESH_BINARY,blockSize = 11, C=2)

surf = cv2.SURF(400)


SIZESMALLSAVED = 20;

#################      Now finding Contours         ###################
cv2.imshow('thresh',thresh);
contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

print thresh
print np.shape(thresh)
print np.shape(im);
samples =  np.empty((0,2*SIZESMALLSAVED*SIZESMALLSAVED))
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
        roi = gray[y:y+h,x:x+w]
        kp, des = surf.detectAndCompute(roi,None)
        print len(kp)
        img=cv2.drawKeypoints(roi,kp,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        roismall = cv2.resize(roi,(SIZESMALLSAVED,SIZESMALLSAVED))
        regionfft = abs(np.fft.fft2(roismall))
        cv2.imshow('surf',roismall);
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
            fftsample = regionfft.reshape((1, SIZESMALLSAVED*SIZESMALLSAVED));
            print np.size(sample);
            print np.size(fftsample);
            print np.size(samples);
            sample = np.append(sample,fftsample[0]);
            print np.size(sample);
            if np.size(samples) == 0:
                samples = [sample];
            else:
                samples = np.append(samples,[sample],0);

responses = np.array(responses,np.float32)
responses = responses.reshape((responses.size,1))
print "training complete"

path = "./trainingdata/";

np.savetxt(path +featurestype + "samples/"+  imgstring+"generalsamples.data",samples)
np.savetxt(path + featurestype +"responses/"+ imgstring+"generalresponses.data",responses)
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
