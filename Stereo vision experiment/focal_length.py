import numpy as np
import cv2
import glob

# Prepare object points (assuming a checkerboard pattern)
objp = np.zeros((6*8, 3), np.float32)
objp[:, :2] = np.mgrid[0:8, 0:6].T.reshape(-1, 2)  # Assumes a 8x6 chessboard pattern

# Arrays to store object points and image points
objpoints = []  # 3D points in real world space
imgpoints = []  # 2D points in image plane
frameSize = (1224,1632)
# Load calibration images
images = glob.glob('images/*.jpg')

# Iterate through calibration images
for fname in images:
    img = cv2.resize(cv2.imread(fname),frameSize)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, (8, 6), None)

    # If corners are found, add object points and image points
    if ret:
        objpoints.append(objp)
        imgpoints.append(corners)

# Calibrate camera
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# Print focal length
print("Focal length (in pixels):", mtx[0, 0])