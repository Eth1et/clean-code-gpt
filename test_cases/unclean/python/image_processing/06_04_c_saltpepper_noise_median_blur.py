
import cv2
import numpy as np

noise_salt_percentage = 0.05
noise_pepper_percentage = 0.05
median_size = 3
blur_size = 3


def on_median_size_change(pos):
    global median_size

    median_size = pos * 2 + 3
    print('Median size:', median_size)
    do_filter()


def on_blur_size_change(pos):
    global blur_size

    blur_size = pos * 2 + 3
    print('Blur size: ' + str(blur_size) + 'x' + str(blur_size))
    do_filter()


def on_salt_change(pos):
    global img, img_noise
    global noise_salt_percentage, noise_pepper_percentage

    noise_salt_percentage = pos / 100.0
    img_noise = add_salt_and_pepper_noise(img, noise_salt_percentage, noise_pepper_percentage)
    cv2.imshow('noise', img_noise)
    do_filter()


def on_pepper_change(pos):
    global img, img_noise
    global noise_salt_percentage, noise_pepper_percentage

    noise_pepper_percentage = pos / 100.0
    img_noise = add_salt_and_pepper_noise(img, noise_salt_percentage, noise_pepper_percentage)
    cv2.imshow('noise', img_noise)
    do_filter()


def do_filter():
    global median_size, blur_size
    global img_noise

    img_median = cv2.medianBlur(img_noise, median_size)
    cv2.imshow('median', img_median)

    img_noise_blur = cv2.blur(img_noise, (blur_size, blur_size))
    cv2.imshow('blur', img_noise_blur)


def add_point_noise(img_in, percentage, value):
    noise_res = np.copy(img_in)
    n = int(img_in.shape[0] * img_in.shape[1] * percentage)
    # print(n)

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
img = cv2.imread('GolyoAlszik_rs.jpg', cv2.IMREAD_GRAYSCALE)
# img = cv2.imread('screen01_h.png', cv2.IMREAD_GRAYSCALE)

img_noise = add_salt_and_pepper_noise(img, noise_salt_percentage, noise_pepper_percentage)
cv2.imshow('noise', img)
cv2.createTrackbar('salt', 'noise', 5, 25, on_salt_change)
cv2.createTrackbar('pepper', 'noise', 5, 25, on_pepper_change)

cv2.imshow('median', img_noise)
cv2.createTrackbar('size', 'median', 0, 20, on_median_size_change)
on_median_size_change(0)

cv2.imshow('blur', img_noise)
cv2.createTrackbar('size', 'blur', 0, 20, on_blur_size_change)
on_blur_size_change(0)

cv2.waitKey(0)
cv2.destroyAllWindows()
