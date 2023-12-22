
import cv2
import sys

cap = cv2.VideoCapture('sintel_trailer-480p.mp4')

if not cap.isOpened():
    print('Videófájl megnyitás sikertelen!')
    sys.exit(-1)

cap_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
cap_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
cap_fps = cap.get(cv2.CAP_PROP_FPS)

print('Videó méret: {}x{}'.format(cap_width, cap_height))
print('FPS:', cap_fps)

while True:
    # Beolvasás képkockánként
    ret, frame = cap.read()

    if not ret:
        break

    # Aktuális képkocka feldolgozása
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)

    # Eredmény megjelenítése
    cv2.imshow('frame', edges)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Erőforrás felszabadítása
cap.release()
cv2.destroyAllWindows()
