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
import CircuitSolver;
import os;
import Classification;
import Postprocess;
import math;

SIZESMALLSAVED = 20;

FEATURESSIZE = {FeatureLabels.PIXEL : pow(SIZESMALLSAVED, 2), FeatureLabels.FFT : pow(SIZESMALLSAVED, 2), FeatureLabels.PCA : pow(SIZESMALLSAVED, 1)}; 
path = "./trainingdata/";
MODELTYPES = ["svm", "knn", "nn"];
# paramaters
mode = Mode.TESTING; #TESTING
featureLabels = [FeatureLabels.PIXEL, FeatureLabels.FFT, FeatureLabels.PCA];
featuresdirectory = "";
modeltype = MODELTYPES[1];
   
isPhoto = True;
imgname = "photo3"

#########################
for i in featureLabels:
    featuresdirectory += str(i);
featuresdirectory += "thresh/"

im = ReadImage.readImage(imgname, isPhoto);
cv2.imshow('origorig', im);
imcopy = im.copy();
out = np.zeros(im.shape,np.uint8)

outputcircuit = im.copy();

[toContour, gray] = Preprocess.getImageToSendToContour(im, isPhoto);
cv2.imshow('tocontour', toContour);
#key = cv2.waitKey(0)

print toContour;
contours,hierarchy = cv2.findContours(toContour,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE) # RETR_LIST

SamplesSize = sum([FEATURESSIZE[feat] for feat in featureLabels])
if (mode is Mode.TRAINING):
    [responses, samples] = Training.setUpTraining(SamplesSize);
else:
    [responses, samples, model, responses_order] = Testing.setUpTesting(SamplesSize, featuresdirectory, modeltype);

all_components = []
found_elements = [];

for cnt in contours:
    if cv2.contourArea(cnt)>30 :
        [x,y,w,h] = cv2.boundingRect(cnt)
        imdraw = imcopy.copy();
        cv2.rectangle(imdraw,(x,y),(x+w,y+h),(0,0,255),2)
        cv2.rectangle(im,(x,y),(x+w,y+h),(0,0,255),2)
        roi = toContour[y:y+h,x:x+w]
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
            all_components += [[x, y, w, h, chr(int(result))]];    
            #print result
            string = str(chr(int(result)))
            cv2.putText(out,string,(x,y+h),0,1,(0,255,0))

if mode is Mode.TESTING:
    cv2.imshow('contours', im);
    cv2.imshow('recognized objects',out);
    found_elements = Postprocess.extractElements(all_components);
    found_elements = Features.templateMatching(gray, found_elements, isPhoto);
    print all_components;
    print found_elements;
 #   key = cv2.waitKey(0)
    meshcurrents = CircuitSolver.solveCircuit(found_elements)
    for i in range(0,len(meshcurrents[0])):
        print "this current",meshcurrents[0][i],"is for the loop located at",meshcurrents[1][i]
        x = int(meshcurrents[1][i][0] + meshcurrents[1][i][2]*0.33)
        y = int(meshcurrents[1][i][1] + meshcurrents[1][i][3]*6/7)
        cv2.putText(outputcircuit,str(round(meshcurrents[0][i],2)) + "A",(x,y),0,0.5,(255,0,0))
    for element in meshcurrents[2]:
        cv2.putText(outputcircuit,str(round(element[0],2)) + "V",(abs(element[1][0] - 23),element[1][1]+5),0,0.35,(0,0,255))
    outputcircuit = cv2.resize(outputcircuit, dsize = (0,0), fx = 2, fy = 2, interpolation = cv2.INTER_CUBIC);
    cv2.imshow('solved circuit', outputcircuit);
    print found_elements;
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