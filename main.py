#!/usr/bin/env python
#@ author: Celi Sun 
#@ date: Aug, 2017
#@ brief: rosmaze solving on stdr 

import roslib; roslib.load_manifest('stdr_samples')
import rospy
import sys
import time
import numpy as np
from geometry_msgs.msg import Twist, Pose2D, Point
from sensor_msgs.msg import LaserScan, Range
from stdr_msgs.msg import RobotIndexedVectorMsg
from sensor import Lasers
from sensor2state import *
from pid import PID
from lidar import lidar360



if (len(sys.argv) != 2):       
   raise ValueError('Usage: stdr_gomaze <robot_frame_id>')
robotid = str(sys.argv[1])  

rospy.init_node('stdr_maze')

stdr_range = 10
lidar360 = lidar360(robotid) # turtlebot lidar
cmd_vel_pub = rospy.Publisher("/%s/cmd_vel"%(robotid), Twist, queue_size=1) # speed publisher
    
pid = PID(stdr_range, cmd_vel_pub)    
twist = Twist() 
rate = rospy.Rate(10)


def out():
   m = lidar360.dahead >= lidar360.range_max
   n = lidar360.dleft >= lidar360.range_max
   q = lidar360.dright >= lidar360.range_max
   return (m and n and q)



# run 
while not rospy.is_shutdown():

     d3 = [lidar360.dahead,lidar360.dleft,lidar360.dright]
     i = d3.index(max(d3)) 

     if out(): 
        print "maze finished"
	print "%s, %s, %s"%(lidar360.dahead, lidar360.dleft, lidar360.dright)
        twist.linear.x = 0.
        twist.angular.z = 0.

     elif (lidar360.dahead < 1.5):   # never hit wall. bounce back when necessary
        twist.linear.x = -1.5

     elif (i == 1):    		  #open left, turn left
           print "turn L: %s, %s, %s"%(lidar360.dahead, lidar360.dleft, lidar360.dright)
           twist.linear.x= 0.45
           twist.angular.z = 0.4
           pid.reset()

     elif (i == 0):      # otherwise, go forward 
           print "FORWARD: %s, %s, %s"%(lidar360.dahead, lidar360.dleft, lidar360.dright) 
           pid.go(lidar360.dahead, lidar360.dleft,lidar360.dright)  ## was dright = fixed 1.5
           #twist.angular.z =0.
           #twist.linear.x = 1.5

     elif (i == 2):   	  # otherwise, turn right if open
           print "turn R: %s, %s, %s"%(lidar360.dahead, lidar360.dleft, lidar360.dright)
           twist.linear.x= 0.45
           twist.angular.z = -0.4
           pid.reset()

     #start_t = time.time()
     time.sleep(0.3)
     cmd_vel_pub.publish(twist)
     rate.sleep()


      
