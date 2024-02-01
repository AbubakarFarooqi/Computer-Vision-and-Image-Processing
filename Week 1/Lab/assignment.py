import cv2 as ocv
import numpy as np

#Create an image with dimensions and chanels (1020,1040,3) and each channel
#can have integer value from 0 to 255
img1 = ocv.imread("D:/bscs/6th_Semester/CVIP/Week 1/Lab/1.png")
img2 = ocv.imread("D:/bscs/6th_Semester/CVIP/Week 1/Lab/2.png")
img3 = ocv.imread("D:/bscs/6th_Semester/CVIP/Week 1/Lab/3.png")
img4 = ocv.imread("D:/bscs/6th_Semester/CVIP/Week 1/Lab/4.png")

layer = np.zeros((1020,1040,3),dtype=np.uint8)

layer[3:503,3:503,:] = img1
layer[510:1010,3:503,:] = img2
layer[510:1010,510:1010,:] = img3
layer[3:503,510:1010,:] = img4

ocv.namedWindow("Collage", ocv.WINDOW_NORMAL)

ocv.imshow("Collage",layer)

ocv.resizeWindow("Collage", 1040, 1020)
ocv.waitKey(0)
