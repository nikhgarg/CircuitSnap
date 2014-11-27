import cv2;
import numpy as np;
from Classes import Mode;
from Classes import FeatureLabels;
import Classes;
from sklearn.decomposition import RandomizedPCA;

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
def pcaFeature(roismall):
    pca = RandomizedPCA();
    cp = roismall.copy();
    print cp.shape;
    print cp;
    print "transforming"
    tran = pca.fit(cp)
    print tran
    recov  = pca.explained_variance_;
    print recov.shape;
    print recov;
    return recov;

def calculateFeatures(featureLabels, roismall):
    functions = {FeatureLabels.FFT : fftFeature, FeatureLabels.PIXEL: pixelFeature, FeatureLabels.SIFT : siftFeature, FeatureLabels.SURF: surfFeature, FeatureLabels.PCA : pcaFeature}
    features = []
    for label in featureLabels:
        features.extend(functions[label](roismall));
    return features;
