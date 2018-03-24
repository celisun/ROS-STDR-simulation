# @author: Nishan Acharya, Aaron Marks, Jonathan Turner
# @Autonomous Robotics Lab at Brandeis University
#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler

rospy.init_node('follow_wall')
rate = rospy.Rate(5)
vel_msg = Twist()
vel_msg.linear.x = .08
vel_msg.linear.y = 0
vel_msg.linear.z = 0
vel_msg.angular.x = 0
vel_msg.angular.y = 0
vel_msg.angular.z = 0
turnLeft = False
turnRight = False
current_yaw = 0
calibrate=True
start = True

#Laser Sensor callback -If open on left, turn left, if blocked in front turn right
def callback1(msg):
 global turnLeft, turnRight, calibrate, vel_msg, start
 if start:
    if msg.ranges[179] < .1:
       start = False

 elif calibrate:
    #print "left: ", msg.ranges[269] 
    #print "forward: ", msg.ranges[265]
    #print "back: ", msg.ranges[273]
    if abs(msg.ranges[299]- msg.ranges[239]) > .001 :
       vel_msg.angular.z =-.03
       vel_msg.linear.x =0
       print "calibrating"
   #    pub.publish(vel_msg)
   # elif msg.ranges[269]> msg.ranges[299]:
    #   vel_msg.angular.z =.05
     #  print "turning left"
      # pub.publish(vel_msg)     
    else:
       print "finished calibrating"
       calibrate=False  

 elif msg.ranges[269]>.25 and msg.ranges[234]>.3 and not turnRight and not turnLeft:# and abs(msg.ranges[314]-2.83)<.05:
    turnLeft = True
    print "turn left"
 elif msg.ranges[179] < .15 and not turnLeft and not turnRight:   # or msg.ranges[89] > 4:
    turnRight=True
    print "turn right"
 #elif not turnLeft and not turnRight and msg.ranges[299]- msg.ranges[239] > .001:
  #  tryCalibrate()


#Odom Callback - If turned 90 Degrees, stop turning
def callback2(msg):
 global current_yaw
 global turnLeft
 global turnRight
 global vel_msg
 global calibrate
 orientation_q = msg.pose.pose.orientation
 orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
 (roll, pitch, yaw) = euler_from_quaternion (orientation_list)  
 if calibrate:
   current_yaw= yaw
 elif abs(abs(abs(current_yaw)-abs(yaw))-1.57079632679)<.05:
   print '90 degrees'
   current_yaw= yaw
   vel_msg.angular.z = 0
   pub.publish(vel_msg)
   turnLeft = False
   turnRight=False

def tryCalibrate():
 global calibrate, vel_msg
 vel_msg.linear.x = 0
 vel_msg.angular.z = 0
 pub.publish(vel_msg)
 calibrate=True

pub = rospy.Publisher('robot0/cmd_vel', Twist, queue_size=10)
sub_laser = rospy.Subscriber('robot0/laser_0', LaserScan, callback1, queue_size=10)
sub_odom = rospy.Subscriber('robot0/odom', Odometry, callback2, queue_size=10)

while start:
  pub.publish(vel_msg)
  rate.sleep()  
tryCalibrate()

#Always publish the vel_msg whatever it is
while not rospy.is_shutdown():
 if not calibrate:
   if turnLeft:
    vel_msg.linear.x = .015
    vel_msg.angular.z =.1
   elif turnRight:
    vel_msg.linear.x = 0
    vel_msg.angular.z =-.07
   else:
    vel_msg.linear.x = .08
    vel_msg.angular.z = 0
 pub.publish(vel_msg)
 rate.sleep()





