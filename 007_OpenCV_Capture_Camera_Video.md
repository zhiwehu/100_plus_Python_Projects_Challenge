# OpenCV Capture Camera Video
Use OpenCV to capture computer's camera and show the video.

## Requirements

1. It'll open the computer's camera and show the video in a window.
2. When you press "q" key it'll quit.

## What will we practice in this project?

- OpenCV: you need to install the `opencv-python` package via `pip install opencv-python` command in this project environment.
- while loop
- if condition
- keyboard check

## A reference code

```python
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

```

## Run the demo
Install the OpenCV:
```shell
pip install -r requirements.txt
```
Please save the Python as opencv_capture_camera_video.py and run it in console：

```
python opencv_capture_camera_video.py
```

----

# 使用OpenCV捕捉电脑摄像头视频

## 项目需求

- 运行程序会打开电脑摄像头，并显示捕捉到的视频
- 按`q`键会退出程序

## 项目练习

- 安装OpenCV，需要使用`pip install opencv-python`将OpenCV安装到项目环境中
- while循环
- if条件判断
- OpenCV窗口按键

## 项目参考代码

```python
import cv2

# 打开电脑摄像头
# 默认摄像头编号为0，如果你的电脑默认摄像头编程不为0，请使用其他数字
camera = cv2.VideoCapture(0)

# 重复去读取摄像头捕捉到的视频
while True:
    success, img = camera.read()
    # 如果捕捉成功，将捕捉到的视频显示在一个"Video"窗口中
    if success:
        cv2.imshow('Video', img)
    # 当在Video窗口上按下k键退出程序
    k = cv2.waitKey(1)
    if k == ord('q'):
        break

# 释放摄像头并关闭OpenCV打开的窗口
camera.release()
cv2.destroyAllWindows()

```

## 测试运行

Install OpenCV:
```shell
pip install -r requirements.txt
```
保存代码为opencv_capture_camera_video.py并运行：

```
python opencv_capture_camera_video.py
```
