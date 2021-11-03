#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.dont_write_bytecode = True

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError
import cv2
import random
import numpy as np



class Camera(object):

    def __init__(self):
        cols = 640
        rows = 480
        self.img = np.full((rows, cols, 3), 0, dtype=np.uint8)
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber('image_raw', Image, self.imageCallback)
	return


    def imageCallback(self, data):
        try:
            self.img = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            rospy.logerr(e)
	return


    def MainFunc(self):
        bgr_image = self.img
        half_image = cv2.resize(bgr_image, dsize=(160, 120))
        hsv_image = cv2.cvtColor(half_image, cv2.COLOR_BGR2HSV)
        #cv2.imshow("Image ", half_image)
        kernel = np.ones((3, 5), np.uint8)

	OBJs_red = None
	OBJs_green = None
	OBJs_yellow = None
	OBJs_blue = None
	        
        lower = np.array([0,64,0]) # red
        upper = np.array([8,255,255]) # red
        mask_image1 = cv2.inRange(hsv_image, lower, upper)
        lower = np.array([247,64,0]) # red
        upper = np.array([255,255,255]) # red
        mask_image2 = cv2.inRange(hsv_image, lower, upper)
        mask_red = mask_image1 + mask_image2
        OBJs_red = self.find_OBJs(mask_red, None, 1)
        self.dedug_show_Objs("red", OBJs_red, mask_red, half_image)
	
        lower = np.array([40, 100, 50]) # green
        upper = np.array([60, 255, 255]) # green
        mask_green = cv2.inRange(hsv_image, lower, upper)
        OBJs_green = self.find_OBJs(mask_green, None, 1)
        self.dedug_show_Objs("green", OBJs_green, mask_green, half_image)
	
        lower = np.array([30, 100, 50]) # yellow
        upper = np.array([50, 255, 255]) # yellow
        mask_yellow = cv2.inRange(hsv_image, lower, upper)
        OBJs_yellow = self.find_OBJs(mask_yellow, None, 100)
        self.dedug_show_Objs("yellow", OBJs_yellow, mask_yellow, half_image)
	        
        lower = np.array([120, 40, 10]) # blue
        upper = np.array([140, 255, 255]) # blue
        mask_blue = cv2.inRange(hsv_image, lower, upper)
        OBJs_blue = self.find_OBJs(mask_blue, None, 49)
        self.dedug_show_Objs("blue", OBJs_blue, mask_blue, half_image)
       
        lower = np.array([0, 0, 0]) # black
        upper = np.array([255,255,50]) # black
        mask_black = cv2.inRange(hsv_image, lower, upper)
        OBJs_black = self.find_OBJs(mask_black, kernel, 49)
        self.dedug_show_Objs("black", OBJs_black, None, half_image)

        return {"red":OBJs_red, "green":OBJs_green, "yellow":OBJs_yellow, "blue":OBJs_blue, "black":OBJs_black}


    def find_OBJs(self, mask, kernel, size):
    
    	if kernel is not None:
            mask = cv2.erode(mask, kernel, iterations=1)

    	labels, contours, hierarchy =cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
	if len(contours) == 0:    	
	    return []

	contours = [ contour for contour in contours if cv2.contourArea(contour) > size]     
	contours.sort(key=lambda x: cv2.contourArea(x), reverse=True)	
       	        
        return contours        
                

    def dedug_show_Objs(self, title, contours, mask, Image):
        if mask is not None:
            Image = cv2.bitwise_and(Image, Image, mask=mask)

	for i in range(0, len(contours)):
            #cv2.polylines(Image, contours[i], True, (255, 255, 255), 1)
            rect = contours[i]	
      	    x, y, w, h = cv2.boundingRect(rect)
            cv2.rectangle(Image, (x, y), (x + w, y + h), (255, 255, 255), 1)
            
        cv2.imshow(title, Image)
        cv2.waitKey(1)
	return


if __name__ == '__main__':
    cam = Camera( )



