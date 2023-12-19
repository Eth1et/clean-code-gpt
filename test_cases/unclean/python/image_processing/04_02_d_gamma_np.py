
import cv2


def on_trackbar(x):
    global img

    gamma = (x / 10.0) - 3
    if gamma < 1:
        gamma = -1.0 / (gamma - 2.0)
    print("======================")
    print("Gamma value:", gamma)

    temp = cv2.normalize(img, None, 0, 1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32FC1)
    gamma_corr = temp ** gamma
    out = cv2.normalize(gamma_corr, None, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    cv2.imshow("Gamma", out)


if __name__ == '__main__':
    # img = cv2.imread('Olympos.jpg')
    # img = cv2.imread('PalPant_800.jpg')
    img = cv2.imread('SeaCliffBridge_3_800.jpg', cv2.IMREAD_GRAYSCALE)

    cv2.imshow("Original", img)
    cv2.imshow("Gamma", img)
    cv2.createTrackbar('Parameter', 'Gamma', 40, 80, on_trackbar)
    cv2.waitKey(0)

cv2.destroyAllWindows()
