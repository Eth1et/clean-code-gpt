
import cv2

img = cv2.imread('OpenCV-logo.png', cv2.IMREAD_GRAYSCALE)
# img = cv2.imread('tree_blur_02.png', cv2.IMREAD_GRAYSCALE)
# img = cv2.imread('GolyoAlszik_rs.jpg', cv2.IMREAD_GRAYSCALE)

blurred = cv2.GaussianBlur(img, (5, 5), 2.0)
edges = cv2.Canny(blurred, 100, 200, None, 5, True)
cv2.imshow('Canny', edges)
cv2.waitKey(0)

cv2.destroyAllWindows()
