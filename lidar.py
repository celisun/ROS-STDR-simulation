## simple wrapper for 360 deg. Lidar sensor on turtlebot. 360deg span with 360 # rays.  
##

import rospy
from sensor_msgs.msg import LaserScan


class lidar360(object):
	
	def __init__ (self, robotid, sensorid=None, callback_=None):
		self.robotid = robotid
		if not sensorid:
			sensorid = 1
		if callback_:
			self.callback = callback_
		else:
			self.callback = self.callback
		rospy.Subscriber("/%s/laser_%s" % (self.robotid, sensorid), LaserScan, self.callback)

		## all parameters in /sensor_msgs LaserScan message type
		self.range_min= 0.     ## min range 
		self.range_max= 0.	##lidar max range 
		self.min= 0.
		self.max = 0. 
		self.dahead =0.		## distance 0 dir
		self.dleft =0.		## distance pi/2 dir	
		self.dright =0.		## distance -pi/2 (pi 3/4) dir
		self.ranges = []    ## an array of 360 float32 elements. reporting distance on each rays
		self.angle_min = 0.
		self.angle_max = 0.
		self.angle_increment = 0.
		self.time_increment = 0.
		self.scan_time =0.
		self.intensities = []

		

	def reset(self): 

		self.ranges = [0] * self.num_lasers


	def callback(self, msg): 
		self.ranges = msg.ranges
		self.range_max = msg.range_max
       		self.range_min = msg.range_min
		self.min = min(msg.ranges)
		self.max = max(msg.ranges)		
		self.angle_increment = msg.angle_increment
		self.scan_time = msg.scan_time
		self.time_increment = msg.time_increment
		self.angle_min = msg.angle_min
		self.angle_max = msg.angle_max
		self.intensities = msg.intensities

		right30 = self.ranges[3*len(self.ranges)/4-15:3*len(self.ranges)/4+15]
                left30 = self.ranges[len(self.ranges)/4-15:len(self.ranges)/4+15]
                ahead20 = self.ranges[0:10]+ self.ranges[350:360]
                
		self.dahead = min(ahead20)
		self.dright = min(right30)
		self.dleft = min(left30)
		








