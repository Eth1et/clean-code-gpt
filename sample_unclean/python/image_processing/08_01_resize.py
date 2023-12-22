
import cv2

par_fx = 3
par_fy = 1.5

img = cv2.imread('calb.png', cv2.IMREAD_COLOR)

res_nearest = cv2.resize(img, None, fx=par_fx, fy=par_fy, interpolation=cv2.INTER_NEAREST)
res_linear = cv2.resize(img, None, fx=par_fx, fy=par_fy, interpolation=cv2.INTER_LINEAR)
res_area = cv2.resize(img, None, fx=par_fx, fy=par_fy, interpolation=cv2.INTER_AREA)
res_cubic = cv2.resize(img, None, fx=par_fx, fy=par_fy, interpolation=cv2.INTER_CUBIC)
res_lanczos4 = cv2.resize(img, None, fx=par_fx, fy=par_fy, interpolation=cv2.INTER_LANCZOS4)

cv2.imshow('Original', img)
cv2.imshow('Resampled nearest', res_nearest)
cv2.imshow('Resampled linear', res_linear)
cv2.imshow('Resampled area', res_area)
cv2.imshow('Resampled cubic spline', res_cubic)
cv2.imshow('Resampled Lanczos', res_lanczos4)
cv2.waitKey(0)

cv2.destroyAllWindows()
