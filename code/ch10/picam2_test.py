import time
from picamera2 import Picamera2, Preview

cam = Picamera2()

preview_config = cam.create_preview_configuration()
cam.configure(preview_config)
cam.start_preview(Preview.QTGL)

cam.start()
time.sleep(5)
cam.stop()
cam.stop_preview()