from gpiozero import MotionSensor
from picamera2 import Picamera2
from datetime import datetime
import time

sensor = MotionSensor(14)
cam = Picamera2()
cam.start()

time_format = "%H.%M.%S_%Y-%m-%d.jpg"
while True:
    sensor.wait_for_motion()
    filename = datetime.now().strftime(time_format)
    cam.capture_file(filename)
    print(f"Captured {filename}")
    time.sleep(5)
