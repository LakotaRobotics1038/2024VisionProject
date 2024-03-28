import cv2
import numpy as np

def nothing(n):
    pass

# Contours w/ greatest number of points
#TOdo max by area
def biggestContourI(contours):
    maxVal = 0
    maxI = None
    for i in range(0, len(contours)):
        if len(contours[i]) > maxVal:
            cs = contours[i]
            maxVal = len(contours[i])
            maxI = i
    return maxI
            
#default hsv values on the right
# lakota robotic controns room vals = lowH 1 HighH 69 LowS 122 HighS 255 LowV 199 HightV 255
iLowH = 1#0
iHighH = 69#5
iLowS = 122#116
iHighS = 255#208
iLowV = 199#163
iHighV = 255#225

cv2.namedWindow('Control')
cv2.createTrackbar("LowH", "Control", iLowH, 255, nothing)
cv2.createTrackbar("HighH", "Control", iHighH, 255, nothing)
cv2.createTrackbar("LowS", "Control", iLowS, 255, nothing)
cv2.createTrackbar("HighS", "Control", iHighS, 255, nothing)
cv2.createTrackbar("LowV", "Control", iLowV, 255, nothing)
cv2.createTrackbar("HighV", "Control", iHighV, 255, nothing)

cam = cv2.VideoCapture(0)

while True:
    ret_val, img = cam.read()

    lh = 1#cv2.getTrackbarPos('LowH', 'Control')
    ls = 122#cv2.getTrackbarPos('LowS', 'Control')
    lv = 199#cv2.getTrackbarPos('LowV', 'Control')
    hh = 69#cv2.getTrackbarPos('HighH', 'Control')
    hs = 255#cv2.getTrackbarPos('HighS', 'Control')
    hv = 255#cv2.getTrackbarPos('HighV', 'Control')

    lower = np.array([lh, ls, lv], dtype = "uint8")
    higher = np.array([hh, hs, hv], dtype = "uint8")
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, w = img.shape[:2]
    flt = cv2.inRange(hsv, lower, higher)
    
    contours0, hierarchy = cv2.findContours(flt, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Only draw the biggest one

    bc = biggestContourI(contours0)
    cv2.drawContours(img, contours0, bc, (0, 255, 0), 3)

    if bc is not None:
        n=0 #n = the number of iterations the loop below has been through
        totalX=0
        totalY=0
        x_values = []
        y_values = []
        
        for i in range(len(contours0[bc])):

            xyCoord = contours0[bc][i][0]
            x_values.append(xyCoord[0])
            y_values.append(xyCoord[1])

        center_x = int((max(x_values) - min(x_values)) / 2 + min(x_values))
        center_y = int((max(y_values) - min(y_values)) / 2 + min(y_values)) 
        img = cv2.circle(img, (center_x, center_y), 15, (0, 0, 255), -1) 

    
    cv2.imshow('cam', img)
    cv2.imshow('hsv', hsv)
    cv2.imshow('flt', flt)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
