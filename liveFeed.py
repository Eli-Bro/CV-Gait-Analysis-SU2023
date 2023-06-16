import cv2
import mediapipe as mp

# initialize pose estimator
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

count = 0

cap = cv2.VideoCapture(0)
while cap.isOpened():
    # read frame
    count += 1
    _, frame = cap.read()
    try:
        # resize the frame for portrait video
        # frame = cv2.resize(frame, (350, 600))
        # convert to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # process the frame for pose detection
        pose_results = pose.process(frame_rgb)
        # print(pose_results.pose_landmarks)

        # draw skeleton on the frame
        mp_drawing.draw_landmarks(frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        print("ITERATION: " + str(count))
        if pose_results.pose_landmarks is not None:
            if pose_results.pose_landmarks.landmark[0] is not None:
                print(pose_results.pose_landmarks.landmark[0])
            else:
                print('Nose marker not visible')
        else:
            print('No visible landmarks')
        # display the frame
        cv2.imshow('Output', frame)
    except:
        break

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
