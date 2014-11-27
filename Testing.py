import cv2;
import numpy as np;
import os;

def setUpTesting(SamplesSize, featurestype, model):
    dirtocheck = "./trainingdata/"+featurestype;
    responsespath = "responses";
    samplespath = "samples";
    responses = None;
    samples = None;
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
            if samples is None:
                samples = newSamples;
            else:
                samples = np.append(samples, [newSamples]);
    #samples = samples[0];
    samples = samples.reshape(np.size(responses),np.size(samples)/np.size(responses)); 
    model.train(samples,responses)
    return [responses, samples]

