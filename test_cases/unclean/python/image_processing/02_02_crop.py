import cv2

image = cv2.imread('GolyoAlszik_rs.jpg')

# Képkivágás; sor és oszlop tartomány megadása
cropped = image[82:172, 396:486]
# Kivágott rész képbe másolása, új helyre
image[10:100, 20:110] = cropped

cv2.imshow('image', image)
cv2.imshow('cropped', cropped)

cv2.waitKey(0)
