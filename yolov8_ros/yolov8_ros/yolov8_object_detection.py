import cv2 
import torch
import random
import numpy as np

import rclpy
from rclpy.qos import qos_profile_sensor_data
from rclpy.node import Node 
from cv_bridge import CvBridge

from ultralytics import YOLO

from sensor_msgs.msg import Image
from vision_msgs.msg import Detection2D
from vision_msgs.msg import BoundingBox2DArray, BoundingBox2D
from happymimi2_recognition_msgs.msg import ObjectDetect, ObjectDetectArray
from geometry_msgs.msg import Pose2D

class yolov8_object_detection(Node):

    def __init__(self):
        super().__init__('yolov8_object_detection')
        self.cv_bridge = CvBridge()
        self.yolo = YOLO("yolov8n.pt")
        self.track = self.yolo.track(source = 0, show=True, tracker="bytetrack.yaml")
        self.yolo.fuse()

        self.send_objectdetect = self.create_subscription(
            Image,
            'camera/color/image_raw',
            self.CallBack,
            qos_profile_sensor_data
        )
        self.send_track = self.create_subscription(
            Image,
            '/ca mera/color/image_raw',
            self.CallbackTrack,
            qos_profile_sensor_data
        )

        self.send_objectdetect
        self.send_track
    

    
    def proess_image(self, data):
        
        orig = self.cv_bridge.imgmsg_to_cv2(data, "bgr8")
        return orig

    
    def CallBack(self, msg):


        image_data = self.proess_image(msg)
        results = self.yolo(image_data, show=True, conf=0.3)

        frame = results[0].plot()
        boxes = results[0].boxes
        names = results[0].names

        


    def CallbackTrack(self, msg):

        results = self.track




def main(args=None):

    rclpy.init(args=args)

    yolov8_object_detection = yolov8_object_detection()
    
    rclpy.spin(yolov8_object_detection)




if __name__ == '__main__':
    main()

