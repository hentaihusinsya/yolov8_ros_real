import cv2 
import torch

import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge

from ultralytics import YOLO

class YoloRos(Node):

    def __init__(self):

        super().__init__('yolov8_ros')
        

        self.bridge = CvBridge()
        self.yolo = YOLO('yolov8-seg.pt')
        self.yolo.fuse()
        


    def CallDetector(self, msg):
        orig = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        results = self.yolo(orig, show=True, conf=0.4)