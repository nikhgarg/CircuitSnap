import numpy as np
import cv2
from matplotlib import pyplot as plt
#http://docs.opencv.org/trunk/doc/py_tutorials/py_feature2d/py_shi_tomasi/py_shi_tomasi.html#shi-tomasi
#does not work as well as the other one. 
img = cv2.imread('images/hard.PNG')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

corners = cv2.goodFeaturesToTrack(gray,50,0.01,10)
corners = np.int0(corners)
print corners

for i in corners:
    x,y = i.ravel()
    cv2.circle(img,(x,y),3,255,-1)

plt.imshow(img),plt.show()