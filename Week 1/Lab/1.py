import cv2
import numpy as np
image = cv2.imread("D:\\rgb.png")
print(image.shape)
# print(image[66,37])
z=np.zeros((image.shape[0],image.shape[1]))
# image[:,:,0]=z
# image[:,:,2]=z
b=image[:,:,0]
print(b)
g=image[:,:,1]
r=image[0:146,:,2]
image[354:,:,0] = r
# image[354:,:,2] = b

# roi=image[0:100,0:200,:]
# image[250:350,50:250,:]=roi

cv2.imshow("test",g)
# cv2.imshow("test",image)
# cv2.imshow("b",b)
# cv2.imshow("g",g)
cv2.waitKey(0)