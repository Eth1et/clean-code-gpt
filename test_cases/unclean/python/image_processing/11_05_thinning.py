
import cv2

img = cv2.imread('binary_blobs.png', cv2.IMREAD_GRAYSCALE)
cv2.imshow('img', img)

thn = cv2.ximgproc.thinning(img, None, thinningType=cv2.ximgproc.THINNING_ZHANGSUEN)
# thn = cv2.ximgproc.thinning(img, None, thinningType=cv2.ximgproc.THINNING_GUOHALL)
cv2.imshow('thinning', thn)

bgr = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
b, g, r = cv2.split(bgr)
b = cv2.bitwise_and(b, ~thn)
g = cv2.bitwise_and(g, ~thn)
bgr = cv2.merge((b, g, r))
cv2.imshow('Overlay', bgr)

cv2.waitKey(0)
cv2.destroyAllWindows()
