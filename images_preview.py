import numpy as np
import cv2
import os

def main():
    rgb_path = '/home/shubbu/images/rgbd/rgb/'
    depth_path = '/home/shubbu/images/rgbd/depth/'
    
    min = 200   #in mm
    max = 500   #in mm
    
    os.chdir(rgb_path)
    rgb_0 = cv2.imread('001.jpg')
    rgb_1 = cv2.imread('002.jpg')
    rgb_2 = cv2.imread('003.jpg')
    rgb_3 = cv2.imread('004.jpg')
    
    os.chdir(depth_path)
    depth_0 = cv2.imread('001_normalized.png')
    depth_1 = cv2.imread('002_normalized.png')
    depth_2 = cv2.imread('003_normalized.png')
    depth_3 = cv2.imread('004_normalized.png')
    
    rgb_images = np.concatenate((rgb_0, rgb_1, rgb_2, rgb_3), axis=1)
    rgb_images = cv2.rotate(rgb_images, cv2.ROTATE_180)
    rgb_images = cv2.resize(rgb_images, (1200,200))

    depth_images = np.concatenate((depth_0, depth_1, depth_2, depth_3), axis=1)
    depth_images = cv2.rotate(depth_images, cv2.ROTATE_180)
    depth_images = cv2.resize(depth_images, (1200,200))

    images = np.concatenate((rgb_images, depth_images), axis=0)
    
    while True:
        cv2.imshow('Images', images)
        if cv2.waitKey(1) == ord('q'):
            break   

if __name__ == "__main__" :
	main()
	