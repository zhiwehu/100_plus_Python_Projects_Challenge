import cv2

# Open your computer's default camera device.
# If your default camera ID is not 0, please use the correct ID
camera = cv2.VideoCapture(0)

# while loop to read the camera image
while True:
    success, img = camera.read()
    # if read success, it'll show the image in a "Video" window
    if success:
        cv2.imshow('Video', img)
    # get the key press, if you pressed "q" key it'll break the while loop
    k = cv2.waitKey(1)
    if k == ord('q'):
        break

# release your camera device and close the OpenCV windows
camera.release()
cv2.destroyAllWindows()
