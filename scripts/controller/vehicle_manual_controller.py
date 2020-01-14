# -*- coding: utf-8 -*-
import rospy
from autoware_msgs.msg import VehicleCmd

class VehicleManualController(object):
    def __init__(self):
        # Setup timer
        self.timer = rospy.Timer(rospy.Duration(0.1), self.timer_callback)
        # Velocity to send
        self.velocity_linear = 0.0
        self.steer_angle = 0.0
        # Publisher
        self.velocity_cmd_pub = rospy.Publisher('/vehicle_cmd', VehicleCmd, queue_size=1)

    def set_velocity_kmph(self, linear_kmph, steer_angle_deg):
        # type: (float, float) -> None
        self.velocity_linear = linear_kmph * 1000.0 / 3600.0
        self.steer_angle = steer_angle_deg

    def timer_callback(self, event):
        msg = VehicleCmd()
        msg.ctrl_cmd.linear_velocity = self.velocity_linear
        msg.twist_cmd.twist.linear.x = self.velocity_linear
        self.velocity_cmd_pub.publish(msg)

    def stop_now(self):
        # If not call this, last command may be overwritten by callback.
        self.timer.shutdown()
        # Send command to stop
        msg = VehicleCmd()
        msg.ctrl_cmd.linear_velocity = 0.0
        msg.twist_cmd.twist.linear.x = 0.0
        self.velocity_cmd_pub.publish(msg)