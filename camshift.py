import cv2
import numpy as np

drawing = False
camshift = False


def mouse_action(event, x, y, flags, param):
    global drawing, ix, iy, fx, fy, Hi, Si, Vi, Hf, Sf, Vf, track_window, hsv, camshift, roi_hist, term_crit
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        fx, fy = x, y

    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        fx, fy = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        track_window = (min(ix, x), min(iy, y), min(ix, x)+abs(ix-x) + 1, min(iy, y)+abs(iy-y) + 1)
        roi = frame[min(iy, y):min(iy, y)+abs(iy-y) + 1, min(ix, x):min(ix, x)+abs(ix-x) + 1]

        hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        h, s, v = cv2.split(hsv_roi)
        Hi, Hf = np.amin(h), np.amax(h)
        Si, Sf = np.amin(s), np.amax(s)
        Vi, Vf = np.amin(v), np.amax(v)
        HSVi = np.array([Hi, Si, Vi])
        HSVf = np.array([Hf, Sf, Vf])
        mask = cv2.inRange(hsv_roi, HSVi, HSVf)
        roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])
        cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)
        term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

        camshift = True

    if event == cv2.EVENT_LBUTTONUP and (ix, iy) == (x, y):
        Hi, Si, Vi = 0, 0, 0
        Hf, Sf, Vf = 179, 255, 255
        camshift = False

cv2.namedWindow('Preview')
cv2.setMouseCallback('Preview', mouse_action)
cap = cv2.VideoCapture(0)
# set resolution
cap.set(3, 640)
cap.set(4, 480)

while True:
    ret, frame = cap.read()

    if camshift:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)
        ret, track_window = cv2.CamShift(dst, track_window, term_crit)
        pts = cv2.boxPoints(ret)
        pts = np.int0(pts)
        cv2.polylines(frame, [pts], True, 255, 2)

    if drawing:
        cv2.rectangle(frame, (ix, iy), (fx, fy), (255, 0, 0), 2)

    cv2.imshow('Preview', frame)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()
