#!/usr/bin/env python3

import cv2
import depthai as dai
import time

step = 10

newConfig = False

# Create pipeline
pipeline = dai.Pipeline()

# Define sources and outputs
monoLeft = pipeline.create(dai.node.MonoCamera)
monoRight = pipeline.create(dai.node.MonoCamera)
stereo = pipeline.create(dai.node.StereoDepth)
spatialLocationCalculator = pipeline.create(dai.node.SpatialLocationCalculator)

xoutDepth = pipeline.create(dai.node.XLinkOut)
xoutSpatialData = pipeline.create(dai.node.XLinkOut)
xinSpatialCalcConfig = pipeline.create(dai.node.XLinkIn)

xoutDepth.setStreamName("depth")
xoutSpatialData.setStreamName("spatialData")
xinSpatialCalcConfig.setStreamName("spatialCalcConfig")

# Properties
monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)

lrcheck = False
subpixel = False

stereo.initialConfig.setConfidenceThreshold(255)
stereo.setLeftRightCheck(lrcheck)
stereo.setSubpixel(subpixel)

# Config
topLeft = dai.Point2f(0.1, 0.1)
bottomRight = dai.Point2f(0.1 + (0.8/step), 0.1 + (0.8/step))

config = dai.SpatialLocationCalculatorConfigData()
config.depthThresholds.lowerThreshold = 100
config.depthThresholds.upperThreshold = 10000
config.roi = dai.Rect(topLeft, bottomRight)

spatialLocationCalculator.setWaitForConfigInput(False)
spatialLocationCalculator.initialConfig.addROI(config)

# Linking
monoLeft.out.link(stereo.left)
monoRight.out.link(stereo.right)

spatialLocationCalculator.passthroughDepth.link(xoutDepth.input)
stereo.depth.link(spatialLocationCalculator.inputDepth)

spatialLocationCalculator.out.link(xoutSpatialData.input)
xinSpatialCalcConfig.out.link(spatialLocationCalculator.inputConfig)

points=[]
# Connect to device and start pipeline
with dai.Device(pipeline) as device:

	# Output queue will be used to get the depth frames from the outputs defined above
	depthQueue = device.getOutputQueue(name="depth", maxSize=4, blocking=False)
	spatialCalcQueue = device.getOutputQueue(name="spatialData", maxSize=4, blocking=False)
	spatialCalcConfigInQueue = device.getInputQueue("spatialCalcConfig")

	color = (255, 255, 255)

	inDepth = depthQueue.get() # Blocking call, will wait until a new data has arrived
	time.sleep(4)
	depthFrame = inDepth.getFrame()
	depthFrameColor = cv2.normalize(depthFrame, None, 255, 0, cv2.NORM_INF, cv2.CV_8UC1)
	depthFrameColor = cv2.equalizeHist(depthFrameColor)
	depthFrameColor = cv2.applyColorMap(depthFrameColor, cv2.COLORMAP_HOT)

	
	for _ in range(0,10):
		for _ in range(0,10):
			config.roi = dai.Rect(topLeft, bottomRight)
			config.calculationAlgorithm = dai.SpatialLocationCalculatorAlgorithm.AVERAGE
			cfg = dai.SpatialLocationCalculatorConfig()
			cfg.addROI(config)
			spatialCalcConfigInQueue.send(cfg)

			spatialData = spatialCalcQueue.get().getSpatialLocations()
			for depthData in spatialData:
				roi = depthData.config.roi
				roi = roi.denormalize(width=depthFrameColor.shape[1], height=depthFrameColor.shape[0])
				xmin = int(roi.topLeft().x)
				ymin = int(roi.topLeft().y)
				xmax = int(roi.bottomRight().x)
				ymax = int(roi.bottomRight().y)
				depthMin = depthData.depthMin
				depthMax = depthData.depthMax
				fontType = cv2.FONT_HERSHEY_TRIPLEX
				cv2.rectangle(depthFrameColor, (xmin, ymin), (xmax, ymax), color, cv2.FONT_HERSHEY_SCRIPT_SIMPLEX)
				cv2.putText(depthFrameColor, f"X: {int(depthData.spatialCoordinates.x)} mm", (xmin + 10, ymin + 20), fontType, 0.05, 255)
				cv2.putText(depthFrameColor, f"Y: {int(depthData.spatialCoordinates.y)} mm", (xmin + 10, ymin + 35), fontType, 0.05, 255)
				cv2.putText(depthFrameColor, f"Z: {int(depthData.spatialCoordinates.z)} mm", (xmin + 10, ymin + 50), fontType, 0.05, 255)

				points.append([depthData.spatialCoordinates.x, depthData.spatialCoordinates.y, depthData.spatialCoordinates.z])
			topLeft.y += (0.8/step)
			bottomRight.y += (0.8/step)
		topLeft.y = 0.1
		bottomRight.y = 0.1 + (0.8/step)
		topLeft.x += (0.8/step)
		bottomRight.x += (0.8/step)

cv2.imwrite("depth.jpg", depthFrameColor)
print(points)