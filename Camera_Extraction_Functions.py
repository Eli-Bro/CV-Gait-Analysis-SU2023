import cv2

"""
Function: extract_frame_data
This is the main section for testing with the outputs from the pose detection.

To access the data use the following command (i is the index of the landmark you want)
>> pose_results.pose_landmarks.landmark[i]

These landmarks have 4 pieces of data, accessed with these keys:

- x: the x coordinate, calculated by percentage
- y: the y coordinate, calculated by percentage
- z: the z coordinate
- visibility: the confidence score of how visible the landmark is
"""
def extract_frame_data(pose_results):
    #Getting the hip, knee, and ankle points for each side (all info --> x,y,z,vis)
    landmark_indexes = [24, 26, 28, 23, 25, 27]
    frameData = []
    if pose_results.pose_landmarks is not None:
        for ele in landmark_indexes:
            frameData.append(pose_results.pose_landmarks.landmark[ele].x)
            frameData.append(pose_results.pose_landmarks.landmark[ele].y)
            frameData.append(pose_results.pose_landmarks.landmark[ele].z)
            frameData.append(pose_results.pose_landmarks.landmark[ele].visibility)
        # print(frameData)
        print(pose_results.pose_landmarks.landmark[26].visibility)
    else:
        print('No visible landmarks')
        frameData = None
    return frameData

def display_fps(frame, data, newFrameTime, prevFrameTime):
    fps = 1 / (newFrameTime - prevFrameTime)

    # converting the fps into integer then string
    fps = str(int(fps))

    frame = cv2.putText(frame, 'FPS: ' + fps, org=(0, 25), fontScale=1,
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        color=(28, 252, 3), thickness=2)
    return frame
