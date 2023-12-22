
import cv2
import numpy as np


def add_additive_noise(sigma_in):
    global img

    noise = np.zeros(img.shape[:2], np.int16)
    cv2.randn(noise, 0.0, sigma_in)
    imnoise1 = cv2.add(img, noise, dtype=cv2.CV_8UC1)
    cv2.imshow('Noisy', imnoise1)


def on_sigma_change(pos):
    add_additive_noise(pos)


img = cv2.imread('OpenCV-logo.png', cv2.IMREAD_GRAYSCALE)
cv2.imshow('Noisy', img)
cv2.createTrackbar('sigma', 'Noisy', 50, 100, on_sigma_change)

cv2.waitKey(0)
cv2.destroyAllWindows()
