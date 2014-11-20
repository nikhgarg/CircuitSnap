import cv2;
import ReadImage;
import Preprocess;
import numpy as np;

# constants
class Mode:
    TRAINING = 0;
    TESTING = 1;

class Feature:
    PIXELS = 0;
    FFT = 1;
    SIFT = 2;
    SURF = 3;
SIZESMALLSAVED = 20;

FEATURESSIZE = {Feature.PIXELS : pow(SIZESMALLSAVED, 2), Feature.FFT : pow(SIZESMALLSAVED, 2)}; 
# paramaters

isPhoto = True;
mode = Mode.TRAINING; #TESTING
features = [Feature.PIXELS, Feature.FFT];

imgname = "photo1cropped"
#########################

im = ReadImage.readImage(imgname, isPhoto);
toContour = Preprocess.getImageToSendToContour(im, isPhoto);
contours,hierarchy = cv2.findContours(toContour,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

SamplesSize = sum([FEATURESSIZE[feat] for feat in features])

if mode is Mode.TRAINING:
    samples =  np.empty((0,SamplesSize))
    responses = []
else:
    print 'TODO'


cv2.imshow('test',toContour);
key = cv2.waitKey(0)
