# Computer Vision Gait Recording Program (CVGRP)


- [Computer Vision Gait Recording Program (CVGRP)](#computer-vision-gait-recording-program-cvgrp)
  - [Description](#description)
  - [Set Up](#set-up)
  - [Overview](#overview)
    - [How to Use](#how-to-use)
    - [Program Output](#program-output)
  - [MediaPipe Human Pose Estimation](#mediapipe-human-pose-estimation)
    - [What is MediaPipe?](#what-is-mediapipe)
    - [What is the output?](#what-is-the-output)
      - [Default](#default)
      - [World](#world)

## Description
This application is built for the purpose of measuring human gait parameters via an external webcam and [MediaPipe](https://github.com/google/mediapipe), a Google AI application that provides human pose estimation capabilities.

## Set Up
- Download the code via a zip file or cloning the repo using version control.
- Once on the local computer, open the project in an IDE (mainly used with [Spyder](https://www.spyder-ide.org/) or [Pycharm Community](https://www.jetbrains.com/pycharm/download/?section=windows))
- Install the required packages by entering the following line in the terminal
  ```python console
  pip install -r requirements.txt
  ```
- If there issues with the pip installation, such as the **access denied** message, try the following command then reset the terminal
  ```python console
  pip install --upgrade pip --user
  ```
- Once the packages are installed, there should be no active compiler errors, and the program will run
- Plug in the external camera, if your system has an internal camera it may use that by default instead
    - The line to change which camera is used is located in [GUI_Functions.py](https://github.com/Eli-Bro/CV-Gait-Analysis-SU2023/blob/master/GUI_Functions.py)
    - 0 is the default, but this can be changed to 1 to move to the next camera found, and so on
      ```python
      cam = cv2.VideoCapture(0)
      ```

## Overview
### How to Use
Essentially, the general workflow of the program will be as follows:
1. Run the [Gait_Record_GUI.py](https://github.com/Eli-Bro/CV-Gait-Analysis-SU2023/blob/master/Gait_Record_GUI.py) file to start the front panel.
2. Start the camera feed.
3. Assign an output file name.
4. Choose which landmarks to record via the checkboxes.
5. Begin recording, upon stopping the video and csv file will be saved under the working directory.

### Program Output
The final output from a recording session of CVGRP is:
1. An avi file of the session with the MediaPipe landmarks present.
2. A csv containing the ```x```, ```y```, ```z``` coordinates of the selected landmarks as well as the ```visibility``` score of each landmark.
    - The first column in the csv will be the timestamp.

## MediaPipe Human Pose Estimation
### What is MediaPipe?
The code responsible for conduction the human pose estimation is MediaPipe, an open source library of various tools and solutions for AI related tasks. Specifically for this program, the Pose Landmarker solution was used to map out human movement in real time.
- The main guide for the solution can be found [here](https://developers.google.com/mediapipe/solutions/vision/pose_landmarker).
- MediaPipe can be imported into projects easily, simply using ```import mediapipe```.

Once imported, a few settings need to be configured before using the tool in the project. This is primarily handled by the ```initialize_pose_estimator()``` function in [GUI_Functions.py](https://github.com/Eli-Bro/CV-Gait-Analysis-SU2023/blob/master/GUI_Functions.py).

```python
def initialize_pose_estimator():
    # initialize pose estimator
    mp_drawing = mp.solutions.drawing_utils  # Purely for drawing the skeleton on the video
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(model_complexity=1, min_detection_confidence=0.5,
                        min_tracking_confidence=0.5)  # Parameters for the pose detection
    return pose, mp_pose, mp_drawing
```
- ```mp_drawing``` is primarily there to draw the skeleton on the frame so that the tracking can be visually observed on the camera feed.
- ```mp_pose``` is the specific solution used in this project.
- ```pose``` is the pose estimator object, and houses the previously mentioned settings. 
  - *model_complexity* has three different levels: light (0), full (1), and heavy (2). The higher you go, the more accurate the estimation gets, but the slower it becomes.
  - *min_detection_confidence* and *min_tracking_confidence* refer to thresholds for the tool to refer to when drawing and estimating the landmarks, they are set at 0.5 as default.  

### What is the output?
MediaPipe uses a system of 33 body landmarks ordered in the picture below. 
![landmark_map](https://github.com/Eli-Bro/CV-Gait-Analysis-SU2023/assets/78119596/9afd87d4-9566-4b3f-a360-752a07b815e9)
*image credit: https://www.hackersrealm.net/post/realtime-human-pose-estimation-using-python*

These landmarks house 4 different pieces of information:
>1. X coordinate
>2. Y coordinate
>3. Z coordinate
>4. Visibility

To access this data, you will need to have a result from an already completed estimation conducted on a frame. In this case, the results variable is called ```pose_results```. 
```python
#Default
pose_results.pose_landmarks.landmark[0].x
#World
pose_results.pose_world_landmarks.landmark[0].x
```
The ```0``` refers to the landmark number found on the [map](#what-is-the-output), and the ```x``` is the desired info, meaning it can be replaced by ```y```, ```z```, or ```visibility```. The implementation of these landmarks can be found in the ```extract_frame_data()``` function within [Camera_Extraction_Functions.py](https://github.com/Eli-Bro/CV-Gait-Analysis-SU2023/blob/master/Camera_Extraction_Functions.py). 

The scale and reference point of these landmarks differs based on what mode is selected. There are two modes: *default* and *world*.

#### Default
- Reference Point
  - Default mode uses the top left of the camera frame as the origin.
- X coordinate
  - The right edge of the camera frame is 1.0, and the left edge is 0.0.
- Y coordinate
  - The bottom edge of the camera frame is 1.0, and the top edge is 0.0.
- Coordinate Scale
  - The numerical values are a percentage of total distance and are unitless. For example, if a particular landmark was in the very middle of the camera frame, the (x, y) coordinates would be **(0.5, 0.5)**. But if one were to move the point closer to the bottom right corner, both coordinates would increase to a point such as **(0.75, 0.75)**.
- Z coordinate
  - The z coordinate is an estimated value, using a reference point located at the center in between the two hip landmarks. It then interprets distances between this point and the camera to be negative, and distance beyond this point away from the camera to be positive.
  - However, since this value is estimated and not measured in the same method as the x and y, use caution when integrating it in projects (not recommended as of July 2023).
- Visibility
  - Refers to the ability of the AI tool to detect the landmark. MediaPipe will attempt to provide data as much as possible, even when visibility is low. Thus, landmarks will be estimated even if they are off-screen, as long as a sufficient number of other landmarks are present. If not enough landmarks are present, then the tool will not provide any coordinate information. Though if the current number of detected landmarks meets the threshold, then all landmarks will be estimated and given their own visibility scores, meaning the landmarks off-screen will have a very low score in comparison to those on screen. The scale is 0 to 1, and experiences the greatest drops when the landmarker is off-screen or obstructed by an object or another part of the body.

#### World
- Reference Point
  - The center point between the two hip landmarks.
- X coordinate
  - In front of the hips is positive, behind the hips is negative.
- Y coordinate
  - Below the hips is positive, above the hips is negative.
- Coordinate Scale
  - The distance (in meters) from this center point to the particular landmarker.
- Z coordinate
  - Acts the same as [default](#default) mode.
- Visibility
  - Acts the same as [default](#default) mode. 

