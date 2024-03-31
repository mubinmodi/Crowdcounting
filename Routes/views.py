
from time import sleep
from flask import Blueprint, render_template, Response , request, flash, redirect, session, jsonify
import requests
# from ..Models.user import User
from Database.mongodb import mongo
from werkzeug.utils import redirect
from Camera.camera import Camera
import threading
import json

import uuid

views = Blueprint('views', __name__)

camera = mongo.db.cameraConfiguration
graph = mongo.db.graph

thread_dict = {}

@views.route('/', methods=['GET'])
def home():
    
    if 'user' in session:
        all = list(camera.find({"userId": session['user'].get('_id')}))
        for cam in all:
            id = cam.get("_id")
            if thread_dict.get(id) is None:
                newCameraThread = Camera(ip= cam.get("ip") , name = id , lock =  threading.Lock(), outputFrame_camera= None , configured= cam.get('configured'), cord1= cam.get('fc'), cord2= cam.get('sc'))
                thread_dict[id] = newCameraThread
                newCameraThread.start()


        print(  f"Active Threads :  {threading.active_count()}")
        for thread in threading.enumerate(): 
            print(thread.name)
        
        for key , value in thread_dict.items():
            print(key +" : " + str(value))

                #count = thread_dict.get(id).getCount()
                #totalCount+=count
                #count = thread_dict.get(id).getCount()
                #totalCount+=count
     

    return render_template("Admin/home.html")


@views.route('/display')
def display():
    if 'user' in session:
        configuredCameras = list(camera.find({"userId": session['user'].get('_id') , "configured" : True}))
        return render_template("Admin/futureDisplay.html" , allCameras = configuredCameras)
    return redirect('/')
       


@views.route('/report')
def report():

    if 'user' in session:
        configuredCameras = list(camera.find({"userId": session['user'].get('_id') , "configured" : True}))
        return render_template("Admin/report.html" , graphs = configuredCameras)
        
    return redirect('/')

@views.route('/cameras-data')
def reportData():
    if 'user' in session:
        configuredCameras = list(camera.find({"userId": session['user'].get('_id') , "configured" : True}))
        json_data = json.dumps(configuredCameras)
        return jsonify(json_data)

@views.route('/config' , methods = ["POST","GET"])
def config():
    # print(session['logged_in'])
    # if not session['logged_in']:
    #     return redirect('/')
    # return render_template("Admin/config.html")

    if request.method == "POST" :
        ip = request.form.get('ip')
        #print("IP : "+ ip )
        newCameraConfiguration = {
            '_id': str(uuid.uuid4()),
            'ip': ip,
            'userId': session['user'].get('_id'),
            'configured' : False,
            'createdAt' : request.form.get('creationDateAndTime'),
            'CameraName' : request.form.get('CameraName'),
            'threshold' : int(request.form.get('Threshold')),
            'fc' : {
                'x' : 0,
                'y' : 0
            },
            'sc' : {
                'x' : 720,
                'y' : 480
            }

        }
        print(newCameraConfiguration)
        camera.insert_one(newCameraConfiguration)
        sleep(1)
        return redirect('/config')
    if request.method == "GET":
        if 'user' in session:
            all = list(camera.find({"userId": session['user'].get('_id')}))
                
            for cam in all:
                if thread_dict.get(cam.get("_id")) is None:
                    id = cam.get("_id")
                    newCameraThread = Camera(ip= cam.get("ip") , name = id , lock =  threading.Lock(), outputFrame_camera= None , configured= cam.get('configured'), cord1= cam.get('fc'), cord2= cam.get('sc'))
                    thread_dict[id] = newCameraThread
                    newCameraThread.start()
                    count = thread_dict.get(cam.get("_id")).getCount()
                   
                else:
                    count = thread_dict.get(cam.get("_id")).getCount()
                   
                

                

            
            #print(ip)
            #save = camera.find_one({"ip": ip , 'userId' : session['user'].get('_id')})
            #x = 1
            # if save.get('configured'):
            #     cord1 = save.get('fc');
            #     cord2 = save.get('sc')

            #     x = 
            # else:
            #     x = Camera(ip,threading.Lock(), None , save.get('configured'))

            #x.start()
            #print(all)
           # print("hell")
            return render_template("Admin/configCameras.html", allCameras=all)
        else:
            return redirect('/')
            


@views.route('/config/<cameraId>', methods=['POST', 'GET'])
def cameraConfig(cameraId):
    if request.method == 'GET':
        selectedCamera = camera.find_one({"_id": cameraId})
        print("CAM - ", selectedCamera)
        return render_template('Admin/configCamera.html', cam=selectedCamera)

    else:
        data = request.form
        updateCam = camera.find_one({'_id': cameraId})
        updateCam['fc'] = {
            "x": int(data.get('cord1x')),
            "y": int(data.get('cord1y'))
        }
        updateCam['sc'] = {
            "x": int(data.get('cord2x')),
            "y": int(data.get('cord2y'))
        }
        updateCam['configured'] = True
        updateCam['CameraName'] = data.get('cameraName')
        updateCam['ip'] = data.get('IP')
        updateCam['threshold'] = int(data.get('Threshold'))
        
        
        #print(updateCam)
        camera.replace_one({'_id': cameraId}, updateCam)
        thread_dict.get(updateCam.get('_id')).terminate()
        sleep(1)
        thread_dict.get(updateCam.get('_id')).join()
        sleep(1)



        updatedCamThread  = Camera(ip= updateCam.get("ip") , name = updateCam.get("_id") , lock =  threading.Lock(), outputFrame_camera= None , configured= updateCam.get('configured'), cord1= updateCam.get('fc'), cord2= updateCam.get('sc'))
        thread_dict[updateCam.get('_id')] = updatedCamThread
        updatedCamThread.start()
        sleep(1)
        return redirect('/config')

@views.route("/delete/<id>" )
def delete(id):
    delId= camera.find_one({'_id' : id})
    camera.delete_one({'_id' : id})

    thread_dict[delId.get('_id')].terminate()
    sleep(1)
    thread_dict[delId.get('_id')].join()
    sleep(1)

    del thread_dict[delId.get('_id')]
    return redirect('/config')

@views.route("/video_feed/<string:id>")
def video_feed(id):
    # return the response generated along with the specific media
    # type (mime type)
    #print(ip)
    # save = camera.find_one({"ip": ip , 'userId' : session['user'].get('_id')})
    # x = 1
    # if save.get('configured'):
    #     cord1 = save.get('fc');
    #     cord2 = save.get('sc')
    #     x = Camera(ip,threading.Lock(), None ,save.get('configured'), cord1, cord2)
    # else:
    #     x = Camera(ip,threading.Lock(), None , save.get('configured'))

    # x.start()

    cam = thread_dict.get(id)
 
    return Response(cam.generate_camera(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


@views.route("/count_stream/<string:id>")
def count_stream(id):
    cam = thread_dict.get(id)
    return Response(cam.getCount(), mimetype="text/event-stream")


@views.route("/graph/<string:id>")
def graph(id):
    cam = thread_dict.get(id)
    return Response(cam.graph(), mimetype="text/event-stream")

