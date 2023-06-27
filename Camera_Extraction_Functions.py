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
    #using nose landmark for now since it is easiest
    if pose_results.pose_landmarks is not None:
        if pose_results.pose_landmarks.landmark[25] is not None and pose_results.pose_landmarks.landmark[26] is not None:
            result = pose_results.pose_landmarks.landmark[25].x
            print('x loc: ' + str(result))
            # print('visibility: ' + str(pose_results.pose_landmarks.landmark[32].visibility))
        else:
            print('Nose marker not visible')
    else:
        print('No visible landmarks')
    return result

def display_fps(frame, data, newFrameTime, prevFrameTime):
    fps = 1 / (newFrameTime - prevFrameTime)

    # converting the fps into integer then string
    fps = str(int(fps))

    frame = cv2.putText(frame, 'FPS: ' + fps, org=(0, 25), fontScale=1,
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        color=(28, 252, 3), thickness=2)
    return frame
