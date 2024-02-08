import cv2 as cv

#맥에서는 폴더 구분자가 /, 윈도우에서는 \
img = cv.imread('./data/lenna.png', cv.IMREAD_COLOR)

cv.imshow('image', img)

cv.waitKey()