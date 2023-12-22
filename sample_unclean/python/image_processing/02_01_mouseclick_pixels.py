import cv2


def mouse_click(event, x, y, flags, param):
    # Globalis valtozo atvetele
    global image

    if event == cv2.EVENT_LBUTTONDOWN:
        # (x, y) színérték kiírása
        print('Pixel = ', image[y, x])
        # Ha 3 csatornás a kép
        if image.ndim == 3:
            print('R = ', image[y, x, 2])
        cv2.imshow('image', image)


image = cv2.imread('OpenCV-logo.png', cv2.IMREAD_COLOR)
# image = cv2.imread('OpenCV-logo.png', cv2.IMREAD_GRAYSCALE)
print('Kép indexelhető dimenziói:', image.ndim)
print('Kép mérete: ', image.shape)
print('Kép pixeltípusa: ', image.dtype)

cv2.imshow('image', image)
# Egerkezelo callback fuggveny beallitasa az ablakhoz
cv2.setMouseCallback('image', mouse_click)
# Kilepes billentyunyomasra
cv2.waitKey(0)

cv2.destroyAllWindows()
