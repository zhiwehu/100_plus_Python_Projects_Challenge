import cv2
from handUtils import HandDetector

camera = cv2.VideoCapture(1)
hand_detector = HandDetector()

while True:
    success, img = camera.read()
    if success:
        img = cv2.flip(img, 1)
        hand_detector.process(img, draw=False)
        position = hand_detector.find_position(img)
        left_finger = position['Left'].get(8, None)
        if left_finger:
            cv2.circle(img, (left_finger[0], left_finger[1]),10, (0, 0, 255), cv2.FILLED)
        right_finger = position['Right'].get(8, None)
        if right_finger:
            cv2.circle(img, (right_finger[0], right_finger[1]),10, (0, 255, 0), cv2.FILLED)
        cv2.imshow('Video', img)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
