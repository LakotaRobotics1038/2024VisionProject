import numpy as np
import cv2
import glob

# Size of each square in meters
square_size = 0.025  # 25mm in meters

# Define the grid dimensions (number of inner corners)
grid_size = (10, 7)

# Prepare object points
objp = np.zeros((grid_size[0] * grid_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:grid_size[0], 0:grid_size[1]].T.reshape(-1, 2) # * square_size

# Arrays to store object points and image points from all the images.
objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.

# Read images and find chessboard corners
images = glob.glob('calibration_images/*.jpeg')  # Change the path to your calibration images

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

for fname in images:
    print(fname)
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, grid_size, None)

    # If found, add object points, image points (after refining them)
    if ret:
        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

# Calibrate camera
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# Extract focal length and principal point from the camera matrix
focal_length_x = mtx[0, 0]
focal_length_y = mtx[1, 1]
principal_point_x = mtx[0, 2]
principal_point_y = mtx[1, 2]

print("Focal Length: (fx, fy) =", (focal_length_x, focal_length_y))
print("Principal Point: (cx, cy) =", (principal_point_x, principal_point_y))