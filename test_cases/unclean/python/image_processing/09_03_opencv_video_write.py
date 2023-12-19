
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

# Define the codec and create VideoWriter object

# AVI
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('output.avi', fourcc, cap_fps, (cap_width, cap_height))

# MP4
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, cap_fps, (cap_width, cap_height))

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        break

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    frame = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    out.write(frame)

    # Display the resulting frame
    cv2.imshow('frame', edges)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
out.release()
cv2.destroyAllWindows()
