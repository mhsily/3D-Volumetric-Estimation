import numpy as np
import open3d as o3d
import cv2
import depthai as dai
import os
from pyntcloud import PyntCloud


_rgbPath = '/home/shubbu/images/rgbd/rgb/'
_depthPath = '/home/shubbu/images/rgbd/depth/'

os.chdir(_depthPath)

from pyntcloud.geometry.models.sphere import create_sphere
cloud = PyntCloud.from_file("sync.ply")
convex_hull_id = cloud.add_structure("convex_hull")
convex_hull = cloud.structures[convex_hull_id]
print(convex_hull.volume)