
import numpy as np
import cv2

im = cv2.imread('FrenchCardsShapes.png')
im_orig = im.copy()
im_gray = 255 - cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(im_gray, 127, 255, 0)

contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

print('Hierarchia:')
print(hierarchy)

print('Kontúrok száma:', len(contours))
for cntrIdx in range(0, len(contours)):
    # Ha nem külső kontúr (van szülője), akkor kihagyjuk
    if hierarchy[0][cntrIdx][3] != -1:
        continue

    print('=======================================================================')
    print('Kontúr index:', cntrIdx)

    print(contours[cntrIdx].shape)
    moments = cv2.moments(contours[cntrIdx], True)
    print('Momentumok:', moments)
    print('Momentumok darabszáma:', len(moments))
    print('m00 indexelve:', moments['m00'])

    hu_moments = cv2.HuMoments(moments).flatten()
    print('Hu momentumok:', hu_moments)
    hu_moments_log = -np.sign(hu_moments) * np.log10(np.abs(hu_moments))
    print('Log transzformált Hu momentumok', hu_moments_log)

    cv2.drawContours(im, contours, cntrIdx, (0, 255, 0), 3)
    cv2.imshow('Contours', im)
    key = cv2.waitKey(0)
    if key == ord('q'):
        break

    im = im_orig.copy()

cv2.destroyAllWindows()
