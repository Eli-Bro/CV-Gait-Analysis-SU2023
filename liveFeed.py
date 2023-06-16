import cv2
import mediapipe as mp

# initialize pose estimator
mp_drawing = mp.solutions.drawing_utils #Purely for drawing the skeleton on the video
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) #Parameters for the pose detection

#Iteration counter
count = 0

#Start the video stream, if an external camera is plugged in then it should use it be default
cap = cv2.VideoCapture(0)

#Loops as long as the stream is active
while cap.isOpened():
    # read frame
    count += 1
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

        #Testing the pose_results info
        print("ITERATION: " + str(count))
        if pose_results.pose_landmarks is not None:
            if pose_results.pose_landmarks.landmark[0] is not None:
                print(pose_results.pose_landmarks.landmark[0].x)
            else:
                print('Nose marker not visible')
        else:
            print('No visible landmarks')


        # display the frame
        cv2.imshow('Output', frame)
    except:
        break

    #The program exits once the user presses 'q'
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
