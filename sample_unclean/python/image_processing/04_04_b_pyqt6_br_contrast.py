
# https://www.dfstudios.co.uk/articles/programming/image-programming-algorithms/image-processing-algorithms-part-5-contrast-adjustment/
# https://www.tutorialspoint.com/pyqt/pyqt_qslider_widget_signal.htm

import cv2
import numpy as np
from matplotlib import pyplot as plt

from PyQt6.QtCore import *
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget, QVBoxLayout, QSlider
from PyQt6.QtGui import QPixmap, QImage

global img, new_image
global brightness, contrast


def button_clicked_reset():
    global brightness, contrast
    brightness = 0
    contrast = 0
    bsl.setValue(0)
    csl.setValue(0)
    do_brightness_contrast()


def image_cv2qt(img_in):
    img_rgb = cv2.cvtColor(img_in, cv2.COLOR_BGR2RGB)
    height, width, channel = img_rgb.shape
    bytes_per_line = 3 * width
    qt_img = QImage(img_rgb.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)

    return QPixmap(qt_img)


def brightness_value_change():
    global brightness, bsl
    brightness = bsl.value()
    do_brightness_contrast()


def contrast_value_change():
    global contrast, csl
    contrast = csl.value()
    do_brightness_contrast()


def get_diagram_as_image(fig_in):
    fig_in.canvas.draw()
    data = np.frombuffer(fig_in.canvas.tostring_rgb(), dtype=np.uint8)
    data = data.reshape(fig_in.canvas.get_width_height()[::-1] + (3,))
    data_bgr = cv2.cvtColor(data, cv2.COLOR_RGB2BGR)

    return data_bgr


def do_brightness_contrast():
    global brightness, contrast, new_image, img

    # print('======================')
    # print('Brightness:', brightness)
    # print('Contrast:', contrast)

    labelBrText.setText('Brightness value: ' + str(brightness))
    labelCText.setText('Contrast value: ' + str(contrast))

    factor = (259 * (contrast + 255)) / (255 * (259 - contrast))
    # print('Factor:', factor)

    lut = np.arange(0, 256, 1)
    lut = np.uint8(np.clip(brightness + factor * (np.float32(lut) - 128.0) + 128, 0, 255))
    new_image = cv2.LUT(img, lut)

    ax.clear()
    ax.plot(x, x, 'g--', label='Eredeti', linewidth=5)
    ax.plot(x, lut, 'r-', label='Fényesség/kontraszt leképezés', linewidth=5)
    # plt.legend()

    lut_im = get_diagram_as_image(fig)
    lh, lw, ld = np.shape(lut_im)
    new_image[0:lh, 0:lw] = lut_im

    pmap = image_cv2qt(new_image)
    label.setPixmap(pmap)


if __name__ == '__main__':
    # img = cv2.imread('DSC07397_cut.jpg')
    # img = cv2.imread('IMG_20170820_152307_rs.jpg')
    img = cv2.imread('hk_flower_h.jpg')
    # img = cv2.imread('DSC02619_800.jpg', cv2.IMREAD_COLOR)
    new_image = img.copy()

    # Grafikon beállítások
    fig = plt.figure(figsize=(4, 4), dpi=25)
    ax = fig.add_subplot(111)
    # plt.xlabel('Eredeti intenzitásérték')
    # plt.ylabel('Pont operáció eredménye')
    plt.xlim([0, 255])
    # plt.ylim([0, 255])
    x = np.arange(0, 256, 1)

    brightness = 0
    contrast = 0

    app = QApplication([])
    win = QMainWindow()
    win.setWindowTitle('PyQt6 brightness/contrast')
    w = QWidget()

    button = QPushButton('Reset', w)
    button.clicked.connect(button_clicked_reset)

    bsl = QSlider(Qt.Orientation.Horizontal)
    bsl.setMinimum(-255)
    bsl.setMaximum(255)
    bsl.setValue(0)
    bsl.setTickInterval(10)
    bsl.setTickPosition(QSlider.TickPosition.TicksBelow)
    bsl.valueChanged.connect(brightness_value_change)

    csl = QSlider(Qt.Orientation.Horizontal)
    csl.setMinimum(-255)
    csl.setMaximum(255)
    csl.setValue(0)
    csl.setTickInterval(10)
    csl.setTickPosition(QSlider.TickPosition.TicksBelow)
    csl.valueChanged.connect(contrast_value_change)

    label = QLabel(w)
    pixmap = QPixmap(image_cv2qt(img))
    label.setPixmap(pixmap)

    labelBrText = QLabel(w)
    labelCText = QLabel(w)

    layout = QVBoxLayout(w)
    layout.addWidget(label)
    layout.addWidget(button)
    layout.addWidget(bsl)
    layout.addWidget(labelBrText)
    layout.addWidget(csl)
    layout.addWidget(labelCText)

    win.setCentralWidget(w)

    win.show()
    button_clicked_reset()
    app.exit(app.exec())
