# Disparity Range:
# 0  to 95 - Normal Mode
# 95 to 190 - Extended Mode

# Disparity to Depth:
# For 800P resultion =  882.5  * 7.5cm / Disparity (1280x800 Pixels images)
# For 400P resultion =  441.25 * 7.5cm / Disparity (640x400 Pixels images)


# Range in 800P with extended Disparity:
## Min - 34.835526316 cm
## Max - 73.541666667 cm




import numpy as np
import open3d as o3d
import cv2
import depthai as dai
import os
import time

_rgbPath = '/home/shubbu/images/rgbd/rgb/'
_depthPath = '/home/shubbu/images/rgbd/depth/'

_minDepth = 165   #in mm
_maxDepth = 170   #in mm

_minLength = 100   #in pixels			
_maxLength = 100   #in pixels			

_minBreadth = 200   #in pixels			
_maxBreadth = 200   #in pixels			
	

_centerCamDistance = 215
# Center Coordinates are 0,0,0

def _filter_object(_img, _minDepth, _maxDepth):
	_imgShape = _img.shape
	_filteredDepth = np.zeros(_img.shape)
	for x in range(_imgShape[0]):
		for y in range(_imgShape[1]):
			if _minDepth < _img[x][y]< _maxDepth:
				_filteredDepth[x][y] = _img[x][y]
	return np.array(_filteredDepth)

def _depth_to_3d_coordinates(_front_image, _right_image, _rear_image, _left_image):
	_coordinates_array = []
	for y in range(400-_minLength, 400+_maxLength):
		for x in range(640-_minBreadth, 640+_maxBreadth):
			z1 = _front_image[y][x]
			z2 = _right_image[y][x]
			z3 = _rear_image[y][x]
			z4 = _left_image[y][x]
			
			if _minDepth<z1<_maxDepth:
				_coordinates_array.append([x-640, y+400, z1-_centerCamDistance])
			if _minDepth<z2<_maxDepth:
			 	_coordinates_array.append([_centerCamDistance-z2, y+400, x-640])
			if _minDepth<z3<_maxDepth:
				_coordinates_array.append([640-x, y+400, _centerCamDistance-z3])
			if _minDepth<z4<_maxDepth:
			 	_coordinates_array.append([z4-_centerCamDistance, y+400, 640-x])	
	return _coordinates_array

def _visualize_points(_coordinates_array):
	_point_cloud = o3d.geometry.PointCloud()
	_point_cloud.points = o3d.utility.Vector3dVector(_coordinates_array)
	o3d.io.write_point_cloud("sync.ply", _point_cloud)
	_pcd_load = o3d.io.read_point_cloud("sync.ply")
	
	hull, _ = _pcd_load.compute_convex_hull()
	hull_ls = o3d.geometry.LineSet.create_from_triangle_mesh(hull)
	hull_ls.paint_uniform_color((1, 0, 0))
	o3d.visualization.draw_geometries([hull_ls, _pcd_load])



	#o3d.visualization.draw_geometries([_pcd_load])

def _invert_image (_img):
	_imgShape = _img.shape
	_invertedImage = np.zeros(_img.shape)
	for x in range(_imgShape[0]):
		for y in range(_imgShape[1]):
				_invertedImage[x][y] = _img[_imgShape[0]-x-1][_imgShape[1]-y-1]
	return np.array(_invertedImage)


def main():
	os.chdir(_depthPath)
	_depth1 = np.load('001.npy')
	_depth2 = np.load('002.npy')
	_depth3 = np.load('003.npy')
	_depth4 = np.load('004.npy')
	print("\n Images Loaded")

	# _front_image = _filter_object(_invert_image(_depth1), _minDepth, _maxDepth)
	# _right_image = _filter_object(_invert_image(_depth2), _minDepth, _maxDepth)
	# #_right_image = None
	# _rear_image  = _filter_object(_invert_image(_depth3), _minDepth, _maxDepth)
	# _left_image  = _filter_object(_invert_image(_depth4), _minDepth, _maxDepth)
	# #_left_image = None
	# print("\n Object Filtered")

	_coordinates_array = _depth_to_3d_coordinates(_front_image, _right_image, _rear_image, _left_image)
	print("\n 3D Coordinates Created")

	_visualize_points(_coordinates_array)

if __name__ == "__main__" :
	main()
	