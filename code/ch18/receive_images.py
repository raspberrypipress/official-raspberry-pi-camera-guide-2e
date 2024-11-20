import io
import os
import socket
import struct
from time import sleep
from PIL import Image
from datetime import datetime

# Start a socket listening for connections on
# 0.0.0.0:8000 (0.0.0.0 means all interfaces)
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8088))
server_socket.listen(0)

folder = "pictures"
os.makedirs(folder, exist_ok = True) # A folder to store images.

print("Ready for connections.")
try:
    while True:
        # Accept a connection and make a file-like object for it.
        conn, addr = server_socket.accept()
        stream = conn.makefile('rb')
        try:
            while True:
                # Read the image length as a 32-bit unsigned int.
                # If the length is zero, quit the loop.
                length = stream.read(struct.calcsize('<L'))
                image_len = struct.unpack('<L', length)[0]
                print(image_len)
                if not image_len:
                    break
                # Construct a stream to hold the image data and
                # read the image data from the connection.
                image_stream = io.BytesIO()
                image_stream.write(stream.read(image_len))
                # Rewind the stream, open it as an image with PIL
                # and save it in the image folder
                image_stream.seek(0)
                image = Image.open(image_stream)
                ts = str(datetime.now()) # get a timestamp
                image.save(os.path.join(folder, ts) + ".jpg")

        finally:
            conn.close()
except KeyboardInterrupt: # Press CTRL+C to quit. 
    print("Received CTRL+C, exiting.")
    server_socket.close()
