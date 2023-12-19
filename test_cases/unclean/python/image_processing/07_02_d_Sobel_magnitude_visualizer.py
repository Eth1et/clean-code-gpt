
import cv2
import numpy as np
import math

MAGN_THRESH_PERCENT = 0.2
# ARROW_MAX_LENGTH = 200
SHOW_CONCATENATED_RESULT = False


def gradient_draw_callback(event, x, y, flags, param):
    global img, img_dx, img_dy, img_gradient_magnitude
    global img_dx_norm, img_dy_norm, img_gradient_magnitude_norm
    # global ARROW_MAX_LENGTH

    # Ha szükségünk van a vektor szögére.
    angle_rad = math.atan2(img_dy[y, x], img_dx[y, x])
    angle_deg = math.degrees(angle_rad)
    # Ha a rajzolt vektor hosszát maximalizálni akarjuk.
    # print(math.degrees(angle_rad), img_gradient_magnitude[y, x])
    # arr_length = ARROW_MAX_LENGTH * img_gradient_magnitude[y, x] / np.amax(img_gradient_magnitude)
    # x2 = round(x + arr_length * math.cos(angle))
    # y2 = round(y + arr_length * math.sin(angle))

    # Ha a tényleges vektor hosszát rajzoljuk, ez is elég.
    x2 = round(x + img_dx[y, x])
    y2 = round(y + img_dy[y, x])

    img_arrow = cv2.merge([img.copy(), img.copy(), img.copy()])
    cv2.line(img_arrow, (x, y), (x2, y), (0, 255, 0), 2)
    cv2.line(img_arrow, (x2, y), (x2, y2), (255, 0, 0), 2)
    cv2.arrowedLine(img_arrow, (x, y), (x2, y2), (0, 0, 255), 3, tipLength=0.25)
    angle_deg_rounded = round(angle_deg, 2)
    cv2.putText(img_arrow, 'Angle: ' + str(angle_deg_rounded) + ' degrees', (6, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
    cv2.putText(img_arrow, 'Angle: ' + str(angle_deg_rounded) + ' degrees', (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255))
    cv2.imshow('img', img_arrow)

    img_dx_bgr = cv2.cvtColor(img_dx_norm.copy(), cv2.COLOR_GRAY2BGR)
    cv2.circle(img_dx_bgr, (x, y), 2, (32, 32, 32), 4)
    cv2.circle(img_dx_bgr, (x, y), 1, (0, 255, 0), 2)
    cv2.putText(img_dx_bgr, 'Gradient X value: ' + str(img_dx[y, x]), (6, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
    cv2.putText(img_dx_bgr, 'Gradient X value: ' + str(img_dx[y, x]), (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
    cv2.imshow('Ix', img_dx_bgr)

    img_dy_bgr = cv2.cvtColor(img_dy_norm.copy(), cv2.COLOR_GRAY2BGR)
    cv2.circle(img_dy_bgr, (x, y), 2, (32, 32, 32), 4)
    cv2.circle(img_dy_bgr, (x, y), 1, (255, 0, 0), 2)
    cv2.putText(img_dy_bgr, 'Gradient Y value: ' + str(img_dy[y, x]), (6, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
    cv2.putText(img_dy_bgr, 'Gradient Y value: ' + str(img_dy[y, x]), (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))
    cv2.imshow('Iy', img_dy_bgr)

    img_magnitude_bgr = cv2.cvtColor(img_gradient_magnitude_norm.copy(), cv2.COLOR_GRAY2BGR)
    cv2.circle(img_magnitude_bgr, (x, y), 2, (32, 32, 32), 4)
    cv2.circle(img_magnitude_bgr, (x, y), 1, (255, 255, 0), 2)
    magnitude_rounded = round(img_gradient_magnitude[y, x], 2)
    cv2.putText(img_magnitude_bgr, 'Gradient magnitude: ' + str(magnitude_rounded), (6, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
    cv2.putText(img_magnitude_bgr, 'Gradient magnitude: ' + str(magnitude_rounded), (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0))
    cv2.imshow('Gradient magnitude', img_magnitude_bgr)

    if SHOW_CONCATENATED_RESULT:
        cv2.drawMarker(img_arrow, (x + 1, y + 1), (0, 0, 0), cv2.MARKER_CROSS, 50, 1)
        cv2.drawMarker(img_arrow, (x, y), (192, 192, 192), cv2.MARKER_CROSS, 50, 1)
        img_concat = cv2.vconcat([
                cv2.hconcat([img_dx_bgr, img_dy_bgr]),
                cv2.hconcat([img_magnitude_bgr, img_arrow])
        ])
        cv2.imshow('Gradient visualization', img_concat)


# img = cv2.imread('OpenCV-logo.png', cv2.IMREAD_GRAYSCALE)
img = cv2.imread('tree_blur_02.png', cv2.IMREAD_GRAYSCALE)
# img = cv2.imread('GolyoAlszik_rs.jpg', cv2.IMREAD_GRAYSCALE)
# img = cv2.imread('PalPant_800.jpg', cv2.IMREAD_GRAYSCALE)
# img = cv2.imread('SeaCliffBridge_3_800.jpg', cv2.IMREAD_GRAYSCALE)
cv2.imshow('img', img)


# Kép normalizálása és megjelenítése
def display_image(window, image):
    disp = cv2.normalize(image, None, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    cv2.imshow(window, disp)


# ksize = -1   # Scharr kernel
ksize = 3    # 3x3 Sobel
# ksize = 5    # 5x5 Sobel

img_dx = cv2.Sobel(img, cv2.CV_32FC1, 1, 0, None, ksize)
img_dx_norm = cv2.normalize(img_dx, None, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
cv2.imshow('Ix', img_dx_norm)

img_dy = cv2.Sobel(img, cv2.CV_32FC1, 0, 1, None, ksize)
img_dy_norm = cv2.normalize(img_dy, None, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
cv2.imshow('Iy', img_dy_norm)

img_gradient_magnitude = cv2.magnitude(img_dx, img_dy)
img_gradient_magnitude_norm = cv2.normalize(img_gradient_magnitude, None, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
cv2.imshow('Gradient magnitude', img_gradient_magnitude_norm)

magn_th = np.amax(img_gradient_magnitude) * MAGN_THRESH_PERCENT
print('magn_th =', magn_th)
_, ImagnTh = cv2.threshold(img_gradient_magnitude, magn_th, 1.0, cv2.THRESH_BINARY)
display_image('Thresholded gradient magnitude', ImagnTh)

cv2.setMouseCallback('img', gradient_draw_callback)

cv2.waitKey(0)
cv2.destroyAllWindows()
