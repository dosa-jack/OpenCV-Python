# this code encodes the frame data into a new format and saves it to disk as a file.
import cv2

# read a bitmap image file from disk
orig_img = cv2.imread('./Data/jungfrau.bmp')
cv2.imshow('original image', orig_img)

# encode image data to jpeg format
ret, enc_frm = cv2.imencode('.jpg', orig_img, [cv2.IMWRITE_JPEG_QUALITY, 100])

enc_file = open('enc_frm.jpg', 'wb')
enc_file.write(enc_frm)
enc_file.close()

cv2.waitKey()