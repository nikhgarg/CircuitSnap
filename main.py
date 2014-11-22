import cv2;
import ReadImage;
import Preprocess;
import numpy as np;
import Training;
import Testing;
import Features;
import Classes;
from Classes import Mode;
from Classes import FeatureLabels;
import os;
import Classification;

SIZESMALLSAVED = 20;

FEATURESSIZE = {FeatureLabels.PIXEL : pow(SIZESMALLSAVED, 2), FeatureLabels.FFT : pow(SIZESMALLSAVED, 2)}; 
path = "./trainingdata/";
MODELTYPES = ["svm", "knn"];
# paramaters
isPhoto = True;
mode = Mode.TESTING; #TESTING
featureLabels = [FeatureLabels.PIXEL, FeatureLabels.FFT];
featuresdirectory = "";
modeltype = MODELTYPES[0];
    
imgname = "photo3cropped"
model = Classification.createModel(modeltype);
#########################
for i in featureLabels:
    featuresdirectory += str(i);
featuresdirectory += "/"

im = ReadImage.readImage(imgname, isPhoto);
imcopy = im.copy();
out = np.zeros(im.shape,np.uint8)

[toContour, gray] = Preprocess.getImageToSendToContour(im, isPhoto);
contours,hierarchy = cv2.findContours(toContour,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

SamplesSize = sum([FEATURESSIZE[feat] for feat in featureLabels])
if (mode is Mode.TRAINING):
    [responses, samples] = Training.setUpTraining(SamplesSize);
else:
    [responses, samples] = Testing.setUpTesting(SamplesSize, featuresdirectory, modeltype, model);

for cnt in contours:
    if cv2.contourArea(cnt)>15 :
        [x,y,w,h] = cv2.boundingRect(cnt)
        imdraw = imcopy.copy();
        cv2.rectangle(imdraw,(x,y),(x+w,y+h),(0,0,255),2)
        cv2.rectangle(im,(x,y),(x+w,y+h),(0,0,255),2)
        roi = gray[y:y+h,x:x+w]
        roismall = cv2.resize(roi,(SIZESMALLSAVED,SIZESMALLSAVED))
        roismallarray = np.float32(roismall.copy().reshape((1,SIZESMALLSAVED*SIZESMALLSAVED)));
        current_sample = Features.calculateFeatures(featureLabels, roismall);
        if mode is Mode.TRAINING:
            cv2.imshow('norm', imdraw);
            current_response = Training.getResponse();
            responses.append(current_response);
            if np.size(samples) == 0:
                samples = [current_sample];
            else:
                samples = np.append(samples,[current_sample],0);
        else:
            result = Classification.predict(modeltype, model, np.array([current_sample], np.float32));    
            print result
            string = str(chr(int(result)))
            cv2.putText(out,string,(x,y+h),0,1,(0,255,0))


if mode is Mode.TESTING:
    cv2.imshow('input', im);
    cv2.imshow('output',out);
key = cv2.waitKey(0)

if mode is Mode.TRAINING:
    responses = np.array(responses,np.float32)
    responses = responses.reshape((responses.size,1))
    print "training complete"
    dire = path + featuresdirectory;
    if not os.path.exists(dire):
        os.makedirs(dire)
    if not os.path.exists(dire + "samples/"):
        os.makedirs(dire + "samples/")
    if not os.path.exists(dire + "responses/"):
        os.makedirs(dire + "responses/")
    print len(samples)
    np.savetxt(path +featuresdirectory + "samples/"+  imgname+"generalsamples.data",samples)
    np.savetxt(path + featuresdirectory +"responses/"+ imgname+"generalresponses.data",responses)



        #string = str(chr((results[0][0])))
        #cv2.putText(out,string,(x,y+h),0,1,(0,255,0))

        ###########other stuff --- features
        #kp, des = surf.detectAndCompute(roi,None)
        #img=cv2.drawKeypoints(roi,kp,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)