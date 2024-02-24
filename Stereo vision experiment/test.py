import sys
import cv2
import numpy as np
import time
import imutils
from matplotlib import pyplot as plt
from ultralytics import YOLO
# Function for stereo vision and depth estimation
import triangulation as tri
import calibration
import time

frame_rate = 120    #Camera frame rate (maximum at 120 fps)
B = 16                 #Distance between the cameras [cm]
# f = 35              #Camera lense's focal length [mm]
f = 28              #Camera lense's focal length [mm]
# alpha = 148        #Camera field of view in the horisontal plane [degrees]
alpha = 70        #Camera field of view in the horisontal plane [degrees]

model = YOLO('yolov8n.pt')

frame_right = cv2.imread('1.jpg')
frame_right = cv2.resize(frame_right, (1224,1632))
frame_left = cv2.imread('2.jpg')
frame_left = cv2.resize(frame_left, (1224,1632))

# frame_right, frame_left = calibration.undistortRectify(frame_right, frame_left)

# cv2.imshow('a',frame_left)
# cv2.imshow('b',frame_right)
# cv2.waitKey(0)

start = time.time()

results_right = model(frame_right)
results_left = model(frame_left)

label_left = []
label_right = []
confidence_left = []
confidence_right = []
centerPoint_left = []
centerPoint_right = []
x_min_left = []
y_min_left = []
x_max_left = []
y_max_left = []
x_min_right = []
y_min_right = []
x_max_right = []
y_max_right = []


for box in results_left[0].boxes:
    label = results_left[0].names[int(box.cls)]
    confidence = float(box.conf.cpu())
    detection = box.xyxy[0]
    x_min, y_min, x_max, y_max = detection[:4].cpu().numpy().astype(int)
    center_point = ((x_min + x_max) // 2, (y_min + y_max) // 2)
    
    centerPoint_left.append(center_point)
    label_left.append(label)
    confidence_left.append(confidence)
    x_min_left.append(x_min)
    y_min_left.append(y_min)
    x_max_left.append(x_max)
    y_max_left.append(y_max)




for box in results_right[0].boxes:
    label = results_right[0].names[int(box.cls)]
    confidence = float(box.conf.cpu())
    detection = box.xyxy[0]
    x_min, y_min, x_max, y_max = detection[:4].cpu().numpy().astype(int)
    center_point = ((x_min + x_max) // 2, (y_min + y_max) // 2)
    
    centerPoint_right.append(center_point)
    label_right.append(label)
    confidence_right.append(confidence)
    x_min_right.append(x_min)
    y_min_right.append(y_min)
    x_max_right.append(x_max)
    y_max_right.append(y_max)

for i in range(min(len(label_left), len(label_right))):
    try:
        idx = label_left.index(label_right[i])
    except ValueError:
        continue
    depth = tri.find_depth(centerPoint_right[i], centerPoint_left[idx], frame_right, frame_left, B, f, alpha)
    cv2.rectangle(frame_right, (x_min_right[i], y_min_right[i]), (x_max_right[i], y_max_right[i]), (0, 255, 0), 2)
    cv2.putText(frame_right, f'{label_right[i]}: {confidence_right[i]:.2f}: Distance {depth:.2f}', (x_min_right[i], y_min_right[i] - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    print(f'{label_left[idx]} : {depth}')             
cv2.imshow("aa",cv2.resize(frame_right,(500,600)))
cv2.waitKey(0)
   