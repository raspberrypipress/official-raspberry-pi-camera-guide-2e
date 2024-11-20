from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
from gpiozero import Button, MotionSensor
from pygame import mixer
import time
import os
import pathlib

# Set up the devices
cam = Picamera2()
motion = MotionSensor(17)
doorSensor = Button(26)
letterbox = Button(19)
doorbell = Button(13)
mixer.init()

# Set up filenames
home = pathlib.Path.home()
vidfile = os.path.join(home, 'Desktop', 'motion.h264')
bellfile = os.path.join(home, 'smartdoor', 'doorbell.mp3')
picfile = os.path.join(home, 'Desktop', 'doorbell.jpg')
mixer.music.load(bellfile)

recording = False
photographing = False
def motionDetected():
    global recording, photographing
    while photographing:
        time.sleep(1) # wait until the photo is done
    print("Motion detected, video recording")
    recording = True
    cam.start_and_record_video(vidfile, show_preview=True)
    time.sleep(10)

def motionStopped():
    global recording
    # Make sure we're really recording, because the sensor may
    # have already been active when you started the program.
    if recording:
        print("Stopping video recording")
        cam.stop_recording()
        cam.stop_preview()
        recording = False

def doorOpen():
    print("Door open")

def doorClosed():
    print("Door closed")

def letterboxOpen():
    print("You've got mail!")

def doorbellPressed():
    global recording, photographing
    while recording: # Wait until the video is done
        time.sleep(1)
    mixer.music.play()
    photographing = True
    cam.start_and_capture_file(picfile)
    photographing = False
    print("Someone's at the door!")

# Attach our functions to GPIO Zero events
motion.when_motion = motionDetected
motion.when_no_motion = motionStopped
doorSensor.when_pressed = doorClosed
doorSensor.when_released = doorOpen
letterbox.when_released = letterboxOpen
doorbell.when_released = doorbellPressed

print("Smart door is smart")
# Loop forever allowing events to do their thing
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Smart door no longer smart")
