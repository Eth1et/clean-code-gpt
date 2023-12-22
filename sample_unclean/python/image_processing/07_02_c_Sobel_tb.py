
import cv2
import numpy as np

MAGN_THRESH_PERCENT = 0.2

img = cv2.imread('OpenCV-logo.png', cv2.IMREAD_GRAYSCALE)
# img = cv2.imread('GolyoAlszik_rs.jpg', cv2.IMREAD_GRAYSCALE)
# img = cv2.imread('PalPant_800.jpg', cv2.IMREAD_GRAYSCALE)
# img = cv2.imread('SeaCliffBridge_3_800.jpg', cv2.IMREAD_GRAYSCALE)
img_bgr = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)


def on_tb_th_change(pos):
    global img_gradient_magnitude, img_bgr
    global magn_th

    _, img_th = cv2.threshold(img_gradient_magnitude, pos, 1.0, cv2.THRESH_BINARY)
    # display_image('Thresholded gradient magnitude', img_th)
    img_bgr_edge = img_bgr.copy()
    img_bgr_edge[img_th > 0] = [0, 0, 255]
    cv2.imshow('Thresholded gradient magnitude', img_bgr_edge)


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
img_gradient_magnitude_norm = cv2.normalize(img_gradient_magnitude, None, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
display_image('Gradient magnitude', img_gradient_magnitude)

gradient_max = np.amax(img_gradient_magnitude)
print('gradient_max =', gradient_max)
magn_th = round(gradient_max * MAGN_THRESH_PERCENT)
print('magn_th =', magn_th)

cv2.imshow('Thresholded gradient magnitude', img_gradient_magnitude_norm)
cv2.createTrackbar('Magnitude threshold', 'Thresholded gradient magnitude', magn_th, round(gradient_max + 1), on_tb_th_change)


cv2.waitKey(0)
cv2.destroyAllWindows()
