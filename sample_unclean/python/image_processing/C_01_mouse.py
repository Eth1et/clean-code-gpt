
import cv2

start_x = start_y = -1
button_down = False


def mouse_event(event, x, y, flags, param):
    global start_x, start_y, button_down, im

    print('x, y:', x, y)

    if event == cv2.EVENT_LBUTTONDOWN:
        start_x = x
        start_y = y
        button_down = True

    if event == cv2.EVENT_MOUSEMOVE:
        if button_down:
            im = im_orig.copy()
            cv2.line(im, (start_x, start_y), (x, y), (0, 0, 255), 3)
            cv2.imshow('image', im)

    if event == cv2.EVENT_LBUTTONUP:
        start_x = start_y = -1
        button_down = False


im = cv2.imread('OpenCV-logo.png', cv2.IMREAD_COLOR)
im_orig = im.copy()
cv2.imshow('image', im)

cv2.setMouseCallback('image', mouse_event)

cv2.waitKey(0)

cv2.destroyAllWindows()
