from flask import Flask, Response
import cv2
# from networktables import NetworkTables
from datetime import datetime

# declares cameras and sets our server address
app = Flask(__name__)
cam0 = cv2.VideoCapture(0)
# cam1 = cv2.VideoCapture(1)
serverAddr = '10.10.38.2'

# NetworkTables.initialize(server=serverAddr)
# gets custom table
# tables = NetworkTables.getTable('Vision')

def get_image():
    ret, img = cam0.read()
    # ret, img = cam1.read()
    # default port for network tables = 1735

    while True:
        # shouldStream0 = tables.getboolean('shouldStream0', True)

        # if (shouldStream0):
        ret, img = cam0.read()
        # else:
        #     ret, img = cam1.read()

        img = cv2.resize(img, (160, 120))
        _, frame = cv2.imencode('.jpg', img)
        yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n'

@app.route('/stream')
def stream():
    return Response(get_image(), mimetype='multipart/x-mixed-replace; boundary=frame')

app.run(host='0.0.0.0', port = 1180, threaded=True)
        