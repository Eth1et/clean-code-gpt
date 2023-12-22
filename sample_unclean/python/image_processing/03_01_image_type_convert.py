
import cv2
import numpy as np

# Kép beolvasása és megjelenítése
img_uint8 = cv2.imread('OpenCV-logo.png', cv2.IMREAD_GRAYSCALE)
print('img_uint8[100, 100] =', img_uint8[100, 100])
cv2.imwrite('logo-uint8.png', img_uint8)
cv2.imshow('img_uint8', img_uint8)
cv2.waitKey(0)

# Konverzió uint16-ra
img_uint16 = np.uint16(img_uint8)
print('img_uint16[100, 100] =', img_uint16[100, 100])
cv2.imshow('img_uint16', img_uint16)
cv2.imwrite('logo-uint16.png', img_uint16)
cv2.waitKey(0)

# uint16 256-tal szorzás
img_uint16_mult256 = img_uint16 * 256
print('img_uint16[100, 100] =', img_uint16_mult256[100, 100])
cv2.imshow('img_uint16_mult256', img_uint16_mult256)
cv2.imwrite('logo-uint16_mult256.png', img_uint16_mult256)
cv2.waitKey(0)

# Konverzió int16-ra
img_int16 = np.int16(img_uint8)
print('img_int16[100, 100] =', img_int16[100, 100])
cv2.imshow('img_int16', img_int16)
cv2.imwrite('logo-int16.png', img_int16)
cv2.waitKey(0)

# Konverzió float32-re
img_float32 = np.float32(img_uint8)
print('img_float32[100, 100] =', img_float32[100, 100])
cv2.imshow('img_float32', img_float32)
cv2.imwrite('logo-float32.png', img_float32)
cv2.waitKey(0)

img_float32f_norm = cv2.normalize(img_float32, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
print('img_float32_norm[100, 100] =', img_float32f_norm[100, 100])
cv2.imshow('img_float32_norm', img_float32f_norm)
cv2.imwrite('logo-float32_norm.png', img_float32f_norm)
cv2.waitKey(0)

cv2.destroyAllWindows()
