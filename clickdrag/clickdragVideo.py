import cv2

drawing = False  # initialize drawing status
# initialize initial and final x, y coordinates
ix, iy = 0, 0
fx, fy = 0, 0


def mouse_action(event, x, y, flags, param):
    global drawing, ix, iy, fx, fy
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        fx, fy = x, y
        print('click')

    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        fx, fy = x, y
        print(x),
        print(y)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        print('release')


cap = cv2.VideoCapture(0)
# set resolution
cap.set(3, 640)
cap.set(4, 480)

cv2.namedWindow('Preview')
cv2.setMouseCallback('Preview', mouse_action)

while True:
    _, img = cap.read()
    
    # if drawing, draw blue rectangle that is variable. else, draw final white rectangle
    if drawing:
        cv2.rectangle(img, (ix, iy), (fx, fy), (255, 0, 0), 2)
    else:
        cv2.rectangle(img, (ix, iy), (fx, fy), (255, 255, 255), 2)

    cv2.imshow('Preview', img)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
