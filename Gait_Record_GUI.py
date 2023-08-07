import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
import GUI_Functions as gui
from GUI_Visual_Resources import *

# Create tkinter window
win = tk.Tk()
win.title("HPE Recorder")

# Create the placeholder picture for the eventual live feed
im = Image.open('Building.jpg')
im = im.resize(photoDim)
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
cameraControlFrame.grid(row=0, column=4, sticky='n', padx=10, pady=10)
cameraControlFrame.config(padx=5, pady=5)

# Start button
startFeedButton = tk.Button(cameraControlFrame,
                            text="Start",
                            bg=startButtonColor,
                            command=lambda: gui.initiate_cam(placeholder_img=placeholder_img),
                            height=btnHeight, width=btnWidth)
startFeedButton.grid(row=0, column=0)

# Stop button
stopFeedButton = tk.Button(cameraControlFrame,
                           text="Stop",
                           bg=stopButtonColor,
                           command=gui.stop_cam,
                           height=btnHeight, width=btnWidth)
stopFeedButton.grid(row=0, column=1)

## Record Controls
# Label Frame
recordControlFrame = tk.LabelFrame(win, text='Recording Controls')
recordControlFrame.grid(row=0, column=5, sticky='n', padx=10, pady=10)
recordControlFrame.config(padx=5, pady=5)

# Filename textbox
filenameEntry = tk.Entry(recordControlFrame, bg=textboxColor)
filenameEntry.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Start button
startRecordButton = tk.Button(recordControlFrame,
                              text="Start",
                              bg=startButtonColor,
                              command=lambda: gui.start_recording(filenameEntry.get(), landmarks),
                              height=btnHeight, width=btnWidth)
startRecordButton.grid(row=0, column=0, sticky='e')

# Stop button
stopRecordButton = tk.Button(recordControlFrame,
                             text="Stop",
                             bg=stopButtonColor,
                             command=gui.stop_recording,
                             height=btnHeight, width=btnWidth)
stopRecordButton.grid(row=0, column=1, sticky='w')

# Landmark Label Frame
landmarkFrame = tk.LabelFrame(recordControlFrame, text='Landmarks')
landmarkFrame.grid(row=2, column=0, columnspan=2)
landmarkFrame.config(padx=5, pady=5)

# Right frame
rightFrame = tk.LabelFrame(landmarkFrame, text='Right')
rightFrame.grid(row=0, column=1, columnspan=1)
rightFrame.config(padx=5, pady=5)

# left frame
leftFrame = tk.LabelFrame(landmarkFrame, text='Left')
leftFrame.grid(row=0, column=0, columnspan=1)
leftFrame.config(padx=5, pady=5)

# Landmark list
landmarks = []
for i in range(0, 10):
    landmarks.append(tk.IntVar())

labels = ['Hip', 'Knee', 'Ankle', 'Heel', 'Foot']

# Landmark checkboxes
for i in range(0, 5):
    gui.create_checkboxes(rightFrame, labels[i], landmarks[i], i)

for i in range(5, 10):
    gui.create_checkboxes(leftFrame, labels[i-5], landmarks[i], i)

# GUI log Label Frame
logFrame = tk.LabelFrame(win, text='Log')
logFrame.grid(row=0, column=4, columnspan=1)
logFrame.config(padx=5, pady=5)

# GUI log Entry
logText = tk.StringVar()
logEntry = tk.Entry(logFrame, textvariable=logText, bg=textboxColor, state='disabled')
logEntry.grid(row=0, column=0)

# Landmark toggle
rawWorld = Image.open('button blue.png')
rawDefault = Image.open('button gray.png')
resizeWorld = rawWorld.resize((70, 40))
resizeDefault = rawDefault.resize((70, 40))

world = ImageTk.PhotoImage(resizeWorld)
default = ImageTk.PhotoImage(resizeDefault)

toggle = tk.Button(recordControlFrame, image=world, bd=0, command=lambda: gui.record_mode(toggle, world, default))
toggle.grid(row=4, column=0, columnspan=2)

defaultModeLabel = tk.Label(recordControlFrame, text='Default')
defaultModeLabel.grid(row=3, column=0)

worldModeLabel = tk.Label(recordControlFrame, text='World')
worldModeLabel.grid(row=3, column=1)

win.mainloop()
