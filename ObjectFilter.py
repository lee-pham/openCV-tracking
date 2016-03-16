import cv2
import numpy as np
import os

os.system("sudo modprobe bcm2835-v4l2 #")  # required for the camera module to be recognized as a USB camera
cap = cv2.VideoCapture(0)

while True:

    # Take each frame
    _, img = cap.read()
    frame = cv2.flip(img, 0)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of HSV values
    HSV0 = np.array([0,0,0])
    HSV1 = np.array([179,255,255])

    # Threshold the HSV image to get only HSV range
    mask = cv2.inRange(hsv, HSV0, HSV1)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('Raw', frame)
    cv2.imshow('Mask', mask)
    cv2.imshow('Preview', res)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
