from datetime import datetime
from picamera2 import Picamera2
from ultralytics import YOLO
import time
import os
import cv2

# Initialize and configure the camera
cam = Picamera2()
config = cam.create_still_configuration(main={"size":(1280, 720), 
                                              "format": "RGB888"})
cam.align_configuration(config)
cam.configure(config)
cam.start()

# Download (if necessary) and load the YOLO11 model.
model = YOLO("yolo11n.pt")
names = model.names

threshold = .40 # Minimum confidence required to consider a match.
folder = "wildlife"
os.makedirs(folder, exist_ok = True) # A folder to store images.

def capture_objects(previous_classes):

    # Capture a frame from the camera.
    img = cam.capture_array()
    ts = str(datetime.now()) # get a timestamp

    # Run the inference on that image.
    results = model(img)

    # Add boxes and labels to the image.
    annotated = results[0].plot()

    # Get all the boxes (one for each object identified), the
    # class names, and confidence levels.
    boxes = results[0].boxes.xyxy.cpu().tolist()
    clss = results[0].boxes.cls.cpu().tolist()
    confs = results[0].boxes.conf.cpu().tolist()

    # Iterate over each object.
    if boxes is not None:
        if set(clss) == previous_classes:
            print("Scene is unchanged, not saving images.")
            return set(clss)

        for box, cls, conf in zip(boxes, clss, confs):
            if conf < threshold: # Is confidence under threshold?
                continue

            # Crop the image to the current object.
            crop = img[int(box[1]) : int(box[3]), 
                       int(box[0]) : int(box[2])]
            clssname = names[int(cls)] # get the object class name

            # Save each object in its class folder.
            clss_folder = os.path.join(folder, clssname)
            os.makedirs(clss_folder, exist_ok = True)
            filename = os.path.join(clss_folder, ts) + ".jpg"
            cv2.imwrite(filename, crop)

    # Save the original and the annotated version.
    image_basename = os.path.join(folder, ts) 
    cv2.imwrite(image_basename + ".jpg", img)
    cv2.imwrite(image_basename + "-annotated.jpg", annotated)

    return set(clss)

# Start the main loop
previous_classes = set()
try:
    while True:
        previous_classes = capture_objects(previous_classes)
        time.sleep(10)
except KeyboardInterrupt: # If you press CTRL+C, quit the program.
    print("Received CTRL+C, shutting down.")
    cam.stop()
