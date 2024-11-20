import socket
import time

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput

# Configure the camera
cam = Picamera2()
vid_config = cam.create_video_configuration({"size": (1280, 720)})
cam.configure(vid_config)
encoder = H264Encoder(1000000)
cam.encoders = encoder

# Listen on a socket for connections
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", 8888))
    sock.listen()

    # Each time through the loop, stream video until the 
    # client disconnects.
    try:
        while True:
            conn, addr = sock.accept()
            stream = conn.makefile("wb")
            encoder.output = FileOutput(stream)
            cam.start_encoder(encoder)
            cam.start()

            # Wait until the client disconnects
            try:
                while(conn.recv(512)):
                    pass
            except ConnectionResetError:
                pass

            print("Client disconnected.")
            cam.stop()
            cam.stop_encoder()
            conn.close()
    except KeyboardInterrupt: # Press CTRL+C to quit. 
        print("Received CTRL+C, exiting.")
        sock.close()
