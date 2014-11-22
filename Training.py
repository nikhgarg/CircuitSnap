import cv2;
import numpy as np;

def setUpTraining(SamplesSize):
    samples =  np.empty((0,SamplesSize))
    responses = []
    return [responses, samples];

def getResponse():
    key = cv2.waitKey(0);
    if key == 27:  # (escape to quit)
        sys.exit()
    else:
        response = (ord(chr(key)))
    return response