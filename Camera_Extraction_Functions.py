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