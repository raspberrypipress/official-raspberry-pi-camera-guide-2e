import io
import socket
import struct
import time
from picamera2 import Picamera2

# Connect a client socket to my_server:8088 (change my_server to 
# the hostname of your server)
client_socket = socket.socket()
client_socket.connect(('my_server', 8088))

# Make a file-like object out of the connection
connection = client_socket.makefile('wb')
try:
    cam = Picamera2()
    # Start a preview and let the camera warm up for 2 seconds
    cam.start()
    time.sleep(2)

    # Construct a stream to hold image data temporarily (we could
    # write it directly to connection but in this case we want the
    # size of each image first to keep our protocol simple).
    stream = io.BytesIO()
    for i in range(0, 15): # Capture 15 images
        stream = io.BytesIO()
        cam.capture_file(stream, format='jpeg')

        # Write the length of the capture to the stream and flush
        # to ensure it actually gets sent
        connection.write(struct.pack('<L', stream.tell()))
        connection.flush()
        # Rewind the stream and send the image data over the wire
        stream.seek(0)
        connection.write(stream.read())

        # Pause
        time.sleep(2)

        # Reset the stream for the next capture
        stream.seek(0)
        stream.truncate()

    # Write a length of zero to the stream to signal we're done
    connection.write(struct.pack('<L', 0))
finally:
    connection.close()
    client_socket.close()
