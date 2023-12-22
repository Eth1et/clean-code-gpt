
import cv2
import numpy as np

src = cv2.imread('car_numberplate_rs.jpg', cv2.IMREAD_GRAYSCALE)
cv2.imshow('Eredeti', src)

im_thresh = np.ndarray(src.shape, src.dtype)

im_thresh[src >= 120] = 255
im_thresh[src < 120] = 0
cv2.imshow('Kuszobolt 120 ertekkel', im_thresh)

im_thresh.fill(0)
im_thresh[(src >= 80) & (src <= 160)] = 255
cv2.imshow('Kuszoboles 80-160 tartomanyban', im_thresh)

im_clip = src.copy()
im_clip[src < 80] = 0
im_clip[src > 160] = 0
cv2.imshow('Vagas ket kuszobbel', im_clip)
cv2.waitKey(0)

cv2.destroyAllWindows()
