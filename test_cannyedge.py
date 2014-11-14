# http://docs.opencv.org/doc/tutorials/imgproc/imgtrans/canny_detector/canny_detector.html
import cv2
import numpy as np
from matplotlib import pyplot as plt
import math
import cv

img_rgb = cv2.imread('images/3.PNG',cv2.CV_LOAD_IMAGE_COLOR)
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
(thresh, im_gray) = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
edges = cv2.Canny(im_gray, 80, 120);
x = len(img_gray)
y = (len(img_gray[0]))
output = np.ones((len(img_gray), len(img_gray[0]))) * 255;
lines = cv2.HoughLinesP(edges, 1, math.pi/2, 2, None, 15, 1);
for line in lines[0]:
    pt1 = (line[0],line[1])
    pt2 = (line[2],line[3])
    cv2.line(output, pt1, pt2, (0,0,255), 3)
circles = cv2.HoughCircles(edges, cv.CV_HOUGH_GRADIENT, 1, 10, np.array([]), 100, 30, 1, 30)
a, b, c = circles.shape
for i in range(b):
    cv2.circle(output, (circles[0][i][0], circles[0][i][1]), circles[0][i][2], (0, 0, 255), 3, 1)
    cv2.circle(output, (circles[0][i][0], circles[0][i][1]), 2, (0, 255, 0), 3, 3) # draw center of circle
plt.imshow(output), plt.show()