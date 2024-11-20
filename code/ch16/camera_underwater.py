from flask import Flask, render_template,request, redirect, url_for
import os, shutil
from picamera2 import Picamera2
from datetime import datetime
from subprocess import call

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

# Make the a subdirectory for images.
os.makedirs("static", exist_ok = True)

started = False # Make sure we only create the camera object once!
def start_camera():
    global started, cam, message
    if not started:
        cam = Picamera2()
        message = "Camera ready"
        started = True

def take_picture(): # take a picture
    
    global message

    t='{:%Y%m%d-%H%M%S}'.format(datetime.now())
    filename = 'snap'+t+'.jpg'
    # Take the photo
    cam.start_and_capture_file(f"static/{filename}", 
                               show_preview=False)
    # Copy it to the latest.jpg file
    shutil.copyfile(f"static/{filename}", 'static/latest.jpg')

    message = f"Took photo: {filename}"

@app.route('/', methods = ['POST','GET'])
def hello_world():

    global message

    start_camera() # Start up the camera

    if request.method == 'POST':

        if request.form['submit'] == 'Take Photo':
            take_picture()
        elif request.form['submit'] == 'Shutdown':
            call("sudo shutdown --poweroff now", shell=True)
        else:
            pass

    df = os.statvfs('/') # are we running out of disk space?
    df_size = df.f_frsize * df.f_blocks
    df_avail = df.f_frsize * df.f_bfree
    df_pc = round(100 -(100 * df_avail/df_size),1)

    # Display the web page template with our template variables
    return render_template('index.html', message=message,
                           df_pc=df_pc)

if __name__ == "__main__":

    # let's launch our site!
    app.run(host='0.0.0.0',port=5000,debug=True)
