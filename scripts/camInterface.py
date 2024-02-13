
import cv2
import camServ
import time

runCam = False
running = False

#turns vision proccesing on and off and turns off the camera

while running:

    key = cv2.waitKey(1)

    if key == ord('b'):
        runCam = True
        runCam = app.run(host='0.0.0.0', port = 1180, threaded = True)

    elif key == ord('n'):
        runCam = False
        app.stop(host='0.0.0.0', port = 1180, threaded=true)

    elif key == ord('q'):
        running = False

    endTime = time.time()

camera.stop()
  
