
import cv2
import numpy as np

MAGN_THRESH_PERCENT = 0.2

img = cv2.imread('OpenCV-logo.png', cv2.IMREAD_GRAYSCALE)
# img = cv2.imread('GolyoAlszik_rs.jpg', cv2.IMREAD_GRAYSCALE)
# img = cv2.imread('PalPant_800.jpg', cv2.IMREAD_GRAYSCALE)
# img = cv2.imread('SeaCliffBridge_3_800.jpg', cv2.IMREAD_GRAYSCALE)


# Kép normalizálása és megjelenítése
def display_image(window, image):
    disp = cv2.normalize(image, None, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    cv2.imshow(window, disp)


# ksize = -1   # Scharr kernel
ksize = 3    # 3x3 Sobel
# ksize = 5    # 5x5 Sobel

img_dx = cv2.Sobel(img, cv2.CV_32FC1, 1, 0, None, ksize)
display_image('Ix', img_dx)

img_dy = cv2.Sobel(img, cv2.CV_32FC1, 0, 1, None, ksize)
display_image('Iy', img_dy)

img_gradient_magnitude = cv2.magnitude(img_dx, img_dy)
display_image('Gradient magnitude', img_gradient_magnitude)

magn_th = np.amax(img_gradient_magnitude) * MAGN_THRESH_PERCENT
print('magn_th =', magn_th)
_, ImagnTh = cv2.threshold(img_gradient_magnitude, magn_th, 1.0, cv2.THRESH_BINARY)
display_image('Thresholded gradient magnitude', ImagnTh)

cv2.waitKey(0)
cv2.destroyAllWindows()
