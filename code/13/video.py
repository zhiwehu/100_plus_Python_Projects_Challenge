import cv2

camera = cv2.VideoCapture(1)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    success, frame = camera.read()
    if success:
        cv2.imshow("Video", frame)
        key = cv2.waitKey(1)
        if key == ord("q"):
            break

camera.release()
cv2.destroyAllWindows()
