
import cv2
import numpy as np
from matplotlib import pyplot as plt


def drawHistogram(src):
    hist_gray = cv2.calcHist([src], [0], None, [256], [0, 256])
    plt.vlines(np.arange(256), 0, hist_gray)
    # plt.xlim([0, 255])
    plt.ylim([0, np.max(hist_gray)])
    plt.show()


img = cv2.imread('Sudoku_h.jpg', cv2.IMREAD_GRAYSCALE)
cv2.imshow('img', img)

fig = plt.figure(figsize=(4, 2), dpi=100)
drawHistogram(img)

th_lower = 100
th_upper = 140
img[img > th_upper] = th_upper
img[img < th_lower] = th_lower
hist_stretch = cv2.normalize(img, None, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)

cv2.imshow('img', hist_stretch)
fig2 = plt.figure(figsize=(4, 2), dpi=100)
drawHistogram(hist_stretch)
