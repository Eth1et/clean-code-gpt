
import cv2

# load the haar cascade face detector from
print("[INFO] loading face detector...")
# detector = cv2.CascadeClassifier('haar/haarcascade_frontalface_default.xml')
detector = cv2.CascadeClassifier('haar/haarcascade_frontalface_alt2.xml')
# detector = cv2.CascadeClassifier('haar/haarcascade_upperbody.xml')
# detector = cv2.CascadeClassifier('haar/haarcascade_eye.xml')

# load the input image from disk and convert it to grayscale
# image = cv2.imread('captured.png', cv2.IMREAD_COLOR)
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

cap = cv2.VideoCapture(0)
if cap.isOpened():
    while True:
        ret, image = cap.read()
        if not ret:
            break

        # image = cv2.flip(image, 1)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # detect faces in the input image using the haar cascade face
        print("[INFO] performing face detection...")
        rects = detector.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
        print("[INFO] {} faces detected...".format(len(rects)))
        print(rects)

        # loop over the bounding boxes
        for (x, y, w, h) in rects:
            # draw the face bounding box on the image
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # show the output image
        cv2.imshow("Image", image)

        key = cv2.waitKey(1)
        if key == ord('q') or key == 27:
            cap.release()
            break


cv2.destroyAllWindows()
