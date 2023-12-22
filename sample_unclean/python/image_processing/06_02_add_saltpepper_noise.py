
import cv2
import numpy as np


def add_point_noise(img_in, percentage, value):
    noise_res = np.copy(img_in)
    n = int(img_in.shape[0] * img_in.shape[1] * percentage)
    print(n)

    for k in range(1, n):
        i = np.random.randint(0, img_in.shape[1])
        j = np.random.randint(0, img_in.shape[0])

        if img_in.ndim == 2:
            noise_res[j, i] = value

        if img_in.ndim == 3:
            noise_res[j, i] = [value, value, value]

    return noise_res


def add_salt_and_pepper_noise(img_in, percentage1, percentage2):
    n = add_point_noise(img_in, percentage1, 255)   # Só
    n2 = add_point_noise(n, percentage2, 0)         # Bors

    return n2


# img = cv2.imread('OpenCV-logo.png', cv2.IMREAD_GRAYSCALE)
img = cv2.imread('OpenCV-logo.png', cv2.IMREAD_COLOR)
noise = add_salt_and_pepper_noise(img, 0.01, 0.01)
cv2.imshow('SaltNPepper', noise)
cv2.waitKey(0)

cv2.destroyAllWindows()
