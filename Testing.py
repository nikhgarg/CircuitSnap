import cv2;
import numpy as np;
import os;
import Classification;

def setUpTesting(SamplesSize, featurestype, modeltype):
    dirtocheck = "./trainingdata/"+featurestype;
    responsespath = "responses";
    samplespath = "samples";
    responses = None;
    samples = [];
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
            print newSamples
            samples = np.append(samples, [newSamples]);
            print samples
    ninputs = len(samples)/len(responses);
    samples = np.array(samples.reshape(np.size(responses),np.size(samples)/np.size(responses)), np.float32); 
    print samples
    noutputs = len(set(responses));
    print ninputs
    print noutputs
    model = Classification.createModel(modeltype, ninputs, noutputs);
    responses_order = list(set(responses));
    responses_order.sort();
    Classification.trainModel(modeltype, model, responses, samples, responses_order);
    return [responses, samples, model, responses_order]

