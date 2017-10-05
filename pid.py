# brief: PID algorithm, keep robot in the middle of path by comparing 
#    distance of left and right side.  

from geometry_msgs.msg import Twist

class PID:
   def __init__(self, range_, cmd_vel_pub, Kp=0.3, Kd=0.02, Ki=0.01, uplimit=0.3, lolimit=-0.3):

       self.range = range_
       self.cmd_vel_pub = cmd_vel_pub
       self.twist = Twist()
       self.Kp = Kp  # proportional gain constant 
       self.Kd = Kd  # derivative gain constant 
       self.Ki = Ki  # integral gain constant
       self.uplimit = uplimit
       self.lolimit = lolimit
       self.preverror = 0.
       self.lerror = 0.

   def reset(self):
       self.preverror = 0.
       self.lerror = 0.
       self.twist.angular.z = 0.

   def go(self, r_ahead, r_left, r_right):
      
      error = 0.  # error
      derror= 0.  # error detivative 

      if (r_ahead < 1):
         self.twist.linear.x = -1.

      error = r_left - r_right
      if (error > self.range or error < - self.range):
         return 0.

      derror = error - self.preverror
      c = (self.Kp*error) + (self.Kd*derror) + (self.Ki*self.lerror)   

      if (self.twist.angular.z +c) > self.uplimit:
         self.twist.angular.z = self.uplimit
      elif (self.twist.angular.z+c) < self.lolimit:
         self.twist.angular.z = self.lolimit
      else: 
         self.twist.angular.z = c

      self.preverror = error
      self.lerror += error
       
      self.twist.linear.x =1.85
      self.cmd_vel_pub.publish(self.twist)






