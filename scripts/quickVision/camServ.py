

# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, Response
import cv2
import ntcore 
import threading
from datetime import datetime
import os
import apriltag 
import numpy as np

# Flask constructor takes the name of c
# declares cameras and set video type
app = Flask(__name__)
cam0 = cv2.VideoCapture(0)
cam1 = cv2.VideoCapture(1) 
fourcc = cv2.VideoWriter_fourcc(*'XVID') 

# declares NetworkTables and set server address and tables
# default port for network tables = 1735
serverAddr = '10.10.38.2'
instance = ntcore.NetworkTableInstance.getDefault(0)
visionTable = instance.getTable('vision')
fmsTable = instance.getTable('FMSInfo') #uncomment for competition
shouldStream0Sub = visionTable.getBooleanTopic("ShouldStream0").subscribe(True)

# The get_image() method returns image from camera
def get_image():
    ret, img = cam0.read()

    while True:
        shouldStream0 =shouldStream0Sub.get()

        if(shouldStream0):
            ret, img = cam0.read()
        else:
            ret, img = cam1.read()
        
        if not ret:
            continue
        
        img = cv2.resize(img, (0, 0), fx = 0.33, fy = 0.33)
        # Converts (encodes) image formats into streaming data and stores it in-memory cache.
        frame = cv2.imencode('.jpg', img)[1]

        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n')

def biggestContourI(contours):
    maxVal = 0
    maxI = None
    for i in range(0, len(contours)):
        if len(contours[i]) > maxVal:
            maxVal = len(contours[i])
            maxI = i
    return maxI

def hsv_Detection(img):
    
    lh = 1
    ls = 122
    lv = 199
    hh = 69
    hs = 255
    hv = 255

    lower = np.array([lh, ls, lv], dtype = "uint8")
    higher = np.array([hh, hs, hv], dtype = "uint8")
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    flt = cv2.inRange(hsv, lower, higher)
    
    contours0, _ = cv2.findContours(flt, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Only draw the biggest one
    bc = biggestContourI(contours0)
   
    
   
     


# The record_cam() method records images from camera
def record_cam():
    print("Recording ...")
    isRecording = False
    shouldRecordSub = visionTable.getBooleanTopic("shouldRecord").subscribe(True)
    matchIDSub = fmsTable.getIntegerTopic("MatchNumber").subscribe(0)
    rematchIDSub = fmsTable.getIntegerTopic("ReplayNumber").subscribe(0)
    while True:
        realTime = datetime.now()
        shouldRecord = shouldRecordSub.get()

        if shouldRecord:
            ret0, img0 = cam0.read()
            ret1, img1 = cam1.read()

            if not isRecording:
                # uncomment following 3 lines for competition
                #matchID = matchIDSub.get()
                #rematchID = rematchIDSub.get()
                #out = cv2.VideoWriter(str(matchID) + '-' + str(rematchID) + '.avi', fourcc, 60.0, (img.shape[1], img.shape[0]))
                if ret0:
                    out0 = cv2.VideoWriter(f"{os.path.expanduser('~')}/Videos/{realTime.strftime('%Y-%m-%d at %H-%M-%S')} cam0.avi", fourcc, 15.0, (img0.shape[1], img0.shape[0]))
                    print(out0)
                if ret1:
                    out1 = cv2.VideoWriter(f"{os.path.expanduser('~')}/Videos/{realTime.strftime('%Y-%m-%d at %H-%M-%S')} cam1.avi", fourcc, 15.0, (img1.shape[1], img1.shape[0]))
                    print(out1)

            if ret0:
                out0.write(img0)
            if ret1:
                out1.write(img1)
            isRecording = True
        elif isRecording and not shouldRecord:
            if out0:
                out0.release()
            if out1:
                out1.release()
            isRecording = False


# The run_network() method sets network table with image data
def run_network():
    print('running network table ...')
    detector = apriltag.Detector()
    valuesPub= visionTable.getStringTopic("values").publish("[]")
    while True:
        on0 = visionTable.getBoolean('on0', True)#change to false for comp 
        on1 = visionTable.getBoolean('on1', False)
        ret = False

        if on0:
            ret, img = cam0.read()
        elif on1:
            ret, img = cam1.read()

        if ret:
            print('time to process images.')
            
            result = detector.detect(cv2.cvtColor(img,cv2.COLOR_BGR2GRAY))

            print(img)
            print(result)

            valuesPub.set()
            #tables.putString('values', result)

            print(tables)
    

            
            
# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/stream')
# ‘/’ URL is bound with hello_world() function.
def stream0():
    return Response(get_image(), mimetype='multipart/x-mixed-replace; boundary=frame')
 
# main driver function
if __name__ == '__main__':
    # Declare, initialize and start the vision process thread
    visionThread = threading.Thread(target=run_network)
    visionThread.start()

    # Declare, initialize and start the recording process thread
    #recordingThread = threading.Thread(target=record_cam)
    #recordingThread.start()
 
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(host='0.0.0.0', port = 1180, threaded=True)

