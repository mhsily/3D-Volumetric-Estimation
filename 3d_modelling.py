import numpy as np
import open3d as o3d
import cv2
import depthai as dai
import os
import time

_rgbPath = '/home/shubbu/images/rgbd/rgb/'
_depthPath = '/home/shubbu/images/rgbd/depth/'

_minDepth = 100   #in mm
_maxDepth = 500   #in mm

def _filter_object(_img, _minDepth, _maxDepth):
	_imgShape = _img.shape
	_filteredDepth = np.zeros(_img.shape)
	for x in range(_imgShape[0]):
		for y in range(_imgShape[1]):
			if _minDepth < _img[x][y][0] < _maxDepth:
				_filteredDepth[x][y] = _img[x][y][0]
	return np.array(_filteredDepth)

def _3d_model(_front_image, _right_image, _rear_image, _left_image):
	_3d_array = np.zeros([400,640,640], dtype=int)

	for y in range(400):
		for x in range(640):
			z = int(_front_image[y][x][0])
			_3d_array[y][x][z] = 1
	for y in range(400):
		for x in range(640):
			z = int(_right_image[y][x][0])
			_3d_array[y][639-z][x] = 1
	for y in range(400):
		for x in range(640):
			z = int(_rear_image[y][x][0])
			_3d_array[y][639-x][639-z] = 1 
	for y in range(400):
		for x in range(640):
			z = int(_left_image[y][x][0])
			_3d_array[y][z][639-x] = 1
	
	return _3d_array

def _3d_array_to_coordinates(_3d_array):
	_coordinates_array = []
	for x in range(640):
		for y in range(400):
			for z in range(640):
				if _3d_array[y][x][z]==1:
					_coordinates_array.append([x, y, z])
	_coordinates_array = np.array(_coordinates_array)
	return _coordinates_array

def _visualize_points(_coordinates_array):
	_point_cloud = o3d.geometry.PointCloud()
	_point_cloud.points = o3d.utility.Vector3dVector(_coordinates_array)
	o3d.io.write_point_cloud("sync.ply", _point_cloud)
	_pcd_load = o3d.io.read_point_cloud("sync.ply")
	o3d.visualization.draw_geometries([_pcd_load])

def main():
	os.chdir(_depthPath)
	_depth0 = cv2.imread('0.png')
	_depth1 = cv2.imread('1.png')
	_depth2 = cv2.imread('2.png')
	_depth3 = cv2.imread('3.png')
	print("\n Images Loaded")

	_front_image = _filter_object(_depth0, _minDepth, _maxDepth)
	_right_image = _filter_object(_depth1, _minDepth, _maxDepth)
	_rear_image  = _filter_object(_depth2, _minDepth, _maxDepth)
	_left_image  = _filter_object(_depth3, _minDepth, _maxDepth)
	print("\n Object Filtered")

	_3d_array = _3d_model(_front_image, _right_image, _rear_image, _left_image)
	print("\n 3D Array Created")

	_coordinates_array = _3d_array_to_coordinates(_3d_array)
	print("\n Coordinated Fetched")

	_visualize_points(_coordinates_array)

if __name__ == "__main__" :
	main()
	