# OAK-D (OpenCV AI Kit - D)
OAK-D is a spatial AI powerhouse, capable of simultaneously running advanced neural networks while providing depth from two stereo cameras and color information from a single 4K camera in the center.

**Applications using OAK/OAK-D** :

 - Social Distancing and Mask Detection.
 - 3D Reconstruction and Estimations.
 - Collision Detection for Unmanned Vehicles and other Vehicles.
 - 6D Human Posture Estimation and Gaze detection.

## DepthAI
DepthAI is a special C++ library created by Luxonis to work with OAK or OAK-D. DepthAI API is only provided for Python and C++ .
For more documentation, visit https://docs.luxonis.com/

### DepthAI - Python API
In Luxonis GitHub depthai-python repository, there are a brief explanation about different programs using OAK or OAK-D. 
Luxonis GitHub repository, https://github.com/luxonis/depthai-python

## Architecture
<a href="https://ibb.co/PwQyGSB"><img src="https://i.ibb.co/6gBS0d6/architecture.png" alt="architecture" border="0"></a>

This is a basic architecture of OAK camera Pipeline, which includes nodes for Camera, Neural Network and their communication linking.
### Pipeline
- Pipeline is the complete structure, which includes nodes and their connecting links.
- Generally, Pipeline contains 5 nodes and 4 links.
- After creating Pipeline, user needs to upload it to the device that is OAK device. 

### Input / Output Queue
- Input or Output at the end Xlink nodes is in a queue.
- Default Max Size of Queue = 30 and Non-Blocking Mode.
- There are 2 behaviors of Queue (Blocking and Non-Blocking).
- To use device for instant we use Max Size = 1 and Non-Blocking mode.
#### Blocking mode
In blocking mode, it blocks all new entry to the queue when it is full. 
#### Non-Blocking mode
In Non-Blocking Mode, it will erase to older entry in the queue to add newest when queue is full.

### Initialization and Uploading
Basic flow for initialization and declaration of Pipeline to OAK-D
 1. Declare Pipeline
 2. Define Pipeline : 
	- Create Nodes and Links
	- Define .blob models for neural network node
3. Upload Pipeline to Device (OAK-D)

For more documentation, visit https://docs.luxonis.com/
For python examples, https://github.com/luxonis/depthai-python/tree/main/examples


(**Note**:- If you are using python examples for first time, please install required libraries, shown on https://docs.luxonis.com/)


# RGBD Image
An RGBD Image is data structure made using a RGB image and a depth Image of same frame and both images have same resolution. Every pixel in the RGB image have their distance value stored in depth image at the same pixel location.

# Depth Image to 3D Point Cloud
## What is Disparity Image?
**Disparity image** is created using stereo camera, where every pixel is the distance between two corresponding points taken from left and right stereo pair.

The value of each pixel in disparity image is inversely proportional to the distance between scene() and camera.

Disparity Image are created using a stereo camera where the color of pixel is proportional to the disparity. 

## Normalization of Disparity Image
To present different depths using colors, we need to normalize depth values such that the maximum value is 255.
So, we simply

<img src="https://render.githubusercontent.com/render/math?math=normalized\_frame = \frac{disparity\_frame}{max\_disparity} \times 255">

Using OpenCV we read this normalized image and it is exactly called as **Depth Image**.

(**Note**:- You will need max disparity distance to gain back disparity or depth of points.)

#
