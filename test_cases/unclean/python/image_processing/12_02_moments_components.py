
import numpy as np
import cv2

im_gray = cv2.imread('FrenchCardsShapes.png', cv2.IMREAD_GRAYSCALE)

threshVal = 100

if threshVal < 128:
    _, bw = cv2.threshold(im_gray, threshVal, 255, cv2.THRESH_BINARY_INV)
else:
    _, bw = cv2.threshold(im_gray, threshVal, 255, cv2.THRESH_BINARY)

moments, labels = cv2.connectedComponents(bw, None, 8, cv2.CV_16U)

print('Komponensek száma:', labels.max())

labels_norm = cv2.normalize(labels, None, 0, 65535, cv2.NORM_MINMAX, cv2.CV_16U)
cv2.imshow('Labels', labels_norm)
cv2.waitKey(0)

im_comp = np.ndarray(im_gray.shape, np.uint8)
for idx in range(1, labels.max() + 1):
    print('=======================================================================')
    print('Komponens címke:', idx)

    im_comp[:, :] = 0
    im_comp[labels == idx] = 255
    cv2.imshow('Komponens', im_comp)

    moments = cv2.moments(im_comp, True)
    print('Momentumok:', moments)
    print('Momentumok darabszáma:', len(moments))

    hu_moments = cv2.HuMoments(moments).flatten()
    print('Hu momentumok:', hu_moments)
    hu_moments_log = -np.sign(hu_moments) * np.log10(np.abs(hu_moments))
    print('Log transzformált Hu momentumok', hu_moments_log)

    key = cv2.waitKey(0)
    if key == ord('q'):
        break

cv2.destroyAllWindows()
