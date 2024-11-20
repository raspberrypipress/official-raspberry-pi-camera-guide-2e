import time
from picamera2 import Picamera2, Preview
from gpiozero import LED

cam = Picamera2()
config = cam.create_still_configuration(main={"size":(1920, 1080)},
                                        lores={"size":(640, 480)},
                                        display="lores")
cam.configure(config)
cam.set_controls({"ExposureTime": 3000000,
                  "FrameRate": 1 / 6,
                  "AnalogueGain": 800 / 100
                  })

cam.start_preview(Preview.QTGL)
cam.start()

# Give the camera a good long time to set gains and
# measure AWB (you may wish to use fixed AWB instead)
time.sleep(30)

# Finally, capture an image with a 6s exposure. Due
# to mode switching on the still port, this will take
# longer than six seconds
cam.capture_file("dark.jpg")
cam.stop()
cam.stop_preview()
