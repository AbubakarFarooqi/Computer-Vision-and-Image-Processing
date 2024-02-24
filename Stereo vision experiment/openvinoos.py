
import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')

img1 = cv2.imread("1.jfif")
# cv2.imshow("a",img1)
# img1 = cv2.imread("1.jfif",cv2.IMREAD_GRAYSCALE)
img1 =  cv2.resize(img1, (500, 600))

results = model(img1)

# results = model.track(img1, persist=True)

        # Visualize the results on the frame
annotated_frame = results[0].plot()

        # Display the annotated frame
cv2.imshow("YOLOv8 Tracking", annotated_frame)
cv2.waitKey(0)
# # Loop through the video frames
# while cap.isOpened():
#     # Read a frame from the video
#     success, frame = cap.read()

#     if success:
#         # Run YOLOv8 tracking on the frame, persisting tracks between frames
#         results = model.track(frame, persist=True)

#         # Visualize the results on the frame
#         annotated_frame = results[0].plot()

#         # Display the annotated frame
#         cv2.imshow("YOLOv8 Tracking", annotated_frame)

#         # Break the loop if 'q' is pressed
#         if cv2.waitKey(1) & 0xFF == ord("q"):
#             break
#     else:
#         # Break the loop if the end of the video is reached
#         break

# # Release the video capture object and close the display window
# cap.release()
# cv2.destroyAllWindows()
















