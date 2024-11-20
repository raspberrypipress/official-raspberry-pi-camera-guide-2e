# Import the necessary modules 
from datetime import datetime
from gpiozero import Button
from picamera2 import Picamera2, Preview
import time

b = Button(14)
cam = Picamera2()

# Configure the camera to capture in FHD with a VGA preview window.
config = cam.create_still_configuration(main={"size":(1920, 1080)},
                                        lores={"size":(640, 480)},
                                        display="lores")
cam.configure(config)

# Start the preview and the camera.
cam.start_preview(Preview.QTGL)
cam.start()

# Take a picture when the button is pressed.
def picture():
    time.sleep(.1) # Debounce (avoid counting one press as many)
    if b.is_pressed:
        # take the picture
        timestamp=datetime.now()
        cam.capture_file('pic'+str(timestamp)+'.jpg')
        print("Taken")

b.when_pressed = picture

try:
    print('Active') # Let users know we're still running
    time.sleep(1)
# If we detect CTRL+C, then quit the program
except KeyboardInterrupt:
    cam.stop()
    cam.stop_preview()
