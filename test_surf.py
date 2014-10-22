import numpy as np
import cv2
from matplotlib import pyplot as plt

#http://docs.opencv.org/trunk/doc/py_tutorials/py_feature2d/py_surf_intro/py_surf_intro.html#surf

img = cv2.imread('images/1.PNG')
surf = cv2.SURF(5000)
kp, des = surf.detectAndCompute(img, None)
print len(kp)
img2 = cv2.drawKeypoints(img,kp,None,(255,0,0),4)
plt.imshow(img2),plt.show()