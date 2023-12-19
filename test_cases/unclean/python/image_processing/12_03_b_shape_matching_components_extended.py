
import numpy as np
import cv2

# https://www.pyimagesearch.com/2014/10/27/opencv-shape-descriptor-hu-moments-example/
# https://docs.opencv.org/4.5.5/d3/dc0/group__imgproc__shape.html#gaf2b97a230b51856d09a2d934b78c015f

component_selected = False
component_selection_string = 'Először válasszon referencia alakzatot a jobb egérgomb kattintással ' \
                             'az összehasonlításhoz!'
component_compare_string = 'Bal egérgomb: komponens választás az összehasonlításhoz.\n' \
                           'Jobb egérgomb: új referencia komponens választása.'


def initialize_component_shape(x, y):
    print('initialize_component_shape() called!')
    global labels, pattern_component

    print('=======================================================================')
    idx = labels[y, x]
    print('Kiválasztott komponens címke:', idx)
    if idx == 0:
        print('Háttér, nem jó!')
        return

    pattern_component[:, :] = 0
    pattern_component[labels == idx] = 255
    cv2.imshow('Minta', pattern_component)

    moments = cv2.moments(pattern_component, True)
    # print('Momentumok:', moments)
    # print('Momentumok darabszáma:', len(moments))

    hu_moments = cv2.HuMoments(moments).flatten()
    print('Hu momentumok:', hu_moments)
    hu_moments_log = -np.sign(hu_moments) * np.log10(np.abs(hu_moments))
    print('Log transzformált Hu momentumok', hu_moments_log)


def mouse_click(event, x, y, flags, param):
    # Globalis valtozok atvetele
    global bw, labels, stats, centroids
    global pattern_component
    global component_selected, component_selection_string, component_compare_string

    if event == cv2.EVENT_RBUTTONUP:
        initialize_component_shape(x, y)
        component_selected = True
        print(component_compare_string)
        return

    if event == cv2.EVENT_LBUTTONUP:
        if not component_selected:
            print(component_selection_string)
            return

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
        cv2.imshow('Minta', pattern_component)

        moments = cv2.moments(im_comp, True)
        # print('Momentumok:', moments)
        # print('Momentumok darabszáma:', len(moments))

        hu_moments = cv2.HuMoments(moments).flatten()
        print('Hu momentumok:', hu_moments)
        hu_moments_log = -np.sign(hu_moments) * np.log10(np.abs(hu_moments))
        print('Log transzformált Hu momentumok:', hu_moments_log)

        shape_match_value = cv2.matchShapes(pattern_component, im_comp, cv2.CONTOURS_MATCH_I2, 0)
        print('Alak hasonlóság:', shape_match_value * 1000)

        print(component_compare_string)


imgray = cv2.imread('shapes_crowns_arrows.png', cv2.IMREAD_GRAYSCALE)
# imgray = cv2.imread('FrenchCardsShapes.png', cv2.IMREAD_GRAYSCALE)
# imgray = cv2.imread('FCards_01_rs.jpg', cv2.IMREAD_GRAYSCALE)
# imgray = cv2.imread('FCards_02_rs.jpg', cv2.IMREAD_GRAYSCALE)
pattern_component = np.ndarray(imgray.shape, np.uint8)

threshVal = 150  # shapes_crowns_arrows.png esetén
# threshVal = 100  # FrenchCardShapes.png, FCards_01_rs.jpg, és FCards_02_rs.jpg esetén

if threshVal < 128:
    _, bw = cv2.threshold(imgray, threshVal, 255, cv2.THRESH_BINARY_INV)
else:
    _, bw = cv2.threshold(imgray, threshVal, 255, cv2.THRESH_BINARY)

retval, labels, stats, centroids = cv2.connectedComponentsWithStats(bw, None, 8, cv2.CV_16U)

print('Komponensek száma:', retval)
print(component_selection_string)

labels_norm = cv2.normalize(labels, None, 0, 65535, cv2.NORM_MINMAX, cv2.CV_16U)
_, labels_norm_thresh = cv2.threshold(labels_norm, 0, 65535, cv2.THRESH_BINARY)
cv2.imshow('Labels', labels_norm_thresh)
im_comp = np.ndarray(imgray.shape, np.uint8)
cv2.setMouseCallback('Labels', mouse_click)
cv2.waitKey(0)

cv2.destroyAllWindows()
