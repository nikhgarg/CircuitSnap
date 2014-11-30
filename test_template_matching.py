import cv2
import numpy as np
from matplotlib import pyplot as plt
import Preprocess;
#http://docs.opencv.org/trunk/doc/py_tutorials/py_imgproc/py_template_matching/py_template_matching.html#py-template-matching

#works, but only if the template size is same as size of object in the query image.
img_rgb = cv2.imread('images/photo3cropped.jpg',cv2.CV_LOAD_IMAGE_COLOR)
img_rgb = cv2.resize(img_rgb, dsize = (0,0), fx = .1, fy = .1, interpolation = cv2.INTER_CUBIC);

[img_gray, gray] = Preprocess.getImageToSendToContour(img_rgb, True);

#img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
templates = ['images/resistorT4.PNG', 'images/resistorT2.PNG', 'images/resistorT2_0degree.PNG', 'images/resistorT4_0degree.PNG'];
print img_gray;
for t in templates:
    templ = cv2.imread(t,cv2.CV_LOAD_IMAGE_COLOR);
    for res in range(6, 15):
        template = cv2.resize(templ, dsize = (0,0), fx = res/10., fy = res/10., interpolation = cv2.INTER_CUBIC);

        [template, g]= Preprocess.getImageToSendToContour(template, False);
        w, h = template.shape[::-1]

        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
        threshold = 0.4
        loc = np.where( res >= threshold)

        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_gray, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

cv2.imshow('template', template)
cv2.imshow('gray', img_gray);
key = cv2.waitKey(0)

plt.imshow(img_rgb),plt.show()
cv2.imwrite('res.png',img_rgb)
