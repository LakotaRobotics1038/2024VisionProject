import cv2
from PIL import Image
import numpy
import math

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()


    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lowerLimit = numpy.array([0, 116, 163], dtype=numpy.uint8)
    upperLimit = numpy.array([12, 208, 255], dtype=numpy.uint8)

    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)

    mask_ = Image.fromarray(mask)

    bbox = mask_.getbbox()

    if (bbox != None):
        x1, y1, x2, y2 = bbox
        centerX = ((x2-x1)/2) + x1
        centerY = ((y2-y1)/2) + y1
        frame = cv2.putText(frame, ("x: " + str(centerX) + " y: " + str(centerY)), (x1, y1), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2, cv2.LINE_AA)
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        frame = cv2.circle(frame, (math.floor(centerX), math.floor(centerY)), 5, (0, 255, 0), -1) 

    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()