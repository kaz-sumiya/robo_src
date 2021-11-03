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

import camera
import strategy
import analyzer

######################################################

class Bot(object):

    def __init__(self, cam, analyzer, strategy):
        self.cam = cam
        self.analyzer = analyzer
        self.strategy = strategy    
        self.vel_pub = rospy.Publisher('cmd_vel', Twist,queue_size=1)
        return


    def MainFunc(self):
        r = rospy.Rate(1000)
        while not rospy.is_shutdown():
            OBJs = self.cam.MainFunc()
            Cond = self.analyzer.MainFunc(OBJs)
            twist = self.strategy.MainFunc(Cond)
            self.vel_pub.publish(twist)
            r.sleep()
        return

######################################################

if __name__ == '__main__':
    rospy.init_node('GaZoo15')
    cam = camera.Camera( )
    analyzer = analyzer.Analyzer( )
    strategy = strategy.Random_Strategy("Random_Strategy")
    #strategy = strategy.Strategy_1("Strategy_1")
    bot = Bot(cam, analyzer, strategy)
    bot.MainFunc()


