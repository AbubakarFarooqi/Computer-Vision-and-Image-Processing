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

# Mediapipe for face detection
# import mediapipe as mp
import time



def calculate_depth(center_point_right, center_point_left, frame_width, focal_length):
    disparity = abs(center_point_right[0] - center_point_left[0])
    depth = (frame_width * focal_length) / disparity
    return depth



# mp_facedetector = mp.solutions.face_detection
# mp_draw = mp.solutions.drawing_utils

# Open both cameras
# cap_right = cv2.VideoCapture(2, cv2.CAP_DSHOW)                    
# cap_left =  cv2.VideoCapture(0, cv2.CAP_DSHOW)


# Stereo vision setup parameters
frame_rate = 120    #Camera frame rate (maximum at 120 fps)
B = 16               #Distance between the cameras [cm]
f = 35              #Camera lense's focal length [mm]
# alpha = 56.6        #Camera field of view in the horisontal plane [degrees]
alpha = 63        #Camera field of view in the horisontal plane [degrees]




# Main program loop with face detector and depth estimation using stereo vision
# with mp_facedetector.FaceDetection(min_detection_confidence=0.7) as face_detection:
# if True:
#     while(True):
#     # while(cap_right.isOpened() and cap_left.isOpened()):

#         # succes_right, frame_right = cap_right.read()
#         # succes_left, frame_left = cap_left.read()

#         frame_right = cv2.imread('1.jfif')
#         frame_right = cv2.resize(frame_right, (300, 400))

#         frame_left = cv2.imread('2.jfif')
#         frame_left = cv2.resize(frame_left, (300, 400))
#     ################## CALIBRATION #########################################################

#         frame_right, frame_left = calibration.undistortRectify(frame_right, frame_left)

#     ########################################################################################

#         # If cannot catch any frame, break
#         if  False:                    
#         # if not succes_right or not succes_left and False:                    
#             break

#         else:

#             start = time.time()
            
#             # Convert the BGR image to RGB
#             frame_right = cv2.cvtColor(frame_right, cv2.COLOR_BGR2RGB)
#             frame_left = cv2.cvtColor(frame_left, cv2.COLOR_BGR2RGB)

#             # Process the image and find faces
#             results_right = face_detection.process(frame_right)
#             results_left = face_detection.process(frame_left)

#             # Convert the RGB image to BGR
#             frame_right = cv2.cvtColor(frame_right, cv2.COLOR_RGB2BGR)
#             frame_left = cv2.cvtColor(frame_left, cv2.COLOR_RGB2BGR)


#             ################## CALCULATING DEPTH #########################################################

#             center_right = 0
#             center_left = 0

#             if results_right.detections:
#                 for id, detection in enumerate(results_right.detections):
#                     mp_draw.draw_detection(frame_right, detection)

#                     bBox = detection.location_data.relative_bounding_box

#                     h, w, c = frame_right.shape

#                     boundBox = int(bBox.xmin * w), int(bBox.ymin * h), int(bBox.width * w), int(bBox.height * h)

#                     center_point_right = (boundBox[0] + boundBox[2] / 2, boundBox[1] + boundBox[3] / 2)

#                     cv2.putText(frame_right, f'{int(detection.score[0]*100)}%', (boundBox[0], boundBox[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 2)


#             if results_left.detections:
#                 for id, detection in enumerate(results_left.detections):
#                     mp_draw.draw_detection(frame_left, detection)

#                     bBox = detection.location_data.relative_bounding_box

#                     h, w, c = frame_left.shape

#                     boundBox = int(bBox.xmin * w), int(bBox.ymin * h), int(bBox.width * w), int(bBox.height * h)

#                     center_point_left = (boundBox[0] + boundBox[2] / 2, boundBox[1] + boundBox[3] / 2)

#                     cv2.putText(frame_left, f'{int(detection.score[0]*100)}%', (boundBox[0], boundBox[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 2)




#             # If no ball can be caught in one camera show text "TRACKING LOST"
#             if not results_right.detections or not results_left.detections:
#                 cv2.putText(frame_right, "TRACKING LOST", (75,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)
#                 cv2.putText(frame_left, "TRACKING LOST", (75,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)

