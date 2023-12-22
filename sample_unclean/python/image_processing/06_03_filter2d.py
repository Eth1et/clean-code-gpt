import cv2
import numpy as np

img = cv2.imread('OpenCV-logo.png', cv2.IMREAD_GRAYSCALE)

noise = np.zeros(img.shape, np.int16)
cv2.randn(noise, 0.0, 20.0)

imnoise = cv2.add(img, noise, dtype=cv2.CV_8UC1)
cv2.imshow('noise', imnoise)

# kernel = np.array([[-1, -1, -1],
#                    [-1, 9, -1],
#                    [-1, -1, -1]])

kernel = np.array([[1, 1, 1],
                   [1, 1, 1],
                   [1, 1, 1]])

kernel = kernel / 9.0

print(kernel)

imnoisefilter = cv2.filter2D(imnoise, -1, kernel)
cv2.imshow('filter2d', imnoisefilter)
cv2.waitKey(0)

cv2.destroyAllWindows()
