import numpy as np
import open3d as o3d
import cv2
import depthai as dai
import os
import time

if __name__ == "__main__" :

	rgb_path = '/home/shubbu/images/rgbd/rgb/'
	depth_path = '/home/shubbu/images/rgbd/depth/'

	# Closer-in minimum depth, disparity range is doubled (from 95 to 190):
	extended_disparity = True
	# Better accuracy for longer distance, fractional disparity 32-levels:
	subpixel = False
	# Better handling for occlusions:
	lr_check = True

	# Create pipeline
	pipeline = dai.Pipeline()

	# Define sources and outputs
	monoLeft = pipeline.createMonoCamera()
	monoRight = pipeline.createMonoCamera()
	depth = pipeline.createStereoDepth()
	xoutDepth = pipeline.createXLinkOut()
	xoutDepth.setStreamName("disparity")

	camRgb = pipeline.createColorCamera()
	xoutRgb = pipeline.createXLinkOut()
	xoutRgb.setStreamName("rgb")

	# Properties
	monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_800_P)
	monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
	monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_800_P)
	monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)

	camRgb.setPreviewSize(1280, 800)
	camRgb.setInterleaved(False)
	camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)
	
	depth.setExtendedDisparity(extended_disparity)
	# Create a node that will produce the depth map (using disparity output as it's easier to visualize depth this way)
	depth.initialConfig.setConfidenceThreshold(200)
	# Options: MEDIAN_OFF, KERNEL_3x3, KERNEL_5x5, KERNEL_7x7 (default)
	depth.initialConfig.setMedianFilter(dai.MedianFilter.KERNEL_7x7)
	depth.setLeftRightCheck(lr_check)
	depth.setSubpixel(subpixel)


	# Linking
	monoLeft.out.link(depth.left)
	monoRight.out.link(depth.right)
	depth.disparity.link(xoutDepth.input)

	camRgb.preview.link(xoutRgb.input)


	# Connect to device and start pipeline
	with dai.Device(pipeline) as device:
		# Output queue will be used to get the depth frames from the outputs defined above
		qDepth = device.getOutputQueue(name="disparity", maxSize=4, blocking=False)
		qRgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
		while True:
			inDepth = qDepth.get()  # blocking call, will wait until a new data has arrived
			frameDepth = inDepth.getFrame()
			inRgb = qRgb.get()
			frameRGB = inRgb.getCvFrame()
			# Normalization for better visualization
			#maxDepth = max(map(max,frameDepth))
			normalized_frame = (frameDepth * (255 / depth.getMaxDisparity())).astype(np.uint8)

			# Available color maps: https://docs.opencv.org/3.4/d3/d50/group__imgproc__colormap.html
			color_frameDepth = cv2.applyColorMap(normalized_frame, cv2.COLORMAP_JET)
			cv2.line(color_frameDepth, (640,0), (640,800), (0, 255, 0), 1)
			cv2.line(color_frameDepth, (0,400), (1280,400), (0, 255, 0), 1)
			cv2.imshow("depth_color", color_frameDepth)

			color_frameRGB = frameRGB
			cv2.line(color_frameRGB, (640,0), (640,800), (0, 255, 0), 1)
			cv2.line(color_frameRGB, (0,400), (1280,400), (0, 255, 0), 1)
			cv2.imshow("rgb", color_frameRGB)

			key = cv2.waitKey(1)
			if key == ord('1'):
				os.chdir(rgb_path)
				cv2.imwrite('001.jpg', frameRGB)
				os.chdir(depth_path)
				cv2.imwrite('001_normalized.png', normalized_frame)
				np.save('001.npy',frameDepth)
				print("\n 1 Captured")

			elif key == ord('2'):
				os.chdir(rgb_path)
				cv2.imwrite('002.jpg', frameRGB)
				os.chdir(depth_path)
				cv2.imwrite('002_normalized.png', normalized_frame)
				np.save('002.npy',frameDepth)
				print("\n 2 Captured")

			elif key == ord('3'):
				os.chdir(rgb_path)
				cv2.imwrite('003.jpg', frameRGB)
				os.chdir(depth_path)
				cv2.imwrite('003_normalized.png', normalized_frame)
				np.save('003.npy',frameDepth)
				print("\n 3 Captured")

			elif key == ord('4'):
				os.chdir(rgb_path)
				cv2.imwrite('004.jpg', frameRGB)
				os.chdir(depth_path)
				cv2.imwrite('004_normalized.png', normalized_frame)
				np.save('004.npy',frameDepth)
				print("\n 4 Captured")

			# break or exit condition
			elif key == ord('q'):
				break