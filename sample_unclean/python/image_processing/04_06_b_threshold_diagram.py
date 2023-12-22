
import numpy as np
import cv2
from matplotlib import pyplot as plt

thresh_value = 80
thresh_maxval = 200


def get_diagram_as_image(fig):
    fig.canvas.draw()
    data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    data_bgr = cv2.cvtColor(data, cv2.COLOR_RGB2BGR)

    return data_bgr


def plot_thresh_result(res, title_text, fname=None):
    ax.clear()
    ax.set_title(title_text)
    plt.xlim([0, 255])
    plt.ylim([-10, 265])
    # plt.axis('equal')
    # plt.xlabel('Eredeti intenzitásérték')
    # plt.ylabel('Küszöbölés/vágás után')
    # plt.scatter(125, 0, c='r')
    plt.plot(x, x, 'g--', label='Eredeti')
    plt.axvline(x=thresh_value, c='b', label='thresh')
    plt.plot(x, maxval_values, 'y--', linewidth=1, label='maxval')
    plt.plot(res, c='r', linewidth=3, label='Eredmény')
    plt.legend()
    res_lut_diag = get_diagram_as_image(fig)
    cv2.imshow('lut_result', res_lut_diag)
    if fname is not None:
        cv2.imwrite(fname, res_lut_diag)
    cv2.waitKey(0)


# Alappontok [0, 255]
x = np.arange(0, 256, 1, np.uint8)
maxval_values = np.arange(0, 256, 1, np.uint8)
maxval_values.fill(thresh_maxval)

# Grafikon beállítások
fig = plt.figure(figsize=(4, 4), dpi=100)
# fig = plt.figure()
ax = fig.add_subplot(111)
fig.canvas.setWindowTitle('cv2.threshold() LUT diagramok')
plt.xlim([0, 255])
plt.ylim([-10, 265])

threshold, res1 = cv2.threshold(x, thresh_value, thresh_maxval, cv2.THRESH_BINARY)
plot_thresh_result(res1, 'cv2.threshold() THRESH_BINARY', '03_05_b_thresh_binary.png')

threshold, res2 = cv2.threshold(x, thresh_value, thresh_maxval, cv2.THRESH_BINARY_INV)
plot_thresh_result(res2, 'cv2.threshold() THRESH_BINARY_INV', '03_05_b_thresh_binary_inv.png')

threshold, res3 = cv2.threshold(x, thresh_value, thresh_maxval, cv2.THRESH_TRUNC)
plot_thresh_result(res3, 'cv2.threshold() THRESH_BINARY_TRUNC', '03_05_b_thresh_trunc.png')

threshold, res4 = cv2.threshold(x, thresh_value, thresh_maxval, cv2.THRESH_TOZERO)
plot_thresh_result(res4, 'cv2.threshold() THRESH_TOZERO', '03_05_b_thresh_tozero.png')

threshold, res5 = cv2.threshold(x, thresh_value, thresh_maxval, cv2.THRESH_TOZERO_INV)
plot_thresh_result(res5, 'cv2.threshold() THRESH_TOZERO_INV', '03_05_b_thresh_tozero_inv.png')
