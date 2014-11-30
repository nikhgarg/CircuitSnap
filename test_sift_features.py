import numpy as np
import cv2
from matplotlib import pyplot as plt

#http://docs.opencv.org/trunk/doc/py_tutorials/py_feature2d/py_matcher/py_matcher.html#matcher
img1 = cv2.imread('images/resistorT2.PNG',0)          # queryImage
img2 = cv2.imread('images/1.PNG',0) # trainImage

MIN_MATCH_COUNT = 10

# Initiate SIFT detector
sift = cv2.SIFT()

# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)

FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 1000)

flann = cv2.FlannBasedMatcher(index_params, search_params)

matches = flann.knnMatch(des1,des2,k=10)

# store all the good matches as per Lowe's ratio test.
#for m,n in matches:
#    if m.distance < 0.7*n.distance:
#        good.append(m)

## Initiate SIFT detector
#sift = cv2.SIFT()

## find the keypoints and descriptors with SIFT
#kp1, des1 = sift.detectAndCompute(img1,None)
#kp2, des2 = sift.detectAndCompute(img2,None)

## BFMatcher with default params
#bf = cv2.BFMatcher()
#matches = bf.knnMatch(des1,des2, k=2)

## Apply ratio test
#good = []
#for m,n in matches:
#    if m.distance < 0.75*n.distance:
#        good.append([m])

#print matches
#print "--------------------"
#print good

for index in range(0, len(matches[0])):
    good = [m[index] for m in matches]
    if len(good)>MIN_MATCH_COUNT:
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        matchesMask = mask.ravel().tolist()

        h,w = img1.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv2.perspectiveTransform(pts,M)
        for x in dst:
            print x
        xs = [x[0][0] for x in dst]
        ys = [x[0][1] for x in dst]
        minx = min(xs)
        maxx = max(xs)
        miny = min(ys)
        maxy = max(ys)
        cv2.rectangle(img2, (minx, miny), (maxx, maxy), 0);
        #cv2.polylines(img2,[np.int32(dst)],True,0)

    else:
        print "Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT)
        matchesMask = None

print img2

cv2.imshow('template', img1);
cv2.imshow('circuit', img2);
key = cv2.waitKey(0)

# cv2.drawMatchesKnn expects list of lists as matches.
#img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,flags=2)

#plt.imshow(img3),plt.show()