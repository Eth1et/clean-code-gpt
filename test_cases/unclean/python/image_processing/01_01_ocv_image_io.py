
# OpenCV2 képbeolvasás, megjelenítés és tükrözés
# OpenCV online dokumentáció: https://docs.opencv.org/

# OpenCV modul definíciók importálása
import cv2

# OpenCV verziószám kiíratása
print('OpenCV verzió:', cv2.__version__)

# Kép beolvasása fájlból
img = cv2.imread('OpenCV-logo.png', cv2.IMREAD_COLOR)

# Képméret kiíratása konzolra
print(img.shape)

# Kép megjelenítése ablakban
cv2.imshow('image', img)
cv2.waitKey(0)

# Tükrözés a függőleges középtengelyre és megjelenítés
flipped = cv2.flip(img, 1)
cv2.imshow('image', flipped)
cv2.imwrite('OpenCV-logo-flipped.png', flipped)
cv2.waitKey(0)

# Tükrözés mindkét középtengelyre és megjelenítés
flipped2 = cv2.flip(img, -1)
cv2.imshow('image', flipped2)
cv2.waitKey(0)

# Összes ablak bezárása
cv2.destroyAllWindows()
