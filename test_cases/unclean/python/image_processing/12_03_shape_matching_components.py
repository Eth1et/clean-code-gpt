import numpy as np
import cv2

# https://www.pyimagesearch.com/2014/10/27/opencv-shape-descriptor-hu-moments-example/
# https://docs.opencv.org/4.5.5/d3/dc0/group__imgproc__shape.html#gaf2b97a230b51856d09a2d934b78c015f


def mouse_click(event, x, y, flags, param):
    # Globalis valtozok atvetele
    global bw, labels, stats, centroids

    if event == cv2.EVENT_LBUTTONDOWN:
        print('=======================================================================')
        idx = labels[y, x]
        print('Komponens címke:', idx)
        if idx == 0:
            print('Háttér!')
            return

        print(stats[idx])
        print('Befoglaló téglalap bal felső sarka: ({}, {})'.format(stats[idx][cv2.CC_STAT_LEFT],
                                                                    stats[idx][cv2.CC_STAT_TOP]))
        print('Befoglaló téglalap mérete: {}x{}'.format(stats[idx][cv2.CC_STAT_WIDTH],
                                                        stats[idx][cv2.CC_STAT_HEIGHT]))
        print('Komponens területe pixelben: {}'.format(stats[idx][cv2.CC_STAT_AREA]))
        print('Komponens súlypontja:', centroids[idx])

        im_comp[:, :] = 0
        im_comp[labels == idx] = 255
        cv2.imshow('Komponens', im_comp)

        moments = cv2.moments(im_comp, True)
        print('Momentumok:', moments)
        print('Momentumok darabszáma:', len(moments))

        hu_moments = cv2.HuMoments(moments).flatten()
        print('Hu momentumok:', hu_moments)
        hu_moments_log = -np.sign(hu_moments) * np.log10(np.abs(hu_moments))
        print('Log transzformált Hu momentumok:', hu_moments_log)


imgray = cv2.imread('FCards_01_rs.jpg', cv2.IMREAD_GRAYSCALE)

threshVal = 100

if threshVal < 128:
    _, bw = cv2.threshold(imgray, threshVal, 255, cv2.THRESH_BINARY_INV)
else:
    _, bw = cv2.threshold(imgray, threshVal, 255, cv2.THRESH_BINARY)

retval, labels, stats, centroids = cv2.connectedComponentsWithStats(bw, None, 8, cv2.CV_16U)

print('Komponensek száma:', retval)
print('Kattintson egy fehér komponensre a jellemzők számításához!')

labelsNorm = cv2.normalize(labels, None, 0, 65535, cv2.NORM_MINMAX, cv2.CV_16U)
_, labelsNormThresh = cv2.threshold(labelsNorm, 0, 65535, cv2.THRESH_BINARY)
cv2.imshow('Labels', labelsNormThresh)
im_comp = np.ndarray(imgray.shape, np.uint8)
cv2.setMouseCallback('Labels', mouse_click)
cv2.waitKey(0)

cv2.destroyAllWindows()
