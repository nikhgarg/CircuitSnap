import cv2;

def readImage(filename, isPhoto):
    path = "images/"
    if isPhoto:
        return readPhoto(path, filename)
    else:
        return readScreenShot(path, filename)

def readScreenShot(path, filename):
    imgtype = ".PNG"
    im = cv2.imread(path + filename + imgtype,cv2.CV_LOAD_IMAGE_COLOR)
    return im;

def readPhoto(path, filename):
    imgtype = ".jpg"
    im = cv2.imread(path + filename + imgtype,cv2.CV_LOAD_IMAGE_COLOR)
    im = cv2.resize(im, dsize = (0,0), fx = .1, fy = .1, interpolation = cv2.INTER_CUBIC);
    return im;

