import cv2
import numpy as np

drawing = False  # initialize drawing status
# initialize variables
ix, iy = 0, 0
fx, fy = 0, 0
Hi, Si, Vi = 0, 0, 0
Hf, Sf, Vf = 179, 255, 255


def mouse_action(event, x, y, flags, param):
    global drawing, ix, iy, fx, fy, ROI, Hi, Si, Vi, Hf, Sf, Vf
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        print(ix, iy)
        fx, fy = x, y

    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        fx, fy = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        print(ix, iy, x, y)
        print(hsv)
        ROI = hsv[min(iy, y):min(iy, y)+abs(iy-y) +1, min(ix,x):min(ix,x)+abs(ix-x) +1]
        h, s, v = cv2.split(ROI)
        Hi, Hf = np.amin(h), np.amax(h)
        Si, Sf = np.amin(s), np.amax(s)
        Vi, Vf = np.amin(v), np.amax(v)
        print(Hi, Hf, Si, Sf, Vi, Vf)
        print('release')


cap = cv2.VideoCapture(0)
# set resolution
cap.set(3, 640)
cap.set(4, 480)

cv2.namedWindow('Preview')
cv2.setMouseCallback('Preview', mouse_action)

while True:
    _, img = cap.read()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # convert to HSV

    HSVi = np.array([Hi, Si, Vi])
    HSVf = np.array([Hf, Sf, Vf])
    mask = cv2.inRange(hsv, HSVi, HSVf)

    output = cv2.bitwise_and(img, img, mask=mask)

    # if drawing, draw blue rectangle
    if drawing:
        cv2.rectangle(output, (ix, iy), (fx, fy), (255, 0, 0), 2)

    cv2.imshow('Preview', output)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
