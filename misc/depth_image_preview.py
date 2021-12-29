import numpy as np
import open3d as o3d
import cv2
import depthai as dai
import os



def maximumof(array):
    return max(array.ravel())


_rgbPath = '/home/shubbu/images/rgbd/rgb/'
_depthPath = '/home/shubbu/images/rgbd/depth/'

os.chdir(_depthPath)
_depth0 = np.load('001.npy')


os.chdir("/home/shubbu/Desktop/spatial-points")
_depth0 = np.load('1.npy')


array = _depth0
# for x in range(1280):
# 	for y in range(800):
# 		array.append([x,y,_depth0[y][x]])

_point_cloud = o3d.geometry.PointCloud()
_point_cloud.points = o3d.utility.Vector3dVector(array)
o3d.io.write_point_cloud("test.ply", _point_cloud)
_pcd_load = o3d.io.read_point_cloud("test.ply")
o3d.visualization.draw_geometries([_pcd_load])