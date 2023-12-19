
# Megjegyzés: a Niblack függvény az OpenCV contrib csomagjában érhető el.
# Ha használni szeretnénk, ilyen OpenCV verziót telepítsünk!

import cv2

tb_k = 18
tb_k_max = 20
# Niblack k paraméter számítása: (tb_k - 10.0) / 10.0
# [-1.0, 1.0] közötti számot kapunk, 1 tizedesjegy pontossággal
# A kezdőérték így 0.8 lesz.

tb_block_size = 18
tb_block_size_max = 30
# Niblack blockSize paraméter számítása: 2 * tb_blockSize + 3
# Lehetséges értékek: 3, 5, 7, ..., 63
# A kezdőérték 39.

tb_type = 0
tb_type_max = 4
# 5 féle OpenCV küszöbölési típus a tb_types szerint.
# Kezdőértékként cv2.THRESH_BINARY.

tb_types = [cv2.THRESH_BINARY, cv2.THRESH_BINARY_INV, cv2.THRESH_TRUNC, cv2.THRESH_TOZERO, cv2.THRESH_TOZERO_INV]
tb_type_strings = ['cv2.THRESH_BINARY',
                   'cv2.THRESH_BINARY_INV',
                   'cv2.THRESH_TRUNC',
                   'cv2.THRESH_TOZERO',
                   'cv2.THRESH_TOZERO_INV']


def refresh_niblack_result():
    k = float((tb_k - 10) / 10)

    block_size = 3
    if tb_block_size > 1:
        block_size = 2 * tb_block_size + 3

    threshold_type = tb_types[tb_type]
    print('Niblack parameters: blocksize={} k={} type={}'.format(block_size, k, tb_type_strings[tb_type]))
    dst = cv2.ximgproc.niBlackThreshold(src, 255, threshold_type, block_size, k)
    cv2.imshow('Niblack', dst)
    cv2.imwrite('threshold_niblack_result.png', dst)


def on_nb_trackbar_k(track_pos):
    global tb_k
    tb_k = track_pos
    refresh_niblack_result()


def on_nb_trackbar_block_size(track_pos):
    global tb_block_size
    tb_block_size = track_pos
    refresh_niblack_result()


def on_nb_trackbar_type(track_pos):
    global tb_type
    tb_type = track_pos
    refresh_niblack_result()


src = cv2.imread('screen01_h.png', cv2.IMREAD_GRAYSCALE)
cv2.imshow('src', src)
cv2.namedWindow('Niblack')

cv2.createTrackbar('k', 'Niblack', tb_k, tb_k_max, on_nb_trackbar_k)
cv2.createTrackbar('blockSize', 'Niblack', tb_block_size, tb_block_size_max, on_nb_trackbar_block_size)
cv2.createTrackbar('thresType', 'Niblack', tb_type, tb_type_max, on_nb_trackbar_type)

cv2.waitKey(0)
cv2.destroyAllWindows()
