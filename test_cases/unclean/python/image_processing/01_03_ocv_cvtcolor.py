
# OpenCV2 képbeolvasás, színtér konverzió
# OpenCV online dokumentáció: https://docs.opencv.org/4.5.5/de/d25/imgproc_color_conversions.html

# OpenCV modul definíciók importálása
import cv2

# Színes kép beolvasása fájlból
imgc = cv2.imread('GolyoAlszik_rs.jpg', cv2.IMREAD_COLOR)
print('imgc:', imgc.shape)
cv2.imshow('color', imgc)

# Szürkeárnyalat
imgr = cv2.cvtColor(imgc, cv2.COLOR_BGR2GRAY)
cv2.imshow('grayscale', imgr)
print('grayscale:', imgr.shape)
cv2.waitKey(0)

# Szürkéből "színes"
imgc2 = cv2.cvtColor(imgr, cv2.COLOR_GRAY2BGR)
cv2.imshow('gray2bgr', imgc2)
print('gray2bgr:', imgc2.shape)
cv2.waitKey(0)

# Áttérés Lab színtérbe
# L: szürkeárnyalat
# a, b: kromatikusok (szín információ)
imgLab = cv2.cvtColor(imgc, cv2.COLOR_BGR2Lab)
print('imgLab:', imgLab.shape)
cv2.waitKey(0)

# Színcsatornákra bontás
L, a, b = cv2.split(imgLab)
cv2.imshow('L', L)
cv2.imshow('a', a)
cv2.imshow('b', b)
cv2.waitKey(0)
