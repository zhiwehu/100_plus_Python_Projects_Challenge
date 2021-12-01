# OpenCV Capture Camera Video
Use OpenCV and MediaPipe to detect hands and count fingers.
This project is based on the previous one: https://github.com/zhiwehu/100_plus_Python_Projects_Challenge/blob/main/008_OpenCV_MediaPipe_hand_detection.md
https://google.github.io/mediapipe/solutions/hands

## Requirements

1. It'll open the computer's camera and show the video in a window.
2. It'll show how many fingers of both hands you put on the screen.
3. When you press "q" key it'll quit.

## What will we practice in this project?

- OpenCV: you need to install the `opencv-python` package via `pip install opencv-python` command in this project environment.
- while loop
- MediaPipe hands solution
- list and dict usage
- if condition

## A reference code

### handUtils.py
```python
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

```

### hand.py
```python
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

```

## Run the demo
Install the OpenCV & MediaPipe:
```shell
pip install opencv-python mediapipe
```
Please save the 2 Python files and run it：

```
python hand.py
```

----

# 使用OpenCV和MediaPipe进行手势识别

## 项目需求

- 运行程序会打开电脑摄像头，并显示捕捉到的视频
- 视频窗口上会显示左右手各伸出了多少手指头
- 按`q`键会退出程序

## 项目练习

- 安装OpenCV，需要使用`pip install opencv-python mediapipe`将OpenCV和MediaPipe安装到项目环境中
- MediaPipe手势识别：https://google.github.io/mediapipe/solutions/hands
- list 和 dict
- while 循环
- 条件语句

## 项目参考代码

### handUtils.py
```python
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

```

### hand.py
```python
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

```

## 测试运行

Install OpenCV and MediaPipe:
```shell
pip install opencv-python mediapipe
```
保存上面2个代码并运行：

```
python hand.py
```
