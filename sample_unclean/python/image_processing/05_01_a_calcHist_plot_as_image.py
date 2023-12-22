
import cv2
import numpy as np
from matplotlib import pyplot as plt


def get_diagram_as_image(fig_in):
    fig_in.canvas.draw()
    data = np.frombuffer(fig_in.canvas.tostring_rgb(), dtype=np.uint8)
    data = data.reshape(fig_in.canvas.get_width_height()[::-1] + (3,))
    data_bgr = cv2.cvtColor(data, cv2.COLOR_RGB2BGR)

    return data_bgr


img = cv2.imread('GolyoAlszik_rs.jpg', cv2.IMREAD_GRAYSCALE)
# img = cv2.imread('screen01_h.png', cv2.IMREAD_GRAYSCALE)
# img = cv2.imread('Sudoku_h.jpg', cv2.IMREAD_GRAYSCALE)
# img = cv2.imread('FrenchCardsShapes.png', cv2.IMREAD_GRAYSCALE)
# img = cv2.imread('histogram/Picture5.png', cv2.IMREAD_GRAYSCALE)
# img = cv2.imread('Tulipanok_01_800.jpg', cv2.IMREAD_GRAYSCALE)

cv2.imshow('img', img)
print('Min: {}'.format(np.min(img)))
print('Max: {}'.format(np.max(img)))

hist_gray = cv2.calcHist([img], [0], None, [256], [0, 256])

fig = plt.figure(figsize=(4, 2), dpi=100)
# plt.plot(hist_gray)
# plt.scatter(np.arange(256), hist_gray, s=1)
# plt.bar(np.arange(256), np.transpose(hist_gray.astype(int))[0])
plt.vlines(np.arange(256), 0, hist_gray)
# plt.xlim([0, 255])
plt.ylim([0, np.max(hist_gray)])
fig.tight_layout(pad=0)
hist_gray_diag = get_diagram_as_image(fig)
cv2.imshow('Hisztogram (teljes)', hist_gray_diag)

# 16 elemű hisztogram
hist_gray2 = cv2.calcHist([img], [0], None, [16], [0, 256])

fig2 = plt.figure(figsize=(4, 2), dpi=100)
# plt.plot(hist_gray2)
plt.scatter(np.arange(16), hist_gray2, s=5)
# plt.bar(np.arange(16), np.transpose(hist_gray2.astype(int))[0])
# plt.vlines(np.arange(16), 0, hist_gray2)
# plt.xlim([0, 15])
plt.ylim([0, np.max(hist_gray2)])
hist_gray_diag2 = get_diagram_as_image(fig2)
cv2.imshow('Hisztogram (16 szint)', hist_gray_diag2)

cv2.waitKey(0)
