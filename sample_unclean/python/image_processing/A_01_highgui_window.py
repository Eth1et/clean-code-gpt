
import cv2

img = cv2.imread('OpenCV-logo.png')

cv2.imshow('imshow', img)
cv2.waitKey(0)
cv2.destroyWindow('imshow')

cv2.namedWindow('namedWindow')
cv2.waitKey(0)
cv2.imshow('namedWindow', img)

cv2.setWindowTitle('namedWindow', 'namedWindow title')
cv2.moveWindow('namedWindow', 200, 300)

print('Válassz célterületet! Bal egérgomb + mozgatás, majd SPACE vagy ENTER. Megszakítás a c billentyűvel!')
cv2.setWindowTitle('namedWindow', 'Valassz celteruletet!')
roi = cv2.selectROI('namedWindow', img)
print(roi)

cv2.destroyAllWindows()
