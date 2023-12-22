import cv2

imgray = cv2.imread('FrenchCardsShapes.png', cv2.IMREAD_GRAYSCALE)

threshVal = 100

if threshVal < 128:
    _, bw = cv2.threshold(imgray, threshVal, 255, cv2.THRESH_BINARY_INV)
else:
    _, bw = cv2.threshold(imgray, threshVal, 255, cv2.THRESH_BINARY)

retVal, labels = cv2.connectedComponents(bw, None, 8, cv2.CV_16U)

print('Kompenensek száma:', retVal)
labelsNorm = cv2.normalize(labels, None, 0, 65535, cv2.NORM_MINMAX, cv2.CV_16U)
cv2.imshow('Labels', labelsNorm)
cv2.waitKey(0)

cv2.destroyAllWindows()
