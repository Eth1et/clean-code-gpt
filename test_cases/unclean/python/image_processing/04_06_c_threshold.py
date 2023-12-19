
import cv2
import numpy as np

# src = cv2.imread('screen01_h.png', cv2.IMREAD_GRAYSCALE)
src = cv2.imread('Sudoku_rs.jpg', cv2.IMREAD_GRAYSCALE)
cv2.imshow('Source', src)

print('Global threshold at intensity value 128.')
threshold, im_thresh = cv2.threshold(src, 128, 255, cv2.THRESH_BINARY)
cv2.imshow('Result', im_thresh)
cv2.waitKey(0)

threshold, im_thresh = cv2.threshold(src, -1, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
print('Detected Otsu threshold = {}'.format(threshold))
cv2.imshow('Result', im_thresh)
cv2.waitKey(0)

print('Global threshold at intensity value 128 using Numpy array operations.')
im_thresh = np.ndarray(src.shape, src.dtype)
im_thresh[src >= 128] = 255
im_thresh[src < 128] = 0
cv2.imshow('Result', im_thresh)
cv2.waitKey(0)

cv2.destroyAllWindows()
