import cv2
import numpy as np

drawing = False  # initialize drawing status


# function that mouse actions constantly callback to
def mouse_action(event, x, y, flags, param):  
    global img, img2, drawing, ix, iy

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True  # drawing begins
        ix, iy = x, y  # set initial x and y coordinates
        print('click')

    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        img = img2.copy()  # revert image to clean copy
        cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 2)  # redraw rectangle on a clean slate
        print(x),
        print(y)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(img, (ix, iy), (x, y), (255, 255, 255), 2)  # final drawn rectangle, in white
        print('release')


cv2.namedWindow('Preview')  # create window
cv2.setMouseCallback('Preview', mouse_action)  # bind mouse actions to a specific window

img = np.zeros((512, 512, 3), np.uint8)  # generate a a black image
img2 = img.copy()  # create a copy of the black image--CRUCIAL!!

while True:
    cv2.imshow('Preview', img)

    k = cv2.waitKey(1) & 0xFF  # press Escape to exit
    if k == 27:
        break

cv2.destroyAllWindows()
