
# https://www.cambridgeincolour.com/tutorials/gamma-correction.htm

import cv2
import numpy as np
from matplotlib import pyplot as plt


def on_trackbar(pos):
    global img

    gamma = (pos / 10.0) - 3
    if gamma < 1:
        gamma = -1.0 / (gamma - 2.0)

    lut = create_gamma_lut(gamma)
    applyLUT(img, lut, 'γ={0:2.2f}'.format(gamma))


def get_diagram_as_image(fig):
    fig.canvas.draw()
    data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    data_bgr = cv2.cvtColor(data, cv2.COLOR_RGB2BGR)

    return data_bgr


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
    global x, fig

    print(label_text)

    im_lut = cv2.LUT(image, lut, None)
    cv2.imshow('Gamma', im_lut)

    fig.clear()
    ax = fig.add_subplot(111)
    ax.set_title('Gamma korrekció LUT diagram')
    plt.plot(x, x, 'g--', label='Eredeti')
    plt.plot(x, lut, 'r-', label=label_text)
    plt.xlabel('Eredeti intenzitásérték')
    plt.ylabel('Gamma korrekció után')
    plt.xlim([0, 255])
    plt.ylim([0, 255])
    plt.legend()

    lut_diag = get_diagram_as_image(fig)
    cv2.imshow('Gamma LUT', lut_diag)


img = cv2.imread('SeaCliffBridge_3_800.jpg', cv2.IMREAD_GRAYSCALE)

# Alappontok [0, 255]
x = np.arange(0, 256, 1, np.uint8)

# Grafikon beállítások
fig = plt.figure(figsize=(6, 6), dpi=80)
fig.canvas.setWindowTitle('Gamma korrekció LUT diagram')

# Gamma korrekciók

cv2.imshow('Gamma', img)
cv2.createTrackbar('Parameter', 'Gamma', 40, 80, on_trackbar)
cv2.waitKey(0)

cv2.destroyAllWindows()
