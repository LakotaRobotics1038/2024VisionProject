import cv2
import numpy as np

# Function to detect the largest bounding ellipse with a certain threshold of orange
def detect_largest_ellipse(frame, lower_orange, upper_orange, orange_threshold):
    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image to get only orange colors
    mask = cv2.inRange(hsv, lower_orange, upper_orange)

    # Calculate the percentage of orange in the mask
    total_pixels = np.prod(mask.shape[:2])
    orange_pixels = cv2.countNonZero(mask)
    orange_percentage = (orange_pixels / total_pixels) * 100

    # If the orange percentage is below the threshold, return None
    if orange_percentage < orange_threshold:
        return None

    # Find contours in the mask
    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour
    largest_contour = max(contours, key=cv2.contourArea)

    # Fit an ellipse to the largest contour
    ellipse = cv2.fitEllipse(largest_contour)

    # Draw the ellipse on the original frame
    cv2.ellipse(frame, ellipse, (0, 255, 0), 2)

    # Get the center coordinates of the ellipse
    center = (int(ellipse[0][0]), int(ellipse[0][1]))

    return center

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Initialize trackbar values
lower_orange = np.array([0, 120, 180])
upper_orange = np.array([15, 198, 255])
orange_threshold = 1  # Percentage of orange required to detect ellipse

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break
    
    # Detect the largest bounding ellipse with a certain threshold of orange
    ellipse_center = detect_largest_ellipse(frame, lower_orange, upper_orange, orange_threshold)

    # If an ellipse is detected, print its location
    if ellipse_center:
        print("Ellipse Center:", ellipse_center)

    # Display the resulting frame
    cv2.imshow('Largest Bounding Ellipse', frame)
    
    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
