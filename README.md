# 3D Volumetric Estimation
In this project we are going to estimate Volume of object using a stereo camera (OAK-D).
For documentation about OAK-D, visit OAK-D repository at https://github.com/mhsily/

## RGBD Image
An RGBD Image is data structure made using a RGB image and a depth Image of same frame and both images have same resolution. 
Every pixel in the RGB image have their distance value stored in depth image at the same pixel location.

## Depth Image
### Disparity Image
**Disparity image** is created using stereo camera, where every pixel is the distance between two corresponding points taken from left and right stereo pair.

The value of each pixel in disparity image is inversely proportional to the distance between scene() and camera.

Disparity Image are created using a stereo camera where the color of pixel is proportional to the disparity. 

### Normalization of Disparity Image
To visualize different depths or disparities using colors, we need to normalize values such that the maximum value is 255.

Consider, we are normalizing disparity image to visualize. 

So, 
<img src="https://render.githubusercontent.com/render/math?math=normalized\_frame = \frac{disparity\_frame}{max\_disparity} \times 255">

(**Note**:- You will need max disparity distance to gain back disparity or depth of points.)

### Depth calculation
Consider, the disparity of a particular point is ```disparity``` , the distance between both camera's is ```baseline``` and the focal length of the camera is ```focal_length```.
(**Note**: Both camera's have same specifications)

Then the depth ```depth``` is given by,

<img src="https://render.githubusercontent.com/render/math?math=depth = \frac{baseline \times focal\_length}{disparity}">

(**Note**: This is a simplified formula for depth, but for proper block matching please read ***~~link here~~*** )


## 2D Array of Points
This is a basic 2D array, which is collection of co-ordinates of points in the image. 
This co-ordinates contains all three axes that is X, Y, Z.
The X and Y co-ordinates are same co-ordinates that of pixel and the Z co-ordinate here is the depth of that particular pixel taken from the depth image.

```python
import numpy as np
import cv2

depth_img = cv2.imread('depth_image.jpg')
depth_img = depth_img[:, :, 1] # Trim 

img_shape = depth_img.shape
points_array = [] 

for x in range(img_shape[0]):
	for y in range(img_shape[1]):
		z = depth_img[x][y]
		temp = [x, y, z]
		points_array.append(temp)
points_array = np.array(points_array)

print('2D Array of Vertices has been created')
print(points_array)
```