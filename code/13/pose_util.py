import cv2
import mediapipe as mp

from utils import find_angle

class PoseDetector():
    def __init__(self):
        self.pose = mp.solutions.pose.Pose()
        self.draw_util = mp.solutions.drawing_utils

    def detect(self, img, draw=True):
        self.positions = []
        results = self.pose.process(img)
        if results and results.pose_landmarks:
            if draw:
                self.draw_util.draw_landmarks(img, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)
        
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.positions.append([id, cx, cy])
    
    def get_angle(self, img, p1, p2, p3, draw=True):
        '''
        获取人体姿势中3个点p1-p2-p3的角度
        :param img: 一帧图像
        :param p1: 第1个点
        :param p2: 第2个点
        :param p3: 第3个点
        :param draw: 是否画出3个点的连接图
        :return: 角度
        '''
        angle = 0
        if self.positions:
            x1, y1 = self.positions[p1][1],self.positions[p1][2]
            x2, y2 = self.positions[p2][1],self.positions[p2][2]
            x3, y3 = self.positions[p3][1],self.positions[p3][2]
            angle = find_angle((x1, y1), (x2, y2), (x3, y3))

            if draw:
                cv2.circle(img, (x1, y1), 8, (0, 255, 255), cv2.FILLED)
                cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (x3, y3), 8, (0, 255, 255), cv2.FILLED)
                cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255, 3))
                cv2.line(img, (x2, y2), (x3, y3), (255, 255, 255, 3))
                cv2.putText(img, str(angle), (x2-50, y2+50),cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 2)

        return angle