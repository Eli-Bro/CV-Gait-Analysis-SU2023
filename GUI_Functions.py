import cv2
import Camera_Extraction_Functions as cef
from PIL import Image, ImageTk
import time
import mediapipe as mp
from GUI_Visual_Resources import *
import tkinter as tk
from tkinter import messagebox
import os

global cam
global recordFlag
global startTime
global filename
global landmarks
global out
global worldMode
global frameCap

#Camera feed functions
'''
Function: initiate_cam
The central driver of the overall program, this function handles starting the video feed
and has several calls to processing functions within it. A recording of numerical data
can only begin once the camera has been initialized.
'''
def initiate_cam(placeholder_img):
    global cam
    # Updates record flag to false each time camera is started
    global recordFlag
    recordFlag = False
    global startTime
    pose, mp_pose, mp_drawing = initialize_pose_estimator()
    global worldMode
    worldMode = True
    global frameCap
    frameCap = True

    cam = cv2.VideoCapture(0)
    prevFrameTime = 0
    count = 0

    # TODO: Specific frequency set up
    # Set your desired frequency here (in Hz)
    frequency = 10.0  # Run 10 times per second (every 0.1 seconds)
    # Calculate delay from frequency
    delay = 1.0 / frequency
    # Time reference
    start_time = time.time()

    while cam.isOpened():
        ret, frame = cam.read()

        try:
            #Convert frame to correct color
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # process the frame for pose detection
            pose_results = pose.process(frame)
            # draw skeleton on the frame
            mp_drawing.draw_landmarks(frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Handle frame times
            newFrameTime = time.time()

            # Record if necessary
            if recordFlag:
                result = cef.extract_frame_data(pose_results, newFrameTime - startTime, worldMode, landmarks)
                cef.record_data(filename, result, landmarks)
                #===
                frameSave = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                out.write(frameSave)

                #===
                frame = indicate_recording(frame, count)
                count += 1

            # Draw all necessary info on frame
            frame = cef.display_fps(frame, newFrameTime, prevFrameTime)
            prevFrameTime = newFrameTime

            # Update the image to tkinter
            frame = cv2.resize(frame, photoDim)
            img_update = ImageTk.PhotoImage(Image.fromarray(frame))
            placeholder_img.configure(image=img_update)
            placeholder_img.image = img_update
            placeholder_img.update()

            #TODO: Used for testing
            if worldMode:
                print('X: ' + str(pose_results.pose_world_landmarks.landmark[0].x))
                print('Y: ' + str(pose_results.pose_world_landmarks.landmark[0].y))
            else:
                print('X: ' + str(pose_results.pose_landmarks.landmark[0].x))
                print('Y: ' + str(pose_results.pose_landmarks.landmark[0].y))

            if frameCap:
                # Compensate for the time that the codes took to run
                loop_duration = time.time() - start_time
                time.sleep(delay - loop_duration % delay)

        except Exception as e:
            print(e)

        # if not ret:
        #     print("failed to grab frame")
        #     break


'''
Function: stop_cam
Stops the active camera feed.
'''
def stop_cam():
    global cam
    cam.release()
    cv2.destroyAllWindows()
    print("Stopped!")


'''
Function: initialize_pose_estimator
Creates the tools needed to enact pose estimation via MediaPipe, including drawing utils
and parameters for detection confidence (default is 0.5 for all minimum values).
===
- model complexity: the specific prebuilt model used in the estimation process, in which:
    0 = light (fast, lower accuracy)
    1 = full (medium)
    2 = heavy (slow, higher accuracy)
===
'''
def initialize_pose_estimator():
    # initialize pose estimator
    mp_drawing = mp.solutions.drawing_utils  # Purely for drawing the skeleton on the video
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(model_complexity=1, min_detection_confidence=0.5,
                        min_tracking_confidence=0.5)  # Parameters for the pose detection
    return pose, mp_pose, mp_drawing


'''
Function: start_recording
Initiates the recording process, and sets the beginning time to 0 for the current recording.
'''
def start_recording(entryFile, landmarkList):
    global recordFlag
    global startTime
    global out
    startTime = time.time()
    if entryFile == '':
        #TODO: print to some log on the GUI
        messagebox.showwarning('Invalid File', 'Please provide a valid file name for the output location.')
        recordFlag = False
    else:
        global filename
        filename = entryFile
        recordFlag = True
        global landmarks
        landmarks = landmarkList

        # Set up video recording variables
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        videoName = os.path.splitext(filename)[0] + '.avi'
        out = cv2.VideoWriter(videoName, fourcc, 16.0, (640, 480))


'''
Function: stop_recording
Ends the current recording.
'''
def stop_recording():
    global recordFlag
    recordFlag = False


'''
Function: indicate_recording
Puts a red recording symbol on the video to show the user that the current
data is being recorded.
'''
def indicate_recording(frame, count):
    if count % 15 == 0:
        frame = cv2.circle(frame, (615, 20), 15, (255, 0, 0), -1)
    return frame


'''
Function: create_checkboxes
Creates the checkboxes for the different available landmarks, with all of them selected by default.
'''
def create_checkboxes(labelFrame, name, var, rowNum):
    checkBtn = tk.Checkbutton(labelFrame,
                              text=name,
                              variable=var,
                              onvalue=idxList[rowNum],
                              offvalue=-1,
                              state='active')
    checkBtn.grid(row=rowNum, column=0, sticky='w')
    checkBtn.select()


'''
Function: record_mode
Controls if the landmarks recorded are in the world coordinate mode or default mode,
with default mode being the one selected at initialization. The switch can only be triggered
once the camera has been initiated.
'''
def record_mode(toggle, worldPic, defPic):
    global worldMode
    if worldMode:
        worldMode = False
        toggle.config(image=defPic)
    else:
        worldMode = True
        toggle.config(image=worldPic)


'''
Function: toggle_frame_cap
Controls if the camera is capped at the specific amount of frames during recording,
primarily for keeping the same frequency of data for the machine learning model.
'''
def toggle_frame_cap(toggle, capPic, unlimPic):
    global frameCap
    if frameCap:
        frameCap = False
        toggle.config(image=unlimPic)
    else:
        frameCap = True
        toggle.config(image=capPic)
