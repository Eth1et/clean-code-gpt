
import cv2

FILE_INPUT = 'calb.png'
FILE_OUTPUT = 'calb_resized.png'
MAX_WIDTH = 640
MAX_HEIGHT = 480

img = cv2.imread(FILE_INPUT, cv2.IMREAD_COLOR)

h, w = img.shape[:2]
assert w > 0 and h > 0

ratio_w = MAX_WIDTH / w
ratio_h = MAX_HEIGHT / h

if ratio_w * h > MAX_HEIGHT:
    ratio = ratio_h
else:
    ratio = ratio_w

res_lanczos4 = cv2.resize(img, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_LANCZOS4)

print(res_lanczos4.shape)

cv2.imshow('Original', img)
cv2.imshow('Resampled Lanczos', res_lanczos4)
cv2.imwrite(FILE_OUTPUT, res_lanczos4)

cv2.waitKey(0)
cv2.destroyAllWindows()
