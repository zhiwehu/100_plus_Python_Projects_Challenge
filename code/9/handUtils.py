import cv2
import mediapipe as mp

class HandDetector():
    def __init__(self):
        self.hand_detector = mp.solutions.hands.Hands()
        self.drawer = mp.solutions.drawing_utils

    def process(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.hands_data = self.hand_detector.process(img_rgb)
        if draw:
            if self.hands_data.multi_hand_landmarks:
                for handlms in self.hands_data.multi_hand_landmarks:
                    self.drawer.draw_landmarks(img, handlms, mp.solutions.hands.HAND_CONNECTIONS)

    def find_position(self, img):
        h, w, c = img.shape
        self.position = {'Left': {}, 'Right': {}}
        if self.hands_data.multi_hand_landmarks:
            i = 0
            for point in self.hands_data.multi_handedness:
                score = point.classification[0].score
                if score >= 0.8:
                    label = point.classification[0].label
                    hand_lms = self.hands_data.multi_hand_landmarks[i].landmark
                    for id, lm in enumerate(hand_lms):
                        x, y = int(lm.x * w), int(lm.y * h)
                        self.position[label][id] = (x, y)
                i = i + 1
        return self.position

    def fingers_count(self, hand='Left'):
        tips = [4, 8, 12, 16, 20]
        tip_data = {4:0, 8:0, 12:0, 16:0, 20:0}
        for tip in tips:
            ltp1 = self.position[hand].get(tip, None)
            ltp2 = self.position[hand].get(tip-2, None)
            if ltp1 and ltp2:
                if tip == 4:
                    if ltp1[0] > ltp2[0]:
                        if hand == 'Left':
                            tip_data[tip] = 1
                        else:
                            tip_data[tip] = 0
                    else:
                        if hand == 'Left':
                            tip_data[tip] = 0
                        else:
                            tip_data[tip] = 1
                else:
                    if ltp1[1] > ltp2[1]:
                        tip_data[tip] = 0
                    else:
                        tip_data[tip] = 1
        return list(tip_data.values()).count(1)