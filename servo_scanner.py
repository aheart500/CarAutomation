import rclpy
from rclpy.node import Node

from sensor_msgs.msg import LaserScan

from servo_lidar import *
import math


SERVO_GPIO = 18
SRV_ANGLE_MIN=math.radians(-90)
SRV_ANGLE_MAX=math.radians(90)
SRV_DUTY_MIN=2
SRV_DUTY_MAX=12.5
SRV_TIME_MIN_MAX=0.4






class ServoScannerPublisher(Node):

    def __init__(self):
        super().__init__('servo_publisher_publisher')
        self.publisher_ = self.create_publisher(LaserScan, 'servo_scanner', 10)

        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        scan = LaserScan()

        tfminiScanner = TfminiServoScanner(SERVO_GPIO, SRV_ANGLE_MIN, SRV_ANGLE_MAX, SRV_DUTY_MIN, SRV_DUTY_MAX,10,'/dev/ttyS0',0.4)

        scan.header.frame_id = 'map'
        scan.range_min = tfminiScanner.laser.distance_min *0.01
        scan.range_max = tfminiScanner.laser.distance_max *0.01

        tfminiScanner.reset_servo()
        time.sleep(1)


        ini_angle,end_angle,time_increment,angle_increment, ranges = tfminiScanner.scan(scale_factor=0.01, reset=True)

        scan.angle_min = ini_angle
        scan.angle_max = end_angle
        scan.angle_increment = angle_increment
        scan.time_increment = time_increment
        scan.ranges = ranges

        self.publisher_.publish(scan)
        self.get_logger().info('Publishing '  )

def main(args=None):
    rclpy.init(args=args)

    servoScanner_publisher = ServoScannerPublisher()

    rclpy.spin(servoScanner_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    servoScanner_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
