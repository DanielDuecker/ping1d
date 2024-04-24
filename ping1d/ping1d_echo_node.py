# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node

#from std_msgs.msg import String
from sensor_msgs.msg import Range
from brping import Ping1D


class Ping1DNode(Node):

    def __init__(self):
        super().__init__('ping1d_echo')
        self.publisher_ = self.create_publisher(Range, 'ping1d_topic', 10)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.publish_range)
        self.i = 0

        device = '/dev/ttyAMA2'
        baudrate = 115200
        speed_of_sound_mms = 1.5e6 # ~1,500,000 mm/s for water 350,000mm/s for air
        # Make a new Ping
        self.myPing = Ping1D()
        if device is not None:
            self.myPing.connect_serial(device, baudrate)
        # elif args.udp is not None:
        #     (host, port) = args.udp.split(':')
        #     myPing.connect_udp(host, int(port))

        if self.myPing.initialize() is False:
            print("Failed to initialize Ping!")
            exit(1)
        print("------------------------------------")
        print("Starting Ping..")
        # print("Press CTRL+C to exit")
        
        # Set the speed of sound used for distance calculations
        # self.myPing.set_speed_of_sound(self, speed_of_sound=speed_of_sound_mms) # ~1,500,000 mm/s for water 350,000mm/s for air
        data_sof = self.myPing.get_speed_of_sound()
        print("Using Speed of Sound = %f m/s" % (float(data_sof["speed_of_sound"])/1000))
        print("------------------------------------")


    #def timer_callback(self):
        # msg = String()
        # msg.data = 'Hello World: %d' % self.i
        # self.publisher_.publish(msg)
        # self.get_logger().info('Publishing: "%s"' % msg.data)
        # self.get_logger().info('Publishing: "%d"' % self.i)
        # self.i += 1

    def publish_range(self):
        range_msg = Range()
        data = self.myPing.get_distance()
        if data:
            range_msg.header.stamp = self.get_clock().now().to_msg()
            range_msg.range = float(data["distance"])/1000
            #print("Distance: %s\tConfidence: %s%%" % (data["distance"], data["confidence"]))
            self.get_logger().info('Publishing:  Dist. "%f" || confidence "%s%%"' % (range_msg.range, data["confidence"]))
            self.publisher_.publish(range_msg)
        else:
            print("Failed to get distance data")
        #time.sleep(0.1)


def main(args=None):
    rclpy.init(args=args)
    ping_1d = Ping1DNode()
    rclpy.spin(ping_1d)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    ping_1d.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
