#test new network table library since the one on the robot is old and not supported anymore
import ntcore
from flask import Flask, Response

app = Flask(__name__)

def start(self):
    defaultInst = ntcore.NetworkTableInstance.getDefault()

    table = defaultInst.getTable('vision')

    self.xPub = table.getDoubleTopic('x').publish()

    self.yPub = table.getDoubleTopic('y').publish()

    self.x = 0

    self.y = 0

    go = True

def increase(self):
    while True:
        if go:
            self.x += 1
        
            self.y += 1











if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 1180, threaded=True)

