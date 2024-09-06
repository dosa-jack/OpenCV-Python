import cv2
import numpy as np

img = cv2.imread('./Data/lena.jpg')
cv2.imshow('original image', img)

# create a new image array and draw lines, circles, rectangles, etc. on it
overlay = np.zeros((700, 700, 3), dtype=np.uint8)

overlay = cv2.line(overlay, (100, 100), (600, 600), (255, 0, 0), 5)
overlay = cv2.circle(overlay, (150, 150), 100, (0, 255, 0), 4)
overlay = cv2.rectangle(overlay, (300, 100), (500, 500), (0, 0, 255), 3)
overlay = cv2.ellipse(overlay, (500, 300), (300, 200), 0, 90, 250, (255, 255, 0), 2)

obj1 = np.array([[300, 500], [500, 500], [400, 600], [200, 600]])
overlay = cv2.polylines(overlay, [obj1], True, (0, 255, 255), 1)

obj2 = np.array([[600, 500], [690, 500], [650, 200]])
overlay = cv2.fillPoly(overlay, [obj2], (255, 255, 255), 1)

cv2.imshow('overlay image', overlay)

cv2.waitKey()