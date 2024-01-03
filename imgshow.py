import cv2 as cv

img = cv.imread('.\data\cup.jpg', cv.IMREAD_COLOR)

cv.imshow('image', img)

cv.waitKey()