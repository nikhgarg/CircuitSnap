import cv2;
import numpy as np;
from Classes import Mode;
from Classes import FeatureLabels;

def fftFeature(roismall):
    SIZESMALLSAVED = len(roismall)
    regionfft = abs(np.fft.fft2(roismall))
    fftarray = regionfft.reshape((1, SIZESMALLSAVED*SIZESMALLSAVED))
    return fftarray;
def surfFeature(roismall):
    return []
def pixelFeature(roismall):
    return roismall;
def siftFeature(roismall):
    return []

def calculateFeatures(featureLabels, roismall):
    functions = {FeatureLabels.FFT : fftFeature, FeatureLabels.PIXEL: pixelFeature, FeatureLabels.SIFT : siftFeature, FeatureLabels.SURF: surfFeature}
    features = []
    for label in featureLabels:
        features.extend(functions[label](roismall));
    return features;
