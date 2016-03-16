import cv2
import numpy as np
import os

os.system("sudo modprobe bcm2835-v4l2 #")  # required for the camera module to be recognized as a USB camera
cap = cv2.VideoCapture(0)

def nothing(x):
    pass

cv2.namedWindow('Preview')

# create Sliders for color change
cv2.createTrackbar('Hmin', 'Preview', 0, 179, nothing)
cv2.createTrackbar('Smin', 'Preview', 0, 255, nothing)
cv2.createTrackbar('Vmin', 'Preview', 0, 255, nothing)
cv2.createTrackbar('Hmax', 'Preview', 0, 179, nothing)
cv2.createTrackbar('Smax', 'Preview', 0, 255, nothing)
cv2.createTrackbar('Vmax', 'Preview', 0, 255, nothing)

# create switch for ON/OFF functionality
switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, 'Preview', 0, 1, nothing)

while True:
    _, img = cap.read()

    frame = cv2.flip(img, 0)  # veritcally or horizontally flip feed (1,0,-1)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # convert to HSV

    # get current positions of four Sliders
    H0 = cv2.getTrackbarPos('Hmin', 'Preview')
    S0 = cv2.getTrackbarPos('Smin', 'Preview')
    V0 = cv2.getTrackbarPos('Vmin', 'Preview')
    H1 = cv2.getTrackbarPos('Hmax', 'Preview')
    S1 = cv2.getTrackbarPos('Smax', 'Preview')
    V1 = cv2.getTrackbarPos('Vmax', 'Preview')
    s = cv2.getTrackbarPos(switch, 'Preview')

    HSV0 = np.array([H0, S0, V0])
    HSV1 = np.array([H1, S1, V1])

    mask = cv2.inRange(hsv, HSV0, HSV1)

    res = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('Preview', res)
    cv2.imshow('Mask', mask)
    cv2.imshow('Raw', frame)

    if s == 0:
        img[:] = 0
    else:
        img[:] = [H0, S0, V0]
        
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
