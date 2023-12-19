
import cv2
import numpy as np

img = cv2.imread('OpenCV-logo.png', cv2.IMREAD_GRAYSCALE)

noise = np.zeros(img.shape, np.int16)
cv2.randn(noise, 0.0, 20.0)

imnoise = cv2.add(img, noise, dtype=cv2.CV_8UC1)
cv2.imshow('noise', imnoise)

imnoiseblur5x5 = cv2.blur(imnoise, (5, 5))
cv2.imshow('blur 5x5', imnoiseblur5x5)

imnoisegauss5x5 = cv2.GaussianBlur(imnoise, (5, 5), sigmaX=2.0, sigmaY=2.0)
cv2.imshow('gauss 5x5', imnoisegauss5x5)
cv2.waitKey(0)

cv2.destroyAllWindows()
