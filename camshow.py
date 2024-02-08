import sys
import cv2

# 맥북에어15의 경우, 내장카메라는 1번 장치
cam = cv2.VideoCapture(1)

ret = cam.isOpened()
if not ret:
    print('Camera open failed !')
    sys.exit()

frm_width  = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
frm_height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)

print('Camera opened !: ', 'width = ', frm_width, 'height = ', frm_height)

while True:
    ret, frame = cam.read()
    if not ret:
        break

    cv2.imshow('Camera', frame)

    if cv2.waitKey(1) == 27:    #ESC key
        break

cam.release()

cv2.destroyAllWindows()