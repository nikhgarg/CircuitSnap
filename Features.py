import cv2;
import numpy as np;
from Classes import Mode;
from Classes import FeatureLabels;
import Classes;
from sklearn.decomposition import RandomizedPCA;
import Postprocess;
import Preprocess;

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
   # print cp.shape;
   # print cp;
   # print "transforming"
    tran = pca.fit(cp)
   # print tran
    recov  = pca.explained_variance_;
   # print recov.shape;
   # print recov;
    return recov;

def calculateFeatures(featureLabels, roismall):
    functions = {FeatureLabels.FFT : fftFeature, FeatureLabels.PIXEL: pixelFeature, FeatureLabels.SIFT : siftFeature, FeatureLabels.SURF: surfFeature, FeatureLabels.PCA : pcaFeature}
    features = []
    for label in featureLabels:
        features.extend(functions[label](roismall));
    return features;


def templateMatching(im,elements, isPhoto):
    templates = ['images/templates/resistorT4.PNG', 'images/templates/resistorT2.PNG', 'images/templates/resistorT2_0degree.PNG', 'images/templates/resistorT2_45degree.PNG', 'images/templates/resistorT2_135degree.PNG','images/templates/resistorT4_0degree.PNG'];
    unmatched_resistors = [];
    for elem in elements:
        if elem[4] == 'o':
            unmatched_resistors += [elem];

    matched_resistors = {}
    matched_resistor_key = {}
    for threshold in [1, .9, .8, .7, .6, .5]:#, .5, .4, .3]:
        for restt in range(2, 15):
            for t in templates:
                templ = cv2.imread(t,cv2.CV_LOAD_IMAGE_COLOR);
                res = 20 - restt;
                template = cv2.resize(templ, dsize = (0,0), fx = res/10., fy = res/10., interpolation = cv2.INTER_CUBIC);
                [template, g]= Preprocess.getImageToSendToContour(template, False);
                w, h = template.shape[::-1]

                res = cv2.matchTemplate(im,template,cv2.TM_CCOEFF_NORMED)

                loc = np.where( res >= threshold)
                pts = []
                for pt in zip(*loc[::-1]):
                    pts += [[pt[0], pt[1], w, h, 'r']];
                indicesToRemove_ii = []
                indicesToRemove_i = []
                for i in range(0, len(unmatched_resistors)):
                    ii = -1;
                    minDistance = 1000000;
                    for ifindmin in range(0,len(pts)): 
                        dist = Postprocess.distance_resistor(unmatched_resistors[i][0:5], pts[ifindmin]);
                        if dist < minDistance and (ifindmin not in indicesToRemove_ii) and dist < 20 and dist < matched_resistor_key.get(i, 10000)*(threshold*1.1) and dist>7:
                            ii = ifindmin;
                            minDistance = dist;
                    if ii == -1:
                        continue;
                    matchresistor = unmatched_resistors[i][:];
                    matchresistor[0] = pts[ii][0]; #take on location of the element in the circuit
                    matchresistor[1] = pts[ii][1];
                    matchresistor[2] = pts[ii][2];
                    matchresistor[3] = pts[ii][3];
                    indicesToRemove_ii += [ii];
                    indicesToRemove_i  += [i];
                    matched_resistors[i] = matchresistor;
                    matched_resistor_key[i] = dist;
                #newunmatched = []
                #for i in range(0, len(unmatched_resistors)):
                #    if i not in indicesToRemove_i:
                #        newunmatched += [unmatched_resistors[i]]
                #unmatched_resistors = newunmatched;

 #   for r in matched_resistors:
 #       print r
    print matched_resistors
    print unmatched_resistors
    for i in matched_resistors.keys():
        pt = matched_resistors[i];
        cv2.rectangle(im, (pt[0], pt[1]), (pt[0] + pt[2], pt[1] + pt[3]), (0,0,0), 2)
        matchresistor = unmatched_resistors[i];
        matchresistor[0] = pt[0]; #take on location of the element in the circuit
        matchresistor[1] = pt[1];
        matchresistor[2] = pt[2];
        matchresistor[3] = pt[3];
    cv2.imshow('resistors', im);
 #   cv2.imshow('temp', template);

#    key = cv2.waitKey(0)
    return elements;
                    #cv2.rectangle(im, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)