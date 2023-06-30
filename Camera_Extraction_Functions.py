import cv2
import csv
import os
from GUI_Visual_Resources import *

"""
Function: extract_frame_data
This is the main section for testing with the outputs from the pose detection.

To access the data use the following command (i is the index of the landmark you want)
>>> pose_results.pose_landmarks.landmark[i]

These landmarks have 4 pieces of data, accessed with these keys:

- x: the x coordinate, calculated by percentage
- y: the y coordinate, calculated by percentage
- z: the z coordinate
- visibility: the confidence score of how visible the landmark is
"""
def extract_frame_data(pose_results, frameTime, landmarkList):
    #Getting the hip, knee, and ankle points for each side (all info --> x,y,z,vis)
    frameData = [frameTime]
    if pose_results.pose_landmarks is not None:
        for ele in landmarkList:
            if ele.get() != -1:
                frameData.append(pose_results.pose_landmarks.landmark[ele.get()].x)
                frameData.append(pose_results.pose_landmarks.landmark[ele.get()].y)
                frameData.append(pose_results.pose_landmarks.landmark[ele.get()].z)
                frameData.append(pose_results.pose_landmarks.landmark[ele.get()].visibility)
    else:
        print('No visible landmarks')
        frameData = None
    return frameData


'''
Function: record_data
Takes in a list of data and writes it to a row of a csv file with a predefined name obtained 
via the GUI.
'''
def record_data(filename, data, landmarkList):
    if not os.path.isfile(filename):
        file = open(filename, 'w', newline='')
        with file:
            landmarkHeaders = { rHipIdx: 'Right Hip', rKneeIdx: 'Right Knee', rAnkleIdx: 'Right Ankle',
                                rHeelIdx: 'Right Heel', rFootIdx: 'Right Foot',
                                lHipIdx: 'Left Hip', lKneeIdx: 'Left Knee', lAnkleIdx: 'Left Ankle',
                                lHeelIdx: 'Left Heel', lFootIdx: 'Left Foot' }
            finalHeaders = ['Timestamp (s)']
            for ele in landmarkList:
                if ele.get() != -1:
                    finalHeaders.append(landmarkHeaders.get(ele.get()) + str(' x'))
                    finalHeaders.append(landmarkHeaders.get(ele.get()) + str(' y'))
                    finalHeaders.append(landmarkHeaders.get(ele.get()) + str(' z'))
                    finalHeaders.append(landmarkHeaders.get(ele.get()) + str(' vis'))

            writer = csv.writer(file)
            writer.writerow(finalHeaders)
            writer.writerow(data)
    else:
        file = open(filename, 'a', newline='')
        with file:
            writer = csv.writer(file)
            writer.writerow(data)


'''
Function: display_fps
Takes the difference between previous frame's time and the new frame's time, dividing 1 by that
difference, then displaying it in the top left corner of the camera feed.
'''
def display_fps(frame, newFrameTime, prevFrameTime):
    fps = 1 / (newFrameTime - prevFrameTime)

    # converting the fps into integer then string
    fps = str(int(fps))

    frame = cv2.putText(frame, 'FPS: ' + fps, org=(0, 25), fontScale=1,
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        color=(28, 252, 3), thickness=2)
    return frame
