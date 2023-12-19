
import cv2
import numpy as np
from matplotlib import pyplot as plt


def do_clip():
    global img, img_orig, fig
    global th_lower, th_upper

    img = img_orig.copy()
    img[img_orig > th_upper] = th_upper
    img[img_orig < th_lower] = th_lower
    hist_stretch = cv2.normalize(img, None, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)

    cv2.imshow('img', hist_stretch)
    hist_img = draw_histogram(img_orig, True)
    cv2.imshow('histogram', hist_img)


def on_change_lower_th(pos):
    global th_lower

    th_lower = pos
    do_clip()


def on_change_upper_th(pos):
    global th_upper

    th_upper = pos
    do_clip()


def get_diagram_as_image():
    global fig

    fig.canvas.draw()
    data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    data_bgr = cv2.cvtColor(data, cv2.COLOR_RGB2BGR)

    return data_bgr


def draw_histogram(src, draw_limits=False):
    global fig

    fig.clf()
    hist_gray = cv2.calcHist([src], [0], None, [256], [0, 256])
    plt.vlines(np.arange(256), 0, hist_gray)
    # plt.xlim([0, 255])
    plt.ylim([0, np.max(hist_gray)])
    if draw_limits:
        plt.axvline(th_lower, color='r')
        plt.axvline(th_upper, color='r')
    # plt.show()
    return get_diagram_as_image()


img = cv2.imread('Sudoku_rs.jpg', cv2.IMREAD_GRAYSCALE)
img_orig = img.copy()
cv2.imshow('img', img)

th_lower = np.amin(img)
th_upper = np.amax(img)
print('Using minimum and maximum intensity values:',  th_lower, th_upper)

fig = plt.figure(figsize=(4, 2), dpi=100)

cv2.createTrackbar('lower', 'img', th_lower, 255, on_change_lower_th)
cv2.createTrackbar('upper', 'img', th_upper, 255, on_change_upper_th)
do_clip()

cv2.waitKey(0)

cv2.destroyAllWindows()
