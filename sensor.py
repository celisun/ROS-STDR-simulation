## simple wrapper for laser 1,2,3 (forward, left & right) of an stdr robot
##

import rospy
import numpy as np
import re
import time
import sys
from sensor_msgs.msg import LaserScan

class Lasers(object):

    def __init__(self, robotid, num_lasers=3, callback=None):
        self.robotid = robotid
        self.num_lasers = num_lasers
        self.r_ahead = 10
        self.r_left = 0.1
        self.r_right = 0.1
        self.max = 1000.
        self.min = 0.
        self.a = 0.
        self.l = 0.
        self.r = 0.
        self.angle_increment =0.
        self.angle_min = 0.
        self.angle_max = 0.
        self.reset()
        if not callback: 
           self.callback = self._callback
        else: 
           self.callback = callback
        for idx in range(0, num_lasers):
            # laser 1, 2, 3  =>  forward, left & right
            rospy.Subscriber("/%s/laser_%s" % (self.robotid, idx+1), LaserScan, self.callback)

    def reset(self):
        # dft noop value for case of lasers not publishing yet
        self.ranges = [0] * self.num_lasers



    def _callback(self, msg):
       ids = ["%s_laser_%s" %(self.robotid, i+1) for i in range(self.num_lasers)]
       i = ids.index(msg.header.frame_id)
      
       r = min(msg.ranges)
       length = len(msg.ranges)
       self.max = msg.range_max
       self.min = msg.range_min
       if r > self.max: r = self.max
       if r < self.min: r = 0

       if i == 0: 
          self.r_ahead = r
          self.a = length
          self.angle_increment = msg.angle_increment
          self.angle_min =msg.angle_min 
          self.angle_max = msg.angle_max

       elif i ==1: 
          self.r_left = r
          self.l = length
       elif i ==2: 
          self.r_right = r
          self.r = length
   

    def laser_callback2(self, msg):
        # record callback from one laser into ranges []
        m = re.match(".*laser_(.*)", msg.header.frame_id)
        idx = int(m.group(1))  			# or die in a regex non match hellfire
        r = msg.range
        self.max = msg.max_range
        self.min = msg.min_range
        if r > self.max: r = self.max
        if r < self.min: r = 0
        self.ranges[idx] = int(r * 100) # for ease of reading







