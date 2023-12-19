
# OpenCV2 képbeolvasás, színtér konverzió
# OpenCV online dokumentáció: https://docs.opencv.org/4.1.2/de/d25/imgproc_color_conversions.html

# OpenCV modul definíciók importálása
import cv2

# Kép beolvasása fájlból
imgc = cv2.imread('GolyoAlszik_rs.jpg', cv2.IMREAD_COLOR)
cv2.imshow('color', imgc)

# Szürkeárnyalat
imgr = cv2.cvtColor(imgc, cv2.COLOR_BGR2GRAY)
cv2.imshow('grayscale', imgr)
cv2.waitKey(0)

# Színcsatornákra bontás és megjelenítés
b, g, r = cv2.split(imgc)
cv2.imshow('red', r)
cv2.imshow('green', g)
cv2.imshow('blue', b)
cv2.waitKey(0)

# Vörös csatorna nullázása és BGR kép előállítása
r[:, :] = 0
imgc2 = cv2.merge((b, g, r))
cv2.imshow('0,g,b', imgc2)
cv2.imwrite('Golyo_GB.jpg', imgc2)
cv2.waitKey(0)

# Színcsatorna ablakok bezárása
cv2.destroyWindow('red')
cv2.destroyWindow('green')
cv2.destroyWindow('blue')
cv2.destroyWindow('0,g,b')

# Áttérés Lab színtérbe
# L: szürkeárnyalat
# a, b: kromatikusok (szín információ)
imgLab = cv2.cvtColor(imgc, cv2.COLOR_BGR2Lab)
L, a, b = cv2.split(imgLab)
cv2.imshow('L', L)
cv2.imshow('a', a)
cv2.imshow('b', b)
cv2.waitKey(0)
