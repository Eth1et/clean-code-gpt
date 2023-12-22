
import cv2
import numpy as np
from matplotlib import pyplot as plt

# Grafikon beállítások
fig = plt.figure(figsize=(6, 6), dpi=80)
# fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title('Inverzió LUT diagram')
fig.canvas.setWindowTitle('Inverzió LUT diagram')
plt.axis('equal')
plt.xlabel('Eredeti intenzitásérték')
plt.ylabel('Pont operáció eredménye')
plt.xlim([0, 255])
plt.ylim([0, 255])

# im = cv2.imread('SeaCliffBridge_3_800.jpg', cv2.IMREAD_GRAYSCALE)
im = cv2.imread('Sudoku_rs.jpg', cv2.IMREAD_GRAYSCALE)
cv2.imshow('Eredeti', im)

# Alappontok [0, 255] között, 8 bites, előjel nélküli egész számként
x = np.arange(0, 256, 1, np.uint8)

# Inverz készítés keresőtáblával
lut = np.arange(0, 256, 1, np.uint8)
lut = 255 - lut
im_inv = cv2.LUT(im, lut, None)
cv2.imshow('LUT', im_inv)

# Diagram rajzolás
plt.plot(x, x, 'g--', label='Eredeti')
plt.plot(x, lut, 'r-', label='Inverzió')
plt.legend()
# plt.savefig('04_01_c_inverse_lut_diagram.png', bbox_inches='tight')
plt.show()

cv2.destroyAllWindows()
