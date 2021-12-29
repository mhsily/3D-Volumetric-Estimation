#!/usr/bin/env python3
import numpy as np
import cv2

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
    preview_depth_images()
if __name__ == "__main__" :
	main()
	