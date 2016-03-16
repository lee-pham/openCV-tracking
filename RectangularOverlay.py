import cv2
import numpy as np
import os

os.system("sudo modprobe bcm2835-v4l2 #")
cap = cv2.VideoCapture(0)

while True:

    # Take each frame
    _, img = cap.read()
    frame = cv2.flip(img, 0)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define HSV range
    HSV0 = np.array([0,0,0])
    HSV1 = np.array([179,255,255])

    # Threshold the HSV image to get only range colors
    mask = cv2.inRange(hsv, HSV0, HSV1)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask=mask)

    _, contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    max_area = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            best_count = contour

    x, y, w, h = cv2.boundingRect(best_count)
    rect = cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)

    cv2.imshow('Preview', frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
