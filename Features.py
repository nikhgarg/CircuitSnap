import cv2;
import numpy as np;
from Classes import Mode;
from Classes import FeatureLabels;
import Classes;

def fftFeature(roismall):
    SIZESMALLSAVED = len(roismall)
    regionfft = abs(np.fft.fft2(roismall))
    return [item for sublist in regionfft for item in sublist];

def surfFeature(roismall):
    return []
def pixelFeature(roismall):
    return [item for sublist in roismall for item in sublist];
def siftFeature(roismall):
    return []

def calculateFeatures(featureLabels, roismall):
    functions = {FeatureLabels.FFT : fftFeature, FeatureLabels.PIXEL: pixelFeature, FeatureLabels.SIFT : siftFeature, FeatureLabels.SURF: surfFeature}
    features = []
    for label in featureLabels:
        features.extend(functions[label](roismall));
    return features;
