from numpy import zeros, mgrid, float32
from cv2 import TERM_CRITERIA_EPS, TERM_CRITERIA_MAX_ITER, imread, cvtColor, COLOR_BGR2GRAY, findChessboardCorners, cornerSubPix, calibrateCamera
from glob import glob
from typing import Tuple, Any

# Size of each square in meters
SQUARE_SIZE: float = 0.025  # 25mm in meters

# Define the grid dimensions (number of inner corners)
GRID_SIZE: Tuple[int, int] = (10, 7)

# Prepare object points
OBJP = zeros((GRID_SIZE[0] * GRID_SIZE[1], 3), float32)
OBJP[:, :2] = mgrid[0:GRID_SIZE[0], 0:GRID_SIZE[1]].T.reshape(-1, 2) # * square_size
# Arrays to store object points and image points from all the images.
objpoints: Any = []  # 3d point in real world space
imgpoints: Any = []  # 2d points in image plane.

# Read images and find chessboard corners
images = glob(r"calibration_images/*.jpeg")  # Change the path to your calibration images

criteria = (TERM_CRITERIA_EPS + TERM_CRITERIA_MAX_ITER, 30, 0.001)

for fname in images:
    print(fname)
    img = imread(fname)
    gray = cvtColor(img, COLOR_BGR2GRAY)

    # Find the chessboard corners
    ret, corners = findChessboardCorners(gray, GRID_SIZE, None)

    # If found, add object points, image points (after refining them)
    if ret:
        objpoints.append(OBJP)

        corners2 = cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

# Calibrate camera
_, mtx, _, _, _ = calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# Extract focal length and principal point from the camera matrix

print(f"Focal Length: (fx, fy) = {(mtx[0, 0], mtx[1, 1])}")
print(f"Principal Point: (cx, cy) = {(mtx[0, 2], mtx[1, 2])}")