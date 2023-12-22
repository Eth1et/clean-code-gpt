
import cv2
import numpy as np

th_lower = 44
th_upper = 116
th_mode = 0


def th_clip():
    global src, th_lower, th_upper, th_mode

    im_th_clip = np.ndarray(src.shape, src.dtype)

    if th_mode == 0:
        im_th_clip.fill(0)
        im_th_clip[(src >= th_lower) & (src <= th_upper)] = 255

    if th_mode == 1:
        im_th_clip = src.copy()
        im_th_clip[src < th_lower] = 0
        im_th_clip[src > th_upper] = 0

    cv2.imshow('Vagas', im_th_clip)


def trackbar_lower(th):
    global th_lower

    th_lower = th
    th_clip()


def trackbar_upper(th):
    global th_upper

    th_upper = th
    th_clip()


def trackbar_mode(x):
    global th_mode

    th_mode = x
    th_clip()


src = cv2.imread('car_numberplate_rs.jpg', cv2.IMREAD_GRAYSCALE)
# src = cv2.imread('Sudoku_h.jpg', cv2.IMREAD_GRAYSCALE)
# src = cv2.imread('coins_rs.jpg', cv2.IMREAD_GRAYSCALE)
# src = cv2.imread('KozuzemiOraallasok/1313518560104.jpg', cv2.IMREAD_GRAYSCALE)
# src = cv2.imread('KozuzemiOraallasok/1313518629386.jpg', cv2.IMREAD_GRAYSCALE)
# src = cv2.imread('KozuzemiOraallasok/1313575791550.jpg', cv2.IMREAD_GRAYSCALE)
# src = cv2.imread('KozuzemiOraallasok/1313575818222.jpg', cv2.IMREAD_GRAYSCALE)
# src = cv2.imread('cards__numbers.jpg', cv2.IMREAD_GRAYSCALE)
# src = cv2.imread('four-kings-playing-cards-b1pk2m.jpg', cv2.IMREAD_GRAYSCALE)
# src = cv2.imread('FCards_02_rs.jpg', cv2.IMREAD_GRAYSCALE)
# src = cv2.imread('10_pr_formula.png', cv2.IMREAD_GRAYSCALE)
# src = cv2.imread('huszar1.jpg', cv2.IMREAD_GRAYSCALE)
# src = cv2.imread('shapes/shapes_10.jpg', cv2.IMREAD_GRAYSCALE)

cv2.imshow('Eredeti', src)

th_clip()

cv2.createTrackbar('Also', 'Vagas', th_lower, 255, trackbar_lower)
cv2.createTrackbar('Felso', 'Vagas', th_upper, 255, trackbar_upper)
cv2.createTrackbar('Mukodes', 'Vagas', th_mode, 1, trackbar_mode)

cv2.waitKey(0)
cv2.destroyAllWindows()
