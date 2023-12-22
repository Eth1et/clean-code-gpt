
import numpy as np
import cv2


def on_trackbar(tb_rot):
    global cols, rows

    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), tb_rot, 1)
    dst = cv2.warpAffine(img, M, (cols, rows))
    cv2.imshow('image', dst)


img = cv2.imread('OpenCV-logo.png', cv2.IMREAD_UNCHANGED)
rows, cols = img.shape[:2]
cv2.imshow('image', img)
cv2.createTrackbar('R', 'image', 0, 360, on_trackbar)

cv2.waitKey(0)
cv2.destroyWindow('image')
