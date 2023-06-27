import tkinter as tk
import mediapipe as mp
import numpy as np
from PIL import Image, ImageTk
import GUI_Functions as gui

# initialize pose estimator
mp_drawing = mp.solutions.drawing_utils  # Purely for drawing the skeleton on the video
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(model_complexity=1, min_detection_confidence=0.5,
                    min_tracking_confidence=0.5)  # Parameters for the pose detection

# Create tkinter window
win = tk.Tk()
win.title("HPE Recorder")

# Create the placeholder picture for the eventual live feed
im = Image.open('Building.jpg')
im = im.resize((640, 480))
frame = np.asarray(im)
img = ImageTk.PhotoImage(Image.fromarray(frame))
placeholder_img = tk.Label(win)
placeholder_img.grid(row=0, column=0, columnspan=3, rowspan=3, pady=1, padx=10)
placeholder_img.configure(image=img)
placeholder_img.image = img
placeholder_img.update()

### Tkinter window elements
## Camera controls
# Label Frame
cameraControlFrame = tk.LabelFrame(win, text='Camera Controls')
cameraControlFrame.grid(row=0, column=4, sticky='n')
cameraControlFrame.config(padx=5, pady=5)

# Start button
startFeedButton = tk.Button(cameraControlFrame, text="Start", command=lambda: gui.initiate_cam(pose=pose,
                                                                                               mp_pose=mp_pose,
                                                                                               mp_drawing=mp_drawing,
                                                                                               placeholder_img=placeholder_img),
                            height=5, width=20)
startFeedButton.grid(row=0, column=4)
startFeedButton.config(height=5, width=10)

# Stop button
stopFeedButton = tk.Button(cameraControlFrame, text="Stop", command=gui.stop_cam, height=5, width=20)
stopFeedButton.grid(row=0, column=5)
stopFeedButton.config(height=5, width=10)

## Record Controls
# Label Frame
recordControlFrame = tk.LabelFrame(win, text='Recording Controls')
recordControlFrame.grid(row=1, column=4, sticky='n')
recordControlFrame.config(padx=5, pady=5)

# Start button
startFeedButton = tk.Button(recordControlFrame, text="Start", command=lambda: gui.initiate_cam(pose=pose,
                                                                                               mp_pose=mp_pose,
                                                                                               mp_drawing=mp_drawing,
                                                                                               placeholder_img=placeholder_img),
                            height=5, width=20)
startFeedButton.grid(row=0, column=4)
startFeedButton.config(height=5, width=10)

# Stop button
stopFeedButton = tk.Button(recordControlFrame, text="Stop", command=gui.stop_cam, height=5, width=20)
stopFeedButton.grid(row=0, column=5)
stopFeedButton.config(height=5, width=10)

win.mainloop()
