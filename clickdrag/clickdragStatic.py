import cv2
import numpy as np

drawing = False


def mouse_action(event, x, y, flags, param):
    global img, img2, drawing, ix, iy

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        print('click')

    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        img = img2.copy()
        cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 2)
        print(x),
        print(y)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(img, (ix, iy), (x, y), (255, 255, 255), 2)  # final drawn rectangle
        print('release')


cv2.namedWindow('Preview')
cv2.setMouseCallback('Preview', mouse_action)

img = np.zeros((512, 512, 3), np.uint8)
img2 = img.copy()

while True:
    cv2.imshow('Preview', img)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
