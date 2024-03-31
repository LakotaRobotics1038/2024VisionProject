# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, Response
import cv2
from ntcore import NetworkTableInstance
import threading
from datetime import datetime
import os
import apriltag
import json
import numpy as np

# Flask constructor takes the name of c
# declares cameras and set video type
app = Flask(__name__)
cam0 = cv2.VideoCapture(0)
cam1 = cv2.VideoCapture(1)
fourcc = cv2.VideoWriter_fourcc(*'XVID')

# declares NetworkTables and set server address and tables
# default port for network tables = 1735
instance = NetworkTableInstance.getDefault()

visionTable = instance.getTable('Vision')
fmsTable = instance.getTable('FMSInfo')

instance.startClient4("Vision Client")
instance.setServerTeam(1038)

shouldStream0Sub = visionTable.getBooleanTopic("ShouldStream0").subscribe(True)
enable0Sub = visionTable.getBooleanTopic("enable0").subscribe(False)
enable1Sub = visionTable.getBooleanTopic("enable1").subscribe(False)
valuesPub = visionTable.getStringTopic("values").publish()

dataOut = [] # this is what stuff with be appended into for network tables publishing

# The get_image() method returns image from camera
def get_image():
    ret, img = cam0.read()

    while True:
        shouldStream0 = shouldStream0Sub.get()

        if(shouldStream0):

            ret, img = cam0.read()
        else:
            ret, img = cam1.read()

        if not ret:
            continue

        img = cv2.resize(img, (320, 180))
        # Converts (encodes) image formats into streaming data and stores it in-memory cache.
        _, frame = cv2.imencode('.jpg', img)

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
    cv2.drawContours(img, contours0, bc, (0, 255, 0), 3)

    #find avg for total x + y to find center of contour
    if bc is not None:
        x_values = []
        y_values = []

        for i in range(len(contours0[bc])):

            xyCoord = contours0[bc][i][0]
            x_values.append(xyCoord[0])
            y_values.append(xyCoord[1])

        center_x = int((max(x_values) - min(x_values)) / 2 + min(x_values))
        center_y = int((max(y_values) - min(y_values)) / 2 + min(y_values))
        img = cv2.circle(img, (center_x, center_y), 15, (0, 0, 255), -1)
        centerPoint = [center_x,center_y]

        dataOut = []
        dataOut.append({
            'id': str(17),
            'center': str(centerPoint),
            'corners': str("")
        })

        valuesPub.set(json.dumps(dataOut))
        print(str(dataOut))
        print(f"Size: {max(x_values) - min(x_values)}, {max(y_values) - min(y_values)}")


# The record_cam() method records images from camera
def record_cam():
    #print("Recording ...")
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
                #uncomment following 3 lines for competition
                #matchID = matchIDSub.get()
                #rematchID = rematchIDSub.get()
                #out = cv2.VideoWriter(str(matchID) + '-' + str(rematchID) + '.avi', fourcc, 60.0, (img.shape[1], img.shape[0]))
                if ret0:
                    out0 = cv2.VideoWriter(f"{os.path.expanduser('~')}/Videos/{realTime.strftime('%Y-%m-%d at %H-%M-%S')} cam0.avi", fourcc, 15.0, (img0.shape[1], img0.shape[0]))
                    #print(out0)
                if ret1:
                    out1 = cv2.VideoWriter(f"{os.path.expanduser('~')}/Videos/{realTime.strftime('%Y-%m-%d at %H-%M-%S')} cam1.avi", fourcc, 15.0, (img1.shape[1], img1.shape[0]))
                    #print(out1)

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
    #print('running network table ...')
    detector = apriltag.Detector()

    while True:
        enabled0 = enable0Sub.get()
        enabled1 = enable1Sub.get()
        ret = False

        if enabled0:
            ret, img = cam0.read()
        elif enabled1:
            ret, img = cam1.read()

        if ret:
            dataOut=[]
            #hsv_Detection(img)
            #print('time to process images.')

            img = cv2.resize(img, (320, 180))
            result = detector.detect(cv2.cvtColor(img,cv2.COLOR_BGR2GRAY))

            if len(result) != 0:
                dataOut.append({
                    'id': str(result[0][1]),
                    'x': str(result[0][6][0]),
                    'y': str(result[0][6][1]),
                    'corners': str(result[0][7])
                })

                # print(str(dataOut))

            valuesPub.set(json.dumps(dataOut))
            # id and corners are for april tags only
            # center is for the notes/rings only

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/stream')
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

