import cv2;
import ReadImage;
import Preprocess;

# constants
class Mode:
    TRAINING = 0;
    TESTING = 1;

class Feature:
    PIXELS = 0;
    FFT = 1;
    SIFT = 2;
    SURF = 3;

# paramaters

isPhoto = True;
mode = Mode.TRAINING; #TESTING
features = [Feature.PIXELS, Feature.FFT];

imgname = "photo1cropped"
#########################

im = ReadImage.readImage(imgname, isPhoto);
thresh = Preprocess.getImageToSendToContour(im, isPhoto);

cv2.imshow('test',thresh);
key = cv2.waitKey(0)
