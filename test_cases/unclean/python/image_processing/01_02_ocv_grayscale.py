
# OpenCV2 képbeolvasás, szürkeárnyalatos konverzió
# OpenCV online dokumentáció: https://docs.opencv.org/

# OpenCV modul definíciók importálása
import cv2

# Kép beolvasása fájlból szürkeárnyalatosként
imgr = cv2.imread('OpenCV-logo.png', cv2.IMREAD_GRAYSCALE)

# Képméret kiíratása konzolra
print(imgr.shape)

# Kép megjelenítése ablakban
cv2.imshow('image', imgr)
cv2.waitKey(0)

# Kép beolvasása fájlból
imgc = cv2.imread('OpenCV-logo.png', cv2.IMREAD_COLOR)
print(imgc.shape)
imgr2 = cv2.cvtColor(imgc, cv2.COLOR_BGR2GRAY)
print(imgr2.shape)

# Kép megjelenítése ablakban
cv2.imshow('image', imgr2)
cv2.waitKey(0)