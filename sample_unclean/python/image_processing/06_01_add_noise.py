
import cv2
import numpy as np

img = cv2.imread('OpenCV-logo.png', cv2.IMREAD_GRAYSCALE)

noise = np.zeros(img.shape[:2], np.int16)
cv2.randn(noise, 0.0, 20.0)

imnoise1 = cv2.add(img, noise, dtype=cv2.CV_8UC1)
cv2.imshow('add', imnoise1)

imnoise2 = cv2.add(img, noise, dtype=cv2.CV_16SC1)
imnoisenorm = cv2.normalize(imnoise2, None, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
cv2.imshow('norm', imnoisenorm)

cv2.waitKey(0)

cv2.destroyAllWindows()
