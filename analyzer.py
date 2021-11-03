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



class Introduction( ):
    def __init__(self, target ):
    	self.x, self.y, self.w, self.h = cv2.boundingRect(target)
    	self.cx = self.x + self.w/2
    	self.cy = self.y + self.h/2
    	self.size = int(cv2.contourArea(target))    	
    	self.dir = ""
    	self.dist = ""
    	self.tgtdir = ""
    	self.etc = ""
	pass 


    def devide3(self, val, th, ret):
	if val < th[0]:
	    return ret[0]
	elif val < th[1]:
	    return ret[1]
	else:
	    return ret[2]


    def debugprint(self, str):
	print( str, self.x, self.y, self.w, self.h, self.cx, self.cy, self.size, self.dir, self.dist, self.tgtdir, self.etc)  
	return


######################################################


class Analyzer(object):

    def __init__(self):
	pass


    def MainFunc(self, OBJs):
    	#print(self.name,  "-------------")
    	
    	enemy = self.find_Enemy(OBJs)
    	target = self.find_Target(OBJs["blue"])    	
    	bump = self.find_Bump(OBJs["yellow"]) 
	wall = self.find_Wall(OBJs["black"]) 
    	

	#if len(enemy) > 0:
	#    print("enemy", enemy) 
    	    
	#for obj in target:
	#    obj.debugprint("target")
	#for obj in bump:
	#    obj.debugprint("bump")	    
	#for obj in wall:
	#    obj.debugprint("wall")	    

	return {"enemy":enemy, "target":target, "bump":bump, "wall":wall}


    def find_Target(self,targets):
        if len(targets)==0:
            return []

	tgts = []
	for target in targets:
	    intro = Introduction(target)  
	    intro.dir = intro.devide3(intro.cx, (80-20, 80+20), ("Left", "Center", "Right"))
	    intro.dist = intro.devide3(intro.h, (40, 50), ("Far", "Middle", "Near"))
	    intro.tgtdir = intro.devide3(intro.h/intro.w, (1.4, 2.0), ("Front", "Mid", "Diag"))	
	    tgts.append(intro)
	return tgts
	

    def find_Bump(self,bumps):
        if len(bumps)==0:
            return []

	intro = Introduction(bumps[0])  
        intro.dir = intro.devide3(intro.cx, (80-20, 80+20),  ("Left", "Center", "Right"))
	intro.dist = intro.devide3(intro.cy, (90, 110), ("Far", "Middle", "Near"))
	return [intro]


    def find_Wall(self,walls):
        if len(walls)==0:
            return []
        
    	intro = Introduction(walls[0])      
        
	if intro.w < 80:
	    return []
	    
	if intro.w / intro.h < 3:
	    return []   
	
	if intro.w>130:
	    intro.dir = "C"
	elif intro.cx <160:
	    intro.dir = "L"
	else:
	    intro.dir = "R"
     
	return [intro]




    def find_EnemyRed(self,enemy):
        if len(enemy)==0:
            return []

	intro = Introduction(enemy[0])  
	intro.dir = intro.devide3(intro.cx, (80-20, 80+20),  ("Left", "Center", "Right"))
	intro.dist = intro.devide3(intro.cy, (15, 30), ("Near", "Middle", "Far"))
	return [intro]
    
    def find_Checker(self, cx, cy, circle):
        if len(circle)==0:
            return False

	for rect in circle:
      	    x, y, w, h = cv2.boundingRect(rect)	
	    if x < cx < x+w and y < cy < y*h:
	        return True
	        
	return False        


    def find_EnemyBlack(self,OBJs):
        enemy = OBJs["black"]
        
        if len(enemy)==0:
            return []

	tgts = []
	for rect in enemy:
	    intro = Introduction(rect)  
	
	    if intro.w / intro.h > 1.5:
	        continue
	        
	    ret1 = self.find_Checker(intro.cx, intro.cy, OBJs["blue"])
	    ret2 = self.find_Checker(intro.cx, intro.cy, OBJs["green"])
	    if ret1 or ret2:
	        continue

	    tgts.append(intro)

        return tgts
        


    def find_Enemy(self,OBJs):
	green = self.find_Target(OBJs["green"]);
	red = self.find_EnemyRed(OBJs["red"]);	
	black = self.find_EnemyBlack(OBJs);
	
	"""
	for obj in green:
	    obj.debugprint("enemyG")	
	for obj in red:
	    obj.debugprint("enemyR")	
	for obj in black:
	    obj.debugprint("enemyK")	
	"""
	
	if len(green) > 0:
	    if len(green) ==1:
	    	if green[0].tgtdir == "Diag":
	    	    tgtdir = "Front"
	    	else:
	            tgtdir = "SorR"
	    else:
	        tgtdir = "SandR"
	    return [green[0].dir, green[0].dist, tgtdir, "Green"]
	    
	if len(red) > 0:
	    tgtdir = "Unknown"      	    
	    for bk in black:
	    	if bk.cx-bk.w < red[0].x < bk.cx+bk.w and bk.y-bk.h < red[0].y < bk.y:
	    	    tgtdir = "FandS"
	    	    break
	    return [red[0].dir, red[0].dist, tgtdir, "Red"]	    
	    
	if len(black) > 0:    
	    if black[0].size > 5000:
	        return ["Center", "Near", "Front", "Black"]	    	

	return []    
  	 

    	
	



if __name__ == '__main__':
    analyzer = Analyzer()
    analyzer.MainFunc()


