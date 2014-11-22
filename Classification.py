import cv2;

def createModel(modeltype):
    if modeltype == "knn":
        return cv2.KNearest();
    elif modeltype == "svm":
        return cv2.SVM();

def trainModel(modeltype, model, responses, samples):
    if modeltype == "knn":
        model.train(samples, responses);
    elif modeltype == "svm":
        model.train(samples, responses);

def predict(modeltype, model, sample):
    if modeltype == "knn":
        retval, results, neigh_resp, dists = model.find_nearest(sample, k = 1)
        return results[0][0];
    elif modeltype == "svm":
        result = model.predict(sample);
        return result


#example for neural nets here:
http://www.swarthmore.edu/NatSci/mzucker1/e27/simple_nnet_example.py