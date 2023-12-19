import cv2
import numpy as np

img = cv2.imread('OpenCV-logo.png', cv2.IMREAD_GRAYSCALE)
# img = cv2.imread('GolyoAlszik_rs.jpg', cv2.IMREAD_GRAYSCALE)
# img = cv2.imread('PalPant_800.jpg', cv2.IMREAD_GRAYSCALE)
# img = cv2.imread('SeaCliffBridge_3_800.jpg', cv2.IMREAD_GRAYSCALE)

blurred = cv2.GaussianBlur(img, (5, 5), 2.0)
LoG = cv2.Laplacian(blurred, cv2.CV_16S, ksize=3)

# OpenCV dokumentáció hibás megoldása

LoG_abs = cv2.convertScaleAbs(LoG);
cv2.imshow('LoG_abs', LoG_abs)

# Nulla-átmenet közelítése: lokális környezetben a minimum negatív, a maximum pozitív

minLoG = cv2.morphologyEx(LoG, cv2.MORPH_ERODE, np.ones((3, 3)))
maxLoG = cv2.morphologyEx(LoG, cv2.MORPH_DILATE, np.ones((3, 3)))

zero_cross = np.logical_and(minLoG < -10, maxLoG > 10)
zero_cross_im = np.zeros(zero_cross.shape, np.uint8)
zero_cross_im[zero_cross] = 255
cv2.imshow('zero_cross_im', zero_cross_im)

cv2.waitKey(0)
cv2.destroyAllWindows()
