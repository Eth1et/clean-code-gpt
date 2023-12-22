
import cv2

# im = cv2.imread('SeaCliffBridge_3_800.jpg', cv2.IMREAD_GRAYSCALE)
im = cv2.imread('Sudoku_rs.jpg', cv2.IMREAD_GRAYSCALE)
cv2.imshow('Eredeti', im)

im_inverse = 255 - im
cv2.imshow('Inverz', im_inverse)
cv2.waitKey(0)

cv2.destroyAllWindows()
