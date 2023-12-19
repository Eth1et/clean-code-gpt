
# http://web.stanford.edu/~sujason/ColorBalancing/simplestcb.html
# https://gist.github.com/DavidYKay/9dad6c4ab0d8d7dbf3dc

import cv2
import numpy as np
from matplotlib import pyplot as plt
import time

global img, out, fig, graph1, hist_im
init_percentage = 4
plot_full_histogram = False


def get_diagram_as_image(in_fig):
    in_fig.canvas.draw()
    data = np.frombuffer(in_fig.canvas.tostring_rgb(), dtype=np.uint8)
    data = data.reshape(in_fig.canvas.get_width_height()[::-1] + (3,))
    data_bgr = cv2.cvtColor(data, cv2.COLOR_RGB2BGR)

    return data_bgr


def draw_histogram(src, full_histogram=True):
    global hist_im

    hist_b = cv2.calcHist([src], [0], None, [256], [0, 256])
    hist_g = cv2.calcHist([src], [1], None, [256], [0, 256])
    hist_r = cv2.calcHist([src], [2], None, [256], [0, 256])

    plt.xlim([0, 255])
    plt.ylim([0, max(np.max(hist_b), np.max(hist_g), np.max(hist_r))])

    if not full_histogram:
        hist_b[0] = 0
        hist_b[255] = 0
        hist_g[0] = 0
        hist_g[255] = 0
        hist_r[0] = 0
        hist_r[255] = 0

    x = np.arange(0, 256, 1)
    ax.clear()
    ax.scatter(x, hist_b, s=1, color='b')
    ax.scatter(x, hist_g, s=1, color='g')
    ax.scatter(x, hist_r, s=1, color='r')

    hist_im = get_diagram_as_image(fig)
    cv2.imshow('histogram', hist_im)


def apply_mask(matrix, mask, fill_value):
    masked = np.ma.array(matrix, mask=mask, fill_value=fill_value)
    return masked.filled()


def apply_threshold(matrix, low_value, high_value):
    low_mask = matrix < low_value
    matrix = apply_mask(matrix, low_mask, low_value)

    high_mask = matrix > high_value
    matrix = apply_mask(matrix, high_mask, high_value)

    return matrix


def simple_cb_hist(in_img, percent):
    assert in_img.shape[2] == 3
    assert 0 < percent < 100

    print('==================================')
    start_time = time.perf_counter()
    half_percent = percent / 200.0

    channels = cv2.split(in_img)

    out_channels = []
    for channel in channels:
        assert len(channel.shape) == 2
        hist_gray = cv2.calcHist([channel], [0], None, [256], [0, 256])
        height, width = channel.shape
        vec_size = width * height

        pixel_sum = 0
        idx = 0
        pixel_sum_stop = vec_size * half_percent
        print(pixel_sum_stop)
        while pixel_sum <= pixel_sum_stop:
            pixel_sum += hist_gray[idx]
            idx += 1

        low_val = idx - 1
        print("Lowval: ", low_val)

        pixel_sum_stop = vec_size * (1.0 - half_percent)
        print(pixel_sum_stop)
        while pixel_sum <= pixel_sum_stop:
            pixel_sum += hist_gray[idx]
            idx += 1

        high_val = idx - 1
        print("Highval: ", high_val)
        # saturate below the low percentile and above the high percentile
        thresholded = apply_threshold(channel, low_val, high_val)
        # scale the channel
        normalized = cv2.normalize(thresholded, thresholded.copy(), 0, 255, cv2.NORM_MINMAX)
        out_channels.append(normalized)

    end_time = time.perf_counter()
    print((end_time - start_time) * 1000.0, "ezredmásodperc.")

    return cv2.merge(out_channels)


def on_trackbar(x):
    global img, out

    print("======================")
    print("Percentage:", x + 1)
    out = simple_cb_hist(img, x + 1)
    cv2.imshow("before", img)
    cv2.imshow("after", out)
    draw_histogram(out, plot_full_histogram)


if __name__ == '__main__':
    img = cv2.imread('SeaCliffBridge_1_800.jpg')
    # img = cv2.imread('PalPant_800.jpg')
    # img = cv2.imread('SeaCliffBridge_1_800.jpg')
    # img = cv2.imread('hk_flower_h.jpg')
    # img = cv2.imread('Tulipanok_01_800.jpg')
    # img = cv2.imread('Olympos_800.jpg')

    fig = plt.figure()
    ax = fig.add_subplot(111)

    cv2.imshow("after", img)
    cv2.createTrackbar('Cutoff percentage', 'after', init_percentage, 98, on_trackbar)

    while True:
        key = cv2.waitKey(0)
        if key == 27 or key == ord('q'):
            break

        if key == ord('s'):
            cv2.imwrite('05_04_scb.jpg', out)
            cv2.imwrite('05_04_scb_hist.png', hist_im)

    cv2.destroyAllWindows()
