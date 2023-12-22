
import cv2
import numpy as np


def create_gamma_lut(gamma):
    """Gamma paraméter értéknek megfelelő 256 elemű keresőtábla generálása.
    A hatványozás miatt először [0, 1] tartományra kell konvertálni, majd utána vissza [0, 255] közé.
    """
    lut = np.arange(0, 256, 1, np.float32)
    lut = lut / 255.0
    lut = lut ** gamma
    lut = np.uint8(lut * 255.0)

    return lut


def applyLUT(image, lut, label_text):
    global x

    print(label_text)
    im_lut = cv2.LUT(image, lut, None)
    cv2.imshow('gamma', im_lut)
    cv2.waitKey(0)


# im = cv2.imread('SeaCliffBridge_3_800.jpg', cv2.IMREAD_GRAYSCALE)
im = cv2.imread('Sudoku_rs.jpg', cv2.IMREAD_GRAYSCALE)

# Gamma korrekciók

lut = create_gamma_lut(1.0 / 3.0)
applyLUT(im, lut, 'γ=1/3')

lut = create_gamma_lut(0.5)
applyLUT(im, lut, 'γ=1/2')

lut = np.arange(0, 256, 1, np.uint8)
applyLUT(im, lut, 'γ=1')

lut = create_gamma_lut(2.0)
applyLUT(im, lut, 'γ=2')

lut = create_gamma_lut(3.0)
applyLUT(im, lut, 'γ=3')

cv2.destroyAllWindows()
