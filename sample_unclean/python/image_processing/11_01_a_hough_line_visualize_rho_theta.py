
import cv2
import math


def visualize_rho_theta():
    global rho, theta, img

    cp = img.copy()
    a = math.cos(math.radians(theta))
    b = math.sin(math.radians(theta))
    x0 = a * rho
    y0 = b * rho
    # Computing line endpoints outside of image matrix
    pt1 = (0, 0)
    pt2 = (int(x0), int(y0))
    cv2.line(cp, pt1, pt2, (255, 0, 0), 2, cv2.LINE_AA)
    pt1 = (int(x0 + size_max * (-b)), int(y0 + size_max * a))
    pt2 = (int(x0 - size_max * (-b)), int(y0 - size_max * a))
    cv2.line(cp, pt1, pt2, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.imshow('img', cp)


def on_rho_trackbar_change(x):
    global rho
    rho = x
    visualize_rho_theta()


def on_theta_trackbar_change(x):
    global theta
    theta = x
    visualize_rho_theta()


img = cv2.imread('sudoku_rs.jpg', cv2.IMREAD_COLOR)
# edge = cv2.Canny(img, 50, 300)
# img = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)
size_max = math.sqrt(img.shape[0] ** 2 + img.shape[1] ** 2)
rho = img.shape[0] >> 1
theta = 45

cv2.imshow('img', img)

cv2.createTrackbar('r (rho)', 'img', rho, int(size_max), on_rho_trackbar_change)
cv2.createTrackbar('theta', 'img', theta, 180, on_theta_trackbar_change)

cv2.waitKey(0)
cv2.destroyAllWindows()
