
import numpy as np
import cv2

nparr = np.array([0, 50, 100, 125, 150, 200, 250], dtype=np.uint8)
print(nparr)

threshold, res1 = cv2.threshold(nparr, 125, 255, cv2.THRESH_BINARY)
print(res1.transpose())

threshold, res2 = cv2.threshold(nparr, 125, 255, cv2.THRESH_BINARY_INV)
print(res2.transpose())

threshold, res3 = cv2.threshold(nparr, 125, 255, cv2.THRESH_TRUNC)
print(res3.transpose())

threshold, res4 = cv2.threshold(nparr, 125, 255, cv2.THRESH_TOZERO)
print(res4.transpose())
cv2.thre

threshold, res5 = cv2.threshold(nparr, 125, 255, cv2.THRESH_TOZERO_INV)
print(res5.transpose())
