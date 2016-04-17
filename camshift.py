import cv2
import numpy as np
ix, iy = 0, 0
fx, fy = 0, 0
Hi, Si, Vi = 0, 0, 0
Hf, Sf, Vf = 179, 255, 255
HSVi = np.array([Hi, Si, Vi])
HSVf = np.array([Hf, Sf, Vf])

def mouse_action(event, x, y, flags, param):
    global drawing, ix, iy, fx, fy, Hi, Si, Vi, Hf, Sf, Vf
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        fx, fy = x, y

    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        fx, fy = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        roi = hsv[min(iy, y):min(iy, y)+abs(iy-y) + 1, min(ix,x):min(ix, x)+abs(ix-x) + 1]
        h, s, v = cv2.split(roi)
        Hi, Hf = np.amin(h), np.amax(h)
        Si, Sf = np.amin(s), np.amax(s)
        Vi, Vf = np.amin(v), np.amax(v)

    if event == cv2.EVENT_LBUTTONUP and (ix, iy) == (x, y):
        Hi, Si, Vi = 0, 0, 0
        Hf, Sf, Vf = 179, 255, 255

cap = cv2.VideoCapture(0)
# set resolution
cap.set(3, 640)
cap.set(4, 480)

ret, frame = cap.read()

r, h, c, w = 250, 90, 400, 125
track_window = (c, r, w, h)

roi = frame[r:r+h, c:c+w]
hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_roi, HSVi, HSVf)
roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])
cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)
term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

while True:
    ret, frame = cap.read()

    if ret:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)

        ret, track_window = cv2.CamShift(dst, track_window, term_crit)

        pts = cv2.boxPoints(ret)
        pts = np.int0(pts)
        img2 = cv2.polylines(frame, [pts], True, 255, 2)
        cv2.imshow('img2', img2)


        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

cv2.destroyAllWindows()
cap.release()