#             else:
#                 # Function to calculate depth of object. Outputs vector of all depths in case of several balls.
#                 # All formulas used to find depth is in video presentaion
#                 depth = tri.find_depth(center_point_right, center_point_left, frame_right, frame_left, B, f, alpha)

#                 cv2.putText(frame_right, "Distance: " + str(round(depth,1)), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255,0),3)
#                 cv2.putText(frame_left, "Distance: " + str(round(depth,1)), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255,0),3)
#                 # Multiply computer value with 205.8 to get real-life depth in [cm]. The factor was found manually.
#                 print("Depth: ", str(round(depth,1)))



#             end = time.time()
#             totalTime = end - start

#             fps = 1 / totalTime
#             #print("FPS: ", fps)

#             cv2.putText(frame_right, f'FPS: {int(fps)}', (20,450), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255,0), 2)
#             cv2.putText(frame_left, f'FPS: {int(fps)}', (20,450), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255,0), 2)                                   


#             # Show the frames
#             cv2.imshow("frame right", frame_right) 
#             cv2.imshow("frame left", frame_left)


#             # Hit "q" to close the window
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break



model = YOLO('yolov8n.pt')

if True:
    while(True):
    # while(cap_right.isOpened() and cap_left.isOpened()):

        # succes_right, frame_right = cap_right.read()
        # succes_left, frame_left = cap_left.read()

        frame_right = cv2.imread('1.jpg')
        frame_right = cv2.resize(frame_right, (300, 400))

        frame_left = cv2.imread('2.jpg')
        frame_left = cv2.resize(frame_left, (300, 400))
    ################## CALIBRATION #########################################################

        # frame_right, frame_left = calibration.undistortRectify(frame_right, frame_left)

    ########################################################################################

        # If cannot catch any frame, break
        if  False:                    
        # if not succes_right or not succes_left and False:                    
            break

        else:

            start = time.time()
            

            # Convert the BGR image to RGB
            # frame_right = cv2.cvtColor(frame_right, cv2.COLOR_BGR2RGB)
            # frame_left = cv2.cvtColor(frame_left, cv2.COLOR_BGR2RGB)
            # cv2.imshow("YOLOv8 Tracking", frame_right)
            # Process the image and find faces
            results_right = model(frame_right)
            results_left = model(frame_left)

            for result in [results_right, results_left]:
                # box = result[0].boxes.xyxy
                # for detection in result[0].boxes.xyxy:
                for box in result[0].boxes:
                    # Extract class name and confidence
                    # class_id = int(detection[5])
                    # confidence = float(detection[4])
                    # class_name = model.names[class_id]
                    
                    label = result[0].names[int(box.cls)]
                    confidence = float(box.conf.cpu())
                    print(label)
                    # Draw bounding box and label
                    # if confidence > 0.5:
                    if confidence > 0.1:
                            detection = box.xyxy[0]
                            x_min, y_min, x_max, y_max = detection[:4].cpu().numpy().astype(int)
                            # x_min, y_min, x_max, y_max = map(int, detection[:4])
                            if(result == results_right):
                                cv2.rectangle(frame_right, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                                cv2.putText(frame_right, f'{label}: {confidence:.2f}', (x_min, y_min - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                            else:
                                cv2.rectangle(frame_left, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                                cv2.putText(frame_left, f'{label}: {confidence:.2f}', (x_min, y_min - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                            # Calculate center point of the bounding box
                            center_point = ((x_min + x_max) // 2, (y_min + y_max) // 2)

                            # Store center points of objects in the right and left frames
                            if result == results_right:
                                if(label == "bottle" or label == "vase"):
                                    center_point_right = center_point
                            else:
                                if(label == "bottle" or label == "vase"):
                                    center_point_left = center_point
                            

            # # Calculate depth if both right and left objects are detected
            # if 'center_point_right' in locals() and 'center_point_left' in locals():
            # # Calculate depth
            # depth = calculate_depth(center_point_right, center_point_left, frame_right.shape[1], focal_length)
            # print("Depth:", depth)




            # Function to calculate depth of object. Outputs vector of all depths in case of several balls.
            # All formulas used to find depth is in video presentaion
            depth = tri.find_depth(center_point_right, center_point_left, frame_right, frame_left, B, f, alpha)
            # cv2.putText(frame_right, "Distance: " + str(round(depth,1)), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0),3)
            # cv2.putText(frame_left, "Distance: " + str(round(depth,1)), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0),3)
            cv2.putText(frame_left, "Distance: " + str(round(depth,1)), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),3)
            cv2.putText(frame_right, "Distance: " + str(round(depth,1)), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),3)

            
            # Multiply computer value with 205.8 to get real-life depth in [cm]. The factor was found manually.
            print("Depth: ", str(round(depth,1)))


                        # # Show the frames
            cv2.imshow("frame right", frame_right) 
            cv2.imshow("frame left", frame_left)


            # Hit "q" to close the window
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            break












            # # Convert the RGB image to BGR
            # frame_right = cv2.cvtColor(frame_right, cv2.COLOR_RGB2BGR)
            # frame_left = cv2.cvtColor(frame_left, cv2.COLOR_RGB2BGR)


            # ################## CALCULATING DEPTH #########################################################

            # center_right = 0
            # center_left = 0

            # if results_right.detections:
            #     for id, detection in enumerate(results_right.detections):
            #         mp_draw.draw_detection(frame_right, detection)

            #         bBox = detection.location_data.relative_bounding_box

            #         h, w, c = frame_right.shape

            #         boundBox = int(bBox.xmin * w), int(bBox.ymin * h), int(bBox.width * w), int(bBox.height * h)

            #         center_point_right = (boundBox[0] + boundBox[2] / 2, boundBox[1] + boundBox[3] / 2)

            #         cv2.putText(frame_right, f'{int(detection.score[0]*100)}%', (boundBox[0], boundBox[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 2)


            # if results_left.detections:
            #     for id, detection in enumerate(results_left.detections):
            #         mp_draw.draw_detection(frame_left, detection)

            #         bBox = detection.location_data.relative_bounding_box

            #         h, w, c = frame_left.shape

            #         boundBox = int(bBox.xmin * w), int(bBox.ymin * h), int(bBox.width * w), int(bBox.height * h)

            #         center_point_left = (boundBox[0] + boundBox[2] / 2, boundBox[1] + boundBox[3] / 2)

            #         cv2.putText(frame_left, f'{int(detection.score[0]*100)}%', (boundBox[0], boundBox[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 2)




            # # If no ball can be caught in one camera show text "TRACKING LOST"
            # if not results_right.detections or not results_left.detections:
            #     cv2.putText(frame_right, "TRACKING LOST", (75,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)
            #     cv2.putText(frame_left, "TRACKING LOST", (75,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)

            # else:
            #     # Function to calculate depth of object. Outputs vector of all depths in case of several balls.
            #     # All formulas used to find depth is in video presentaion
            #     depth = tri.find_depth(center_point_right, center_point_left, frame_right, frame_left, B, f, alpha)

            #     cv2.putText(frame_right, "Distance: " + str(round(depth,1)), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255,0),3)
            #     cv2.putText(frame_left, "Distance: " + str(round(depth,1)), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255,0),3)
            #     # Multiply computer value with 205.8 to get real-life depth in [cm]. The factor was found manually.
            #     print("Depth: ", str(round(depth,1)))



            # end = time.time()
            # totalTime = end - start

            # fps = 1 / totalTime
            # #print("FPS: ", fps)

            # cv2.putText(frame_right, f'FPS: {int(fps)}', (20,450), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255,0), 2)
            # cv2.putText(frame_left, f'FPS: {int(fps)}', (20,450), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255,0), 2)                                   


            # # Show the frames
            # cv2.imshow("frame right", frame_right) 
            # cv2.imshow("frame left", frame_left)


            # # Hit "q" to close the window
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break


# Release and destroy all windows before termination
# cap_right.release()
# cap_left.release()
cv2.waitKey(0   )
# cv2.destroyAllWindows()