
import cv2
import numpy as np
from matplotlib import pyplot as plt


img = cv2.imread('GolyoAlszik_rs.jpg', cv2.IMREAD_COLOR)
# img = cv2.imread('screen01_h.png', cv2.IMREAD_COLOR)
# img = cv2.imread('Sudoku_h.jpg', cv2.IMREAD_COLOR)
# img = cv2.imread('Tulipanok_01_800.jpg', cv2.IMREAD_COLOR)

cv2.imshow('img', img)

hist_b = cv2.calcHist([img], [0], None, [256], [0, 256])
hist_g = cv2.calcHist([img], [1], None, [256], [0, 256])
hist_r = cv2.calcHist([img], [2], None, [256], [0, 256])

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
hist_gray = cv2.calcHist([img_gray], [0], None, [256], [0, 256])

# Vörös színcsatorna hisztogram
fig = plt.figure(figsize=(4,2), dpi=100)
plt.vlines(np.arange(256), 0, hist_r, color='r')
# plt.xlim([0, 255])
plt.ylim([0, np.max(hist_r)])
plt.show()

# Zöld színcsatorna hisztogram
fig.clear()
plt.figure(figsize=(4,2), dpi=100)
plt.vlines(np.arange(256), 0, hist_g, color='g')
# plt.xlim([0, 255])
plt.ylim([0, np.max(hist_g)])
plt.show()

# Kék színcsatorna hisztogram
plt.figure(figsize=(4,2), dpi=100)
# plt.plot(hist_b, color='b')
plt.vlines(np.arange(256), 0, hist_b, color='b')
# plt.xlim([0, 255])
plt.ylim([0, np.max(hist_b)])
plt.show()

# RGB hisztogram
plt.figure(figsize=(4,2), dpi=100)
plt.plot(hist_b, color='b')
plt.plot(hist_g, color='g')
plt.plot(hist_r, color='r')
plt.plot(hist_gray, color='k')
# plt.xlim([0, 255])
plt.ylim([0, max(np.max(hist_b), np.max(hist_g), np.max(hist_r))])
plt.show()

print(len(hist_g[1:255]))

# RGB hisztogram a 0 és 255 elemek kihagyásával
plt.figure(figsize=(4,2), dpi=100)
plt.plot(hist_b[1:255], color='b')
plt.plot(hist_g[1:255], color='g')
plt.plot(hist_r[1:255], color='r')
plt.plot(hist_gray, color='k')
# plt.xlim([0, 255])
plt.ylim([0, max(np.max(hist_b[1:255]), np.max(hist_g[1:255]), np.max(hist_r[1:255]))])
plt.show()
