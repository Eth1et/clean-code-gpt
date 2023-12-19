
import cv2
import numpy as np


def on_threshold_trackbar(trackPos):
    print('Global threshold at intensity value {}.'.format(trackPos))
    threshold, im_thresh = cv2.threshold(src, trackPos, 255, cv2.THRESH_BINARY)
    cv2.imshow('Result', im_thresh)


src = cv2.imread('screen01_h.png', cv2.IMREAD_GRAYSCALE)
cv2.imshow('Source', src)

otsuThreshold, im_thresh = cv2.threshold(src, -1, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
print('Detected Otsu threshold = {}'.format(otsuThreshold))
cv2.imshow('Result', im_thresh)

cv2.createTrackbar('threshold', 'Result', int(otsuThreshold), 255, on_threshold_trackbar)
cv2.waitKey(0)

cv2.destroyAllWindows()
