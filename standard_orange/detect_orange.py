import cv2
import numpy as np

# Callback function for trackbar changes
def on_trackbar(val):
    pass

# Function to detect orange areas based on trackbar values
def detect_orange_areas(frame, lower_orange, upper_orange):
    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image to get only orange colors
    mask = cv2.inRange(hsv, lower_orange, upper_orange)

    # Apply a series of morphological operations to clean up the mask
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Apply the mask to the original frame
    result = cv2.bitwise_and(frame, frame, mask=mask)

    return result

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Create a window for the trackbars
cv2.namedWindow('Trackbars')

# Initialize trackbar values
lower_orange = np.array([0, 129, 160])
upper_orange = np.array([15, 198, 255])

# Create trackbars for adjusting HSV color range thresholds
cv2.createTrackbar('Hue Lower', 'Trackbars', lower_orange[0], 179, on_trackbar)
cv2.createTrackbar('Saturation Lower', 'Trackbars', lower_orange[1], 255, on_trackbar)
cv2.createTrackbar('Value Lower', 'Trackbars', lower_orange[2], 255, on_trackbar)
cv2.createTrackbar('Hue Upper', 'Trackbars', upper_orange[0], 179, on_trackbar)
cv2.createTrackbar('Saturation Upper', 'Trackbars', upper_orange[1], 255, on_trackbar)
cv2.createTrackbar('Value Upper', 'Trackbars', upper_orange[2], 255, on_trackbar)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break
    
    # Get trackbar values
    lower_orange[0] = cv2.getTrackbarPos('Hue Lower', 'Trackbars')
    lower_orange[1] = cv2.getTrackbarPos('Saturation Lower', 'Trackbars')
    lower_orange[2] = cv2.getTrackbarPos('Value Lower', 'Trackbars')
    upper_orange[0] = cv2.getTrackbarPos('Hue Upper', 'Trackbars')
    upper_orange[1] = cv2.getTrackbarPos('Saturation Upper', 'Trackbars')
    upper_orange[2] = cv2.getTrackbarPos('Value Upper', 'Trackbars')

    # Detect orange areas based on trackbar values
    detected_area = detect_orange_areas(frame, lower_orange, upper_orange)

    # Display the resulting frame
    cv2.imshow('Detected Orange Areas', detected_area)
    
    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
