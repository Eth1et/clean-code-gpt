
import cv2

img = cv2.imread('calb.png', cv2.IMREAD_COLOR)
print(img.shape)

dsize = (200, 100)
dst = cv2.resize(img, dsize, interpolation=cv2.INTER_AREA)

fx = dsize[0] / img.shape[1]
fy = dsize[1] / img.shape[0]

print('fx =', fx)
print('fy =', fy)

cv2.imshow('Original', img)
cv2.imshow('Resampled area', dst)
cv2.waitKey(0)

cv2.destroyAllWindows()
