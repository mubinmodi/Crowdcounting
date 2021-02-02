# import the necessary packages
from api.controllers import LoginView
from object_detection.object_detector import SingleMotionDetector
from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import threading
import argparse
import datetime
import imutils
import time
import cv2

# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful when multiple browsers/tabs
# are viewing the stream)
outputFrame_camera1= None
outputFrame_camera2 = None
lock_1 = threading.Lock()
lock_2 = threading.Lock()
# initialize a flask object
app = Flask(__name__)
# initialize the video stream and allow the camera sensor to
# warmup
# vs = VideoStream(usePiCamera=1).start()

@app.route("/", )
def index():
    # return the rendered template
    return render_template("index.html")


@app.route("/track", )
def tracking_page():
    # return the rendered template
    return render_template("index.html")


def generate_camera1():
    # grab global references to the output frame and lock variables
    global outputFrame_camera1, lock_1
    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock_1:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrame_camera1 is None:
                continue
            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame_camera1)
            # ensure the frame was successfully encoded
            if not flag:
                continue
        # yield the output frame in the byte format
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encodedImage) + b'\r\n')

def generate_camera2():
    # grab global references to the output frame and lock variables
    global outputFrame_camera2, lock_2
    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock_2:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrame_camera2 is None:
                continue
            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame_camera2)
            # ensure the frame was successfully encoded
            if not flag:
                continue
        # yield the output frame in the byte format
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encodedImage) + b'\r\n')


@app.route("/video_feed")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate_camera1(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/video_feed_1")
def video_feed_1():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate_camera2(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


def detect_motion_camera1(frameCount):
    global vs, outputFrame_camera1, lock_1
    vs = VideoStream(0).start()
    time.sleep(2.0)
    md = SingleMotionDetector(accumWeight=0.1)
    total = 0
    while True:
        # read the next frame from the video stream, resize it,
        # convert the frame to grayscale, and blur it
        frame = vs.read()
        frame = imutils.resize(frame, width=400)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)
        # if the total number of frames has reached a sufficient
        # number to construct a reasonable background model, then
        # continue to process the frame
        if total > frameCount:
            # detect motion in the image
            motion = md.detect(gray)
            # check to see if motion was found in the frame
            if motion is not None:
                # unpack the tuple and draw the box surrounding the
                # "motion area" on the output frame
                (thresh, (minX, minY, maxX, maxY)) = motion
                cv2.rectangle(frame, (minX, minY), (maxX, maxY),
                              (0, 0, 255), 2)

        # update the background model and increment the total number
        # of frames read thus far
        md.update(gray)
        total += 1
        # acquire the lock, set the output frame, and release the
        # lock
        frame = cv2.rotate(frame.copy(), cv2.ROTATE_180)
        # grab the current timestamp and draw it on the frame
        timestamp = datetime.datetime.now()
        cv2.putText(frame, timestamp.strftime(
            "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        with lock_1:
            outputFrame_camera1 = frame


def detect_motion_camera2(frameCount):
    global vs_1, outputFrame_camera2, lock_2
    vs_1 = VideoStream('http://192.168.1.126:8080/video').start()
    time.sleep(2.0)
    md = SingleMotionDetector(accumWeight=0.1)
    total = 0
    while True:
        # read the next frame from the video stream, resize it,
        # convert the frame to grayscale, and blur it
        frame = vs_1.read()
        frame = imutils.resize(frame, width=400)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)
        # if the total number of frames has reached a sufficient
        # number to construct a reasonable background model, then
        # continue to process the frame
        if total > frameCount:
            # detect motion in the image
            motion = md.detect(gray)
            # check to see if motion was found in the frame
            if motion is not None:
                # unpack the tuple and draw the box surrounding the
                # "motion area" on the output frame
                (thresh, (minX, minY, maxX, maxY)) = motion
                cv2.rectangle(frame, (minX, minY), (maxX, maxY),
                              (0, 0, 255), 2)

        # update the background model and increment the total number
        # of frames read thus far
        md.update(gray)
        total += 1
        # acquire the lock, set the output frame, and release the
        # lock
        #frame = cv2.rotate(frame.copy(), cv2.ROTATE_180)
        # grab the current timestamp and draw it on the frame
        timestamp = datetime.datetime.now()
        cv2.putText(frame, timestamp.strftime(
            "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        with lock_2:
            outputFrame_camera2 = frame


# check to see if this is the main thread of execution
if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=True,
                    help="ip address of the device")
    ap.add_argument("-o", "--port", type=int, required=True,
                    help="ephemeral port number of the server (1024 to 65535)")
    ap.add_argument("-f", "--frame-count", type=int, default=32,
                    help="# of frames used to construct the background model")
    app.add_url_rule('/login', view_func=LoginView.as_view('counter'))

    args = vars(ap.parse_args())

    t = threading.Thread(target=detect_motion_camera1, args=(args["frame_count"],))
    t.daemon = True
    t.start()
    t1 = threading.Thread(target=detect_motion_camera2, args=(args["frame_count"],))
    t1.daemon = True
    t1.start()
    app.run(host=args["ip"], port=args["port"], debug=True, threaded=True, use_reloader=False)
# release the video stream pointer
vs.stop()
