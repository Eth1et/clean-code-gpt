# OpenCV2 képmátrix létrehozása, megjelenítés és fájlba mentése
# OpenCV online dokumentáció: https://docs.opencv.org/

# Modul definíciók importálása
import numpy as np
import cv2

# 320x200x3 méretű Numpy tömb létrehozása RGB színes képnek
img = np.ndarray((200, 320, 3), np.uint8)
# Feltöltés 192 (világosszürke) színnel
img.fill(192)
# Kör rajzolása az (50, 100) középponttal, 40 sugárral, vörös színnel, kitöltve
cv2.circle(img, (50, 100), 40, (0, 0, 192), -1)
# További rajzoló függvények:
#   https://docs.opencv.org/4.5.1/dc/da5/tutorial_py_drawing_functions.html

# Kép megjelenítése ablakban
cv2.imshow('image', img)
cv2.waitKey(0)

# Kép mentése fájlba
cv2.imwrite('ocv_test1_out.png', img)

# Összes ablak bezárása
cv2.destroyAllWindows()
