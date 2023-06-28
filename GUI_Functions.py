import cv2
import Camera_Extraction_Functions as cef
from PIL import Image, ImageTk
import time

global cam
#Camera feed functions
'''
Function: initiate_cam
The central driver of the overall program, this function handles starting the video feed
and has several calls to processing functions within it. A recording of numerical data
can only begin once the camera has been initialized.
'''
def initiate_cam(pose, mp_pose, mp_drawing, placeholder_img):
    global cam
    cam = cv2.VideoCapture(0)
    prevFrameTime = 0
    while cam.isOpened():
        ret, frame = cam.read()

        try:
            #Convert frame to correct color
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # process the frame for pose detection
            pose_results = pose.process(frame)
            # draw skeleton on the frame
            mp_drawing.draw_landmarks(frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Call data processing functions
            result = cef.extract_frame_data(pose_results)

            # Handle FPS
            newFrameTime = time.time()
            frame = cef.display_fps(frame, result, newFrameTime, prevFrameTime)
            prevFrameTime = newFrameTime

            # Update the image to tkinter
            img_update = ImageTk.PhotoImage(Image.fromarray(frame))
            placeholder_img.configure(image=img_update)
            placeholder_img.image = img_update
            placeholder_img.update()

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
