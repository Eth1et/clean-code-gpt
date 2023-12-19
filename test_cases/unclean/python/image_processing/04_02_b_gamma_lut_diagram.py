
# https://www.cambridgeincolour.com/tutorials/gamma-correction.htm

import cv2
import numpy as np
from matplotlib import pyplot as plt


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
    plt.plot(x, lut, label=label_text)
    cv2.imshow('gamma', im_lut)
    cv2.waitKey(0)


# im = cv2.imread('SeaCliffBridge_3_800.jpg', cv2.IMREAD_GRAYSCALE)
im = cv2.imread('Sudoku_rs.jpg', cv2.IMREAD_GRAYSCALE)

# Alappontok [0, 255]
x = np.arange(0, 256, 1, np.uint8)

# Grafikon beállítások
fig = plt.figure(figsize=(6, 6), dpi=80)
ax = fig.add_subplot(111)
ax.set_title('Gamma korrekció LUT diagram')
fig.canvas.setWindowTitle('Gamma korrekció LUT diagram')
plt.xlabel('Eredeti intenzitásérték')
plt.ylabel('Gamma korrekció után')
plt.xlim([0, 255])
plt.ylim([0, 255])

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

# LUT diagram megjelenítése
plt.legend()
# plt.savefig('03_02_b_gamma_lut_diagram.png', bbox_inches='tight')
plt.show()
