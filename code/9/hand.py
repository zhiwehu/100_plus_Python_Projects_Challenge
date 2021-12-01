import cv2
from handUtils import HandDetector

camera = cv2.VideoCapture(1)
hand_detector = HandDetector()

while True:
    success, img = camera.read()
    if success:
        img = cv2.flip(img, 1)
        h, w, c = img.shape
        hand_detector.process(img, draw=False)
        position = hand_detector.find_position(img)
        left_fingers = hand_detector.fingers_count('Left')
        print('左手: ', left_fingers)
        cv2.putText(img, str(left_fingers), (100, 150), cv2.FONT_HERSHEY_DUPLEX, 5, (0, 255, 0))
        right_fingers = hand_detector.fingers_count('Right')
        print('右手：', right_fingers)
        cv2.putText(img, str(right_fingers), (w-200, 150), cv2.FONT_HERSHEY_DUPLEX, 5, (255, 0, 0))
        cv2.imshow('Video', img)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
