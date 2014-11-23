import cv2;
import numpy as np;


def createModel(modeltype, ninputs, noutputs):
    if modeltype == "knn":
        return cv2.KNearest();
    elif modeltype == "svm":
        return cv2.SVM();
    elif modeltype == "nn":
        layers = np.array([ninputs, 300, noutputs]);
        print ninputs
        print noutputs
        return cv2.ANN_MLP(layers);


def trainModel(modeltype, model, responses, samples, responses_order):
    if modeltype == "knn":
        model.train(samples, responses);
    elif modeltype == "svm":
        model.train(samples, responses);
    elif modeltype == "nn":
        trainNN(model, responses, samples, responses_order);

def predict(modeltype, model, sample):
    if modeltype == "knn":
        retval, results, neigh_resp, dists = model.find_nearest(sample, k = 1)
        return results[0][0];
    elif modeltype == "svm":
        result = model.predict(sample);
        return result
    elif modeltype == "nn":
        predictions = np.empty([16])
        model.predict(sample, predictions)
        return predictions[0];

def trainNN(model, responses, samples, responses_order): # code from # http://www.swarthmore.edu/NatSci/mzucker1/e27/simple_nnet_example.py
    # Some parameters for learning.  Step size is the gradient step size
    # for backpropogation.
    step_size = 0.01

    # Momentum can be ignored for this example.
    momentum = 0.5

    # Max steps of training
    nsteps = 10000

    # Error threshold for halting training
    max_err = 0.0001

    # When to stop: whichever comes first, count or error
    condition = cv2.TERM_CRITERIA_COUNT | cv2.TERM_CRITERIA_EPS

    # Tuple of termination criteria: first condition, then # steps, then
    # error tolerance second and third things are ignored if not implied
    # by condition
    criteria = (condition, nsteps, max_err)

    # params is a dictionary with relevant things for NNet training.
    params = dict( term_crit = criteria, 
                   train_method = cv2.ANN_MLP_TRAIN_PARAMS_BACKPROP, 
                   bp_dw_scale = step_size, 
                   bp_moment_scale = momentum )
    targets = np.zeros((len(samples), len(responses_order)));
    print np.shape(targets);
    for i in range(0, len(samples)):
        ind = responses_order.index(responses[i]);
        targets[i][ind] = 1;
    # Train our network
    num_iter = model.train(samples, targets,
                          None, params=params)

