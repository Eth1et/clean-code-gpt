
import cv2
import numpy as np

MAGNITUDE_THRESH_PERCENT = 0.2

img = cv2.imread('OpenCV-logo.png', cv2.IMREAD_GRAYSCALE)
# img = cv2.imread('GolyoAlszik_rs.jpg', cv2.IMREAD_GRAYSCALE)
# img = cv2.imread('PalPant_800.jpg', cv2.IMREAD_GRAYSCALE)
# img = cv2.imread('SeaCliffBridge_3_800.jpg', cv2.IMREAD_GRAYSCALE)


# Kép normalizálása és megjelenítése
def display_image(window, image):
    disp = cv2.normalize(image, None, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    cv2.imshow(window, disp)


Gx = np.array([
    [-1, 0, 1],
    [-2, 0, 2],
    [-1, 0, 1]])

img_dx = cv2.filter2D(img, cv2.CV_32F, Gx)
display_image('Ix', img_dx)

Gy = np.array([
    [1, 2, 1],
    [0, 0, 0],
    [-1, -2, -1]])

img_dy = cv2.filter2D(img, cv2.CV_32F, Gy)
display_image('Iy', img_dy)

img_gradient_magnitude = cv2.magnitude(img_dx, img_dy)
display_image('Gradient magnitude', img_gradient_magnitude)

magn_th = np.amax(img_gradient_magnitude) * MAGNITUDE_THRESH_PERCENT
print('magn_th =', magn_th)
_, ImagnTh = cv2.threshold(img_gradient_magnitude, magn_th, 1.0, cv2.THRESH_BINARY)
display_image('Thresholded gradient magnitude', ImagnTh)

cv2.waitKey(0)
cv2.destroyAllWindows()
