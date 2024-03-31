# import the necessary packages
import ctypes

import numpy as np
import imutils
from imutils.video import VideoStream
import threading
import multiprocessing
import argparse
import datetime
import core.utils as utils
from core.functions import *
import time
import cv2
import json
import tensorflow as tf
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession


physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

from core.config import cfg



saved_model_loaded = tf.saved_model.load('./checkpoints/yolov4-416')
infer = saved_model_loaded.signatures['serving_default']


class Camera(threading.Thread):

    def __init__(self, ip, name , lock, outputFrame_camera ,configured , cord1 = "0", cord2 = "0" ):
        threading.Thread.__init__(self)
        self.ip = ip
        self.lock = lock
        self.name = name
        self.outputFrame_camera = outputFrame_camera
        self.configured = configured
        self.cord1 = cord1
        self.cord2 = cord2
        self.currCount = 0
        self.prevCount = -1
        self.stop = False
        self.graphData = {}
      

    def generate_camera(self):
        # grab global references to the output frame and lock variables
        # global outputFrame_camera, lock
        # loop over frames from the output stream
        while not self.stop:
            # wait until the lock is acquired
            with self.lock:
                # check if the output frame is available, otherwise skip
                # the iteration of the loop
                if self.outputFrame_camera is None:
                    continue
                # encode the frame in JPEG format
                
                (flag, encodedImage) = cv2.imencode(".jpg", self.outputFrame_camera)



                # ensure the frame was successfully encoded
                if not flag:
                    continue
            # yield the output frame in the byte format
                    # yield the output frame in the byte format
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                   bytearray(encodedImage) + b'\r\n')
            # html = "<h1>78</h1>"
            #
            # yield (b'--frame\r\n' b'Content-Type: text/html\r\n\r\n' +
            #        html + b'\r\n')


        

        return
            
            # return self.outputFrame_camera

    def getCount(self):
        while not self.stop:
            # if self.currCount != self.prevCount:
            #     self.prevCount = self.currCount
                jsonData = json.dumps({"count" : self.currCount})
                yield (f"data:{jsonData}\n\n")
                time.sleep(0.33)
                
            
        return

    def graph(self) :
        while not self.stop:
            jsonData = json.dumps(self.graphData)
            yield (f"data:{jsonData}\n\n")
            time.sleep(1)
            
        return   


    def detect_motion_camera(self):

        # global outputFrame_camera, lock
        config = ConfigProto()
        config.gpu_options.allow_growth = True
        session = InteractiveSession(config=config)
        # self.ip = 'http://192.168.0.100:8080'
       
        vs_1 = VideoStream(f'http://{self.ip}:8080/video').start()
        time.sleep(2.0)
        total = 0
        frame_num = 0
        input_size = 416
        while not self.stop:
            # read the next frame from the video stream, resize it,
            # convert the frame to grayscale, and blur it

            frame = vs_1.read()
            # my chnge on below frame = imutils.resize(frame, width=400 ) => default
            frame = imutils.resize(frame, width=720 , height=480)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_num += 1
            dsize = (720,480);
            frame_size = frame.shape[:2]
            image_data = cv2.resize(frame, (input_size, input_size))
            image_data = image_data / 255.
            image_data = image_data[np.newaxis, ...].astype(np.float32)
            start_time = time.time()

            batch_data = tf.constant(image_data)
            pred_bbox = infer(batch_data)
            for key, value in pred_bbox.items():
                boxes = value[:, :, 0:4]
                pred_conf = value[:, :, 4:]

            boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
                boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
                scores=tf.reshape(pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
                max_output_size_per_class=50,
                max_total_size=50,
                iou_threshold=0.45,
                score_threshold=0.50
            )

            # format bounding boxes from normalized ymin, xmin, ymax, xmax ---> xmin, ymin, xmax, ymax
            frame = cv2.resize(frame, dsize)
            original_h, original_w, _ = frame.shape
            #print(original_h,original_w)
            
            
            if self.configured == True:
                frame = cv2.rectangle(frame, (int(self.cord1.get('x')),int(self.cord1.get('y'))), (int(self.cord2.get('x')),int(self.cord2.get('y'))), (0, 125, 252), 2)
            else:
                frame = cv2.rectangle(frame, (0,0), (720, 480), (0, 125, 252), 0)

            
            bboxes = utils.format_boxes(boxes.numpy()[0], original_h, original_w)

            pred_bbox = [bboxes, scores.numpy()[0], classes.numpy()[0], valid_detections.numpy()[0]]
            
            # read in all class names from config
            class_names = utils.read_class_names(cfg.YOLO.CLASSES)

            # by default allow all classes in .names file
            #allowed_classes = list(class_names.values())
            
            allowed_classes = ['person']   


            ####* before modification
            #counted_classes = count_objects(pred_bbox, by_class=True , allowed_classes=allowed_classes)

            #####* Modified Code below 
            cords = []
            if self.configured:
                cords = [
                self.cord1.get('x'),
                self.cord1.get('y'),
                self.cord2.get('x'),
                self.cord2.get('y')
                ]
            else:
                cords = [0,0,720,480]

           
            counted_classes = count_objects(pred_bbox,cords, by_class=True , allowed_classes=allowed_classes )
            
            timestamp = datetime.datetime.now()
            # loop through dict and print
            if counted_classes:
                for key, value in counted_classes.items():
                    print("Number of {}s: {}".format(key, value))

                    self.currCount = value
                    self.graphData = {
                        "time" : timestamp.strftime("%H:%M:%S") ,
                        "value" : value
                    }
            else:
                self.currCount = 0
                self.graphData = {
                       "time" : timestamp.strftime("%H:%M:%S") ,
                        "value" : 0
                }
            
            
            # frame = cv2.rotate(frame.copy(), cv2.ROTATE_180)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            image = utils.draw_bbox(frame, pred_bbox, False, counted_classes, allowed_classes=allowed_classes,
                                    read_plate=False)

           
            cv2.putText(frame, timestamp.strftime(
                "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

            with self.lock:
                self.outputFrame_camera = image

            fps = 1.0 / (time.time() - start_time)
            # print("FPS: %.2f" % fps)

        return

    def get_id(self):

        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id


            


    def terminate(self):
        self.stop = True
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
                                                         ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')
    #raise Exception("Thread terminated")

 

    def run(self):
        
        self.detect_motion_camera();