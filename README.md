# Computer Vision Gait Analysis Program (CVGAP)

1. [Description](#description)
2. [Set Up](#set-up)
3. [Overview](#overview)
4. [MediaPipe Human Pose Estimation](#mediapipe-human-pose-estimation)
    - [What is MediaPipe?](#what-is-mediapipe?)
    - [What is the output?](#what-is-the-output?)

## Description
This application is built for the purpose of measuring human gait parameters via an external webcam and [MediaPipe](https://github.com/google/mediapipe), a Google ai application that provides human pose estimation capabilities.

## Set Up
- Download the code via a zip file or cloning the repo using version control.
- Once on the local computer, open the project in an IDE (mainly used with [Spyder](https://www.spyder-ide.org/) or [Pycharm Community](https://www.jetbrains.com/pycharm/download/?section=windows))
- Install the required packages by entering the following line in the terminal
    >pip install -r requirements.txt
- Once the packages are installed, there should be no active compiler errors, and the program will run
- Plug in the external camera, if your system has an internal camera it may use that by default instead
    - The line to change which camera is used is located in [GUI_Functions.py](https://github.com/Eli-Bro/CV-Gait-Analysis-SU2023/blob/master/GUI_Functions.py)
    - 0 is the default, but this can be changed to 1 to move to the next camera found, and so on
      ```python
      cam = cv2.VideoCapture(0)
      ```

## Overview

## MediaPipe Human Pose Estimation
### What is MediaPipe?
The code responsible for conduction the human pose estimation is MediaPipe, an open source library of various tools and solutions for ai related tasks. Specifically for this program, the Pose Landmarker solution was used to map out human movement in real time.
- The main guide for the solution can be found [here](https://developers.google.com/mediapipe/solutions/vision/pose_landmarker)

### What is the output?
MediaPipe uses a system of 33 body landmarks ordered in the picture below. 
![landmark_map](https://github.com/Eli-Bro/CV-Gait-Analysis-SU2023/assets/78119596/b3658576-ff2e-4405-a896-31fda46dbaad)
*image credit: https://www.hackersrealm.net/post/realtime-human-pose-estimation-using-python*

These landmarks house 4 different pieces of information:
1. X coordinate
2. Y coordinate
3. Z coordinate
4. Visibility
