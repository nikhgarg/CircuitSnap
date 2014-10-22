import cv2
import numpy as np
from matplotlib import pyplot as plt
#http://docs.opencv.org/trunk/doc/py_tutorials/py_imgproc/py_template_matching/py_template_matching.html#py-template-matching

#works, but only if the template size is same as size of object in the query image.
img_rgb = cv2.imread('images/3.PNG',cv2.CV_LOAD_IMAGE_COLOR)
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
template = cv2.imread('images/VoltageSourceTemplate.PNG',0)
w, h = template.shape[::-1]

res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
threshold = 0.8
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

plt.imshow(img_rgb),plt.show()
cv2.imwrite('res.png',img_rgb)
