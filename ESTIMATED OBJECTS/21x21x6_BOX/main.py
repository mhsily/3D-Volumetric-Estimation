# Disparity Range:
# 0  to 95 - Normal Mode
# 95 to 190 - Extended Mode

# Disparity to Depth:
# For 800P resultion =  882.5  * 7.5cm / Disparity (1280x800 Pixels images)
# For 400P resultion =  441.25 * 7.5cm / Disparity (640x400 Pixels images)


# Range in 800P with extended Disparity:
## Min - 34.835526316 cm
## Max - 73.541666667 cm

###########################################################################################################
###########################################################################################################
import numpy as np
import open3d as o3d
import cv2
import depthai as dai
import os
import time
from pyntcloud import PyntCloud

_Path = 'spatial-points/'
_minZ = 515   #in mm
_maxZ = 710   #in mm
_minX = -100   	#in mm			
_maxX = -_minX	#in mm			
_minY = -40   #in mm			
_maxY =  30   #in mm			
_objDist = 611
	
def _process(_point1, _point2, _point3, _point4):
	_coordinates_array = []
	for i in range(2500):
		_p1 = [_point1[i][0], _point1[i][1], _point1[i][2]]
		_p2 = [_objDist-_point2[i][2], _point2[i][1], _objDist+_point2[i][0]]
		_p3 = [-_point3[i][0],_point3[i][1], (_objDist+_objDist-_point3[i][2])]
		_p4 = [_point4[i][2]-_objDist, _point4[i][1], (_objDist-_point4[i][0])]
		if (_minX < _p1[0] < _maxX) and (_minY < _p1[1] < _maxY) and (_minZ < _p1[2] < _maxZ):
			_coordinates_array.append(_p1)   
		if (_minX < _p2[0] < _maxX) and (_minY < _p2[1] < _maxY) and (_minZ < _p2[2] < _maxZ):
			_coordinates_array.append(_p2)
		if (_minX < _p3[0] < _maxX) and (_minY < _p3[1] < _maxY) and (_minZ < _p3[2] < _maxZ):
			_coordinates_array.append(_p3)
		if (_minX < _p4[0] < _maxX) and (_minY < _p4[1] < _maxY) and (_minZ < _p4[2] < _maxZ):
			_coordinates_array.append(_p4)
	return np.array(_coordinates_array)

def _invert_image(_array):
	for i in range(_array.shape[0]):
		_array[i][0] = -_array[i][0]
		_array[i][1] = -_array[i][1]
	return np.array(_array)

def _visualize_points(_coordinates_array):
	_coordinates_array = np.array(_coordinates_array)
	_xMax, _xMin, _yMax, _yMin, _zMax = np.zeros(5)
	_zMin = 99999
	for i in range(_coordinates_array.shape[0]):
		_xMax = max([_coordinates_array[i][0], _xMax])
		_xMin = min([_coordinates_array[i][0], _xMin])
		_yMax = max([_coordinates_array[i][1], _yMax])
		_yMin = min([_coordinates_array[i][1], _yMin])
		_zMax = max([_coordinates_array[i][2], _zMax]) 
		_zMin = min([_coordinates_array[i][2], _zMin])
	_point_cloud = o3d.geometry.PointCloud()
	_point_cloud.points = o3d.utility.Vector3dVector(_coordinates_array)
	o3d.io.write_point_cloud("/home/shubbu/Desktop/3d_Estimations/point-cloud/complete.ply", _point_cloud)
	diamond = PyntCloud.from_file("/home/shubbu/Desktop/3d_Estimations/point-cloud/complete.ply")
	convex_hull_id = diamond.add_structure("convex_hull")
	convex_hull = diamond.structures[convex_hull_id]
	volume = convex_hull.volume
	print("\n Actual Dimensions of BOX (in CM):\n", 21,21,6)
	print("\n Estimated Dimensions of BOX (in CM): \n", abs(_xMax-_xMin)/10, abs(_yMax-_yMin)/10, abs(_zMax-_zMin)/10)
	print("\n Actual Volume of BOX (in CM Cube):\n", 21*21*6)
	print("\n Estimated Volume of BOX (in CM Cube):\n", volume/1000)
	print("\n Accurary = ", (volume/1000)/(21*21*6)*100, "\n")
	_pcd_load = o3d.io.read_point_cloud("/home/shubbu/Desktop/3d_Estimations/point-cloud/complete.ply")
	hull, _ = _pcd_load.compute_convex_hull()
	hull_ls = o3d.geometry.LineSet.create_from_triangle_mesh(hull)
	hull_ls.paint_uniform_color((1, 0, 0))
	o3d.visualization.draw_geometries([hull_ls, _pcd_load])
	#o3d.visualization.draw_geometries([_pcd_load])

def preview_depth_images():
    depth_0 = cv2.imread('depth-images/1.jpg')
    depth_1 = cv2.imread('depth-images/2.jpg')
    depth_2 = cv2.imread('depth-images/3.jpg')
    depth_3 = cv2.imread('depth-images/4.jpg')
    depth_images = np.concatenate((depth_0, depth_1, depth_2, depth_3), axis=1)
    depth_images = cv2.rotate(depth_images, cv2.ROTATE_180)
    depth_images = cv2.resize(depth_images, (1200,200))
    while True:
        cv2.imshow('Images', depth_images)
        if cv2.waitKey(1) == ord('q'):
            break   

def main():
	#preview_depth_images()
	os.chdir(_Path)
	_point1 = np.load('1.npy')
	_point2 = np.load('2.npy')
	_point3 = np.load('3.npy')
	_point4 = np.load('4.npy')
	print("\n 3D Coordinates Processing")
	_coordinates_array = _process(_invert_image(_point1), _invert_image(_point2), _invert_image(_point3), _invert_image(_point4))
	_visualize_points(_coordinates_array)

if __name__ == "__main__" :
	main()
	