import cv2
import numpy as np

drawing = False
camshift = False
lower = np.array([0, 60, 30], dtype=np.uint8)
upper = np.array([179, 255, 255], dtype=np.uint8)


def mouse_action(event, x, y, flags, param):
    global ix, iy, fx, fy, track_window, drawing, camshift, term_crit, roi_hist, img
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        camshift = False
        ix, iy = x, y
        fx, fy = x, y

    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        fx, fy = x, y

        track_window = (min(ix, x), min(iy, y), min(ix, x) + abs(ix - x), min(iy, y) + abs(iy - y))
        roi = frame[min(iy, y):min(iy, y) + abs(iy - y), min(ix, x):min(ix, x) + abs(ix - x)]
        hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_roi, lower, upper)
        roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])
        cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)
        roi_hist = roi_hist.reshape(-1)
        bin_count = roi_hist.shape[0]
        bin_w = 24
        img = np.zeros((256, bin_count * bin_w, 3), np.uint8)
        for i in xrange(bin_count):
            h = int(roi_hist[i])
            cv2.rectangle(img, (i*bin_w+2, 255), ((i+1)*bin_w-2, 255-h), (int(180.0*i/bin_count), 255, 255), -1)
        img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
        cv2.imshow('hist', img)

    elif event == cv2.EVENT_LBUTTONUP and (ix, iy) == (x, y):
        camshift = False
        drawing = False

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        camshift = True

        track_window = (min(ix, x), min(iy, y), min(ix, x)+abs(ix-x), min(iy, y)+abs(iy-y))
        roi = frame[min(iy, y):min(iy, y) + abs(iy-y), min(ix, x):min(ix, x) + abs(ix-x)]
        hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_roi, lower, upper)
        roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])
        cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)
        term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

cv2.namedWindow('hist')
cv2.namedWindow('Preview')
cv2.setMouseCallback('Preview', mouse_action)
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

while True:
    ret, frame = cap.read()

    if camshift:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)
        ret, track_window = cv2.CamShift(dst, track_window, term_crit)
        box = cv2.boxPoints(ret)
        box = np.int0(box)
        cv2.polylines(frame, [box], True, 255, 2)

    elif drawing:
        cv2.rectangle(frame, (ix, iy), (fx, fy), (255, 0, 0), 1)

    cv2.imshow('Preview', frame)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()
