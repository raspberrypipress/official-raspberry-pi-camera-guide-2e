import time
from picamera2 import Picamera2, Preview
from gpiozero import LED

cam = Picamera2()
flash_led = LED(17)

config = cam.create_still_configuration(main={"size":(1920, 1080)},
                                        lores={"size":(640, 480)},
                                        display="lores")
cam.configure(config)

cam.start_preview(Preview.QTGL)
cam.start()

flash_led.on()
time.sleep(1) # Give the camera time to adapt to the lighting. Not
              # needed if you set gain/exposure/colour explicitly.

cam.capture_file("test.jpg")
flash_led.off()
cam.stop()
cam.stop_preview()
