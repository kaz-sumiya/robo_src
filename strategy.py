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



class state(object):
    def __init__(self, name):
        self.name = name
        self.cnt = 0
        return
        
    def MainFunc(self, Cond): 
        self.cnt += 1
	#print(self.name, "  ", self.cnt)        
        return


        

class stateNomal(state):
    def __init__(self, name):
        super(stateNomal, self).__init__(name)
	return
        
    def MainFunc(self, Cond): 
        super(stateNomal, self).MainFunc(Cond)
        
	if Cond["enemy"] is not []
	    print Cond["enemy"]
	

        
	return "Go1"
   	   	

class stateAttack(state):
    def __init__(self, name):
        super(stateNomal, self).__init__(name)
        lostcnt = 0
	return
        
    def MainFunc(self, Cond): 
        super(stateNomal, self).MainFunc(Cond)
        
	if Cond["enemy"] is not []
	    lostcnt += 1
	    
	

        
	return "Stop"


   

######################################################




class Strategy(object):
    def __init__(self, name):
        self.name = name

        twistStop = Twist()
        twistGo1 = Twist()
        twistGo2 = Twist()
        twistBack = Twist()      
        twistTurnR = Twist()      
        twistTurnL = Twist()      

        twistStop.linear.x = 0; twistStop.linear.y = 0; twistStop.linear.z = 0
        twistStop.angular.x = 0; twistStop.angular.y = 0; twistStop.angular.z = 0

        twistGo1.linear.x = 0.1; twistGo1.linear.y = 0; twistGo1.linear.z = 0
        twistGo1.angular.x = 0; twistGo1.angular.y = 0; twistGo1.angular.z = 0

        twistGo2.linear.x = 0.2; twistGo2.linear.y = 0; twistGo2.linear.z = 0
        twistGo2.angular.x = 0; twistGo2.angular.y = 0; twistGo2.angular.z = 0

        twistBack.linear.x = -0.1; twistBack.linear.y = 0; twistBack.linear.z = 0
        twistBack.angular.x = 0; twistBack.angular.y = 0; twistBack.angular.z = 0

        twistTurnR.linear.x = 0; twistTurnR.linear.y = 0; twistTurnR.linear.z = 0
        twistTurnR.angular.x = 0; twistTurnR.angular.y = 0; twistTurnR.angular.z = 1

        twistTurnL.linear.x = 0; twistTurnL.linear.y = 0; twistTurnL.linear.z = 0
        twistTurnL.angular.x = 0; twistTurnL.angular.y = 0; twistTurnL.angular.z = -1

	self.twistDict = {"Stop":twistStop, "Go1":twistGo1,  "Go2":twistGo2, "Back":twistBack,
	 "TurnR":twistTurnR,  "TurnL":twistTurnL}  

	return

    def MainFunc(self, Cond):
    	#print(self.name,  "-------------")
    	pass

    def debud_log(self, str, twist):
	#print(str)
	#print(twist)    	
    	return;

############
class Strategy_1(Strategy):
    def __init__(self, name):
        super(Strategy_1, self).__init__(name)
        self.cur = stateNomal
	self.curState = stateNomal("stateNomal")
	self.preState = self.curState.copy()
	return
	
    def MainFunc(self, Cond):
        super(Strategy_1, self).MainFunc(Cond)
    	next, action = self.curState.MainFunc(Cond)
 
        self.changeState(next) 
 
	twist = self.twistDict[action]
	
	self. debud_log(ret, twist)
        return twist


    def changeState(self, next):
        if self.cur == next:
            return
            
        self.cur = next
	self.preState = self.curState
        if next == "stateNomal"    
	    self.curState = stateNomal("stateNomal")
	elif next == "stateAttack"
	    self.curState = stateAttack("stateAttack")   



############
class Random_Strategy(Strategy):
    def __init__(self, name):
        super(Random_Strategy, self).__init__(name)
        return

    def MainFunc(self, Cond):
        super(Random_Strategy, self).MainFunc(Cond)
	value = random.randint(1,1400)
        if value < 200:
            str = "Stop"
        elif value < 400:
            str = "Go1"
        elif value < 600:
            str = "Go2"
        elif value < 800:
            str = "Back"
        elif value < 1200:
            str = "Stop" 
            #str = "TurnR"
        else:
            str = "Stop" 
            #str = "TurnL"

        twist = self.twistDict[str]
        
	self. debud_log(str, twist)
        return twist


if __name__ == '__main__':
    strategy = Strategy()
    strategy.MainFunc()


