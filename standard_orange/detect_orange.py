import cv2
import numpy as np

def find_largest_orange_circle(frame):
    # Convert the frame to HSV (Hue, Saturation, Value) color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Define the range of orange color in HSV
    lower_orange = np.array([5, 50, 50])
    upper_orange = np.array([15, 255, 255])

    # Threshold the HSV image to get only orange colors
    mask = cv2.inRange(hsv, lower_orange, upper_orange)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    largest_circle = None
    max_radius = 0
    
    # Iterate through all contours to find the largest round shape
    for contour in contours:
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        circularity = 4 * np.pi * area / (perimeter * perimeter)
        
        # Define circularity threshold
        circularity_threshold = 0.6
        
        if circularity > circularity_threshold:
            # Fit a circle to the contour
            (x, y), radius = cv2.minEnclosingCircle(contour)
            
            # Convert the radius to integer
            radius = int(radius)
            
            # Check if the contour is the largest circle found so far
            if radius > max_radius:
                max_radius = radius
                largest_circle = (x, y), radius

    return largest_circle

# Open the webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    if not ret:
        break

    # Find the largest orange circle in the frame
    orange_circle = find_largest_orange_circle(frame)

    if orange_circle is not None:
        # Draw the largest orange circle
        (x, y), radius = orange_circle
        cv2.circle(frame, (int(x), int(y)), radius, (0, 255, 255), 2)

    # Display the frame
    cv2.imshow('Largest Orange Circle', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
