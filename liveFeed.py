import cv2
import mediapipe as mp

"""
Function: extract_frame_data
This is the main section for testing with the outputs from the pose detection.

To access the data use the following command (i is the index of the landmark you want)
> pose_results.pose_landmarks.landmark[i]

These landmarks have 4 pieces of data, accessed with these keys:

- x: the x coordinate, calculated by percentage
- y: the y coordinate, calculated by percentage
- z: the z coordinate
- visibility: the confidence score of how visible the landmark is
"""
def extract_frame_data(pose_results):
    #using nose landmark for now since it is easiest
    if pose_results.pose_landmarks is not None:
        if pose_results.pose_landmarks.landmark[0] is not None:
            print('x: ' + str(pose_results.pose_landmarks.landmark[0].x))
        else:
            print('Nose marker not visible')
    else:
        print('No visible landmarks')


# initialize pose estimator
mp_drawing = mp.solutions.drawing_utils #Purely for drawing the skeleton on the video
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) #Parameters for the pose detection

#Start the video stream, if an external camera is plugged in then it should use it be default
cap = cv2.VideoCapture(0)

#Loops as long as the stream is active
while cap.isOpened():
    # read frame
    _, frame = cap.read()

    try:
        # resize the frame if needed
        # frame = cv2.resize(frame, (350, 600))
        # convert to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # process the frame for pose detection
        pose_results = pose.process(frame_rgb)

        # draw skeleton on the frame
        mp_drawing.draw_landmarks(frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        extract_frame_data(pose_results)

        # display the frame
        cv2.imshow('Output', frame)
    except:
        break

    #The program exits once the user presses 'q'
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
