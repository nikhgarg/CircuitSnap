import cv2;
import numpy as np;

def getImageToSendToContour(im, isPhoto):
    resized = []
    if isPhoto:
        im = cv2.resize(im, dsize = (0,0), fx = .1, fy = .1, interpolation = cv2.INTER_CUBIC);
    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    if isPhoto:
        thresh = cv2.GaussianBlur(gray,(5,5),1)
    else:
        thresh = gray;
    thresh = cv2.adaptiveThreshold(thresh,255,adaptiveMethod = cv2.ADAPTIVE_THRESH_GAUSSIAN_C,thresholdType = cv2.THRESH_BINARY,blockSize = 11, C=2)
    return [thresh, gray]


