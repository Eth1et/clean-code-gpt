
import cv2
import numpy as np


# HSV intervallum szegmentalas
def hsv_segment(interval_H, interval_S, interval_V, wndtitle):
    global imgHSV

    minHSV = np.array([interval_H[0], interval_S[0], interval_V[0]])
    maxHSV = np.array([interval_H[1], interval_S[1], interval_V[1]])
    segmented = cv2.inRange(imgHSV, minHSV, maxHSV)
    cv2.imshow(wndtitle, segmented)


# Foprogram

img = cv2.imread('fruits_h.jpg', cv2.IMREAD_COLOR)
cv2.imshow('origImg', img)

blurred = cv2.GaussianBlur(img, (5, 5), sigmaX=2.0, sigmaY=2.0)
imgHSV = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

# Narancsok
hsv_segment((10, 20), (205, 255), (155, 255), 'Narancs')

# Citrom
hsv_segment((20, 30), (160, 255), (175, 255), 'Citrom')

# Pomelo
hsv_segment((20, 55), (70, 255), (60, 150), 'Pomelo')

cv2.waitKey(0)
cv2.destroyAllWindows()
