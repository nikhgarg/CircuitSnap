import cv2
import numpy as np

img = cv2.imread('images/hard.PNG')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)
circles = cv2.HoughCircles(edges, cv2.cv.CV_HOUGH_GRADIENT, 2, 10, np.array([]), 20, 60, 0)[0]
lines = cv2.HoughLines(edges,1,np.pi/180,75)
for rho,theta in lines[0]:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))
    # cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

for c in circles[:3]:
 # green for circles (only draw the 3 strongest)
 cv2.circle(img, (c[0],c[1]), c[2], (0,255,0), 2)

# print lines
for line in lines[0]:
	# print line
	print line[1] - line[0]
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()