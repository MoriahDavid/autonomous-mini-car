import cv2
import numpy as np
from objectDetection import ObjectDetection
from src.laneDetection import LaneDetection
import time


class Camera:
    def __init__(self, ip, port=8080, fps=1):
        self.ip = ip
        self.url = f'http://{ip}:{port}/video'
        self.cap = cv2.VideoCapture(self.url)
        self.cap.set(cv2.CAP_PROP_FPS, fps)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        if not self.cap.isOpened():
            raise ValueError(f"Unable to connect to camera at {self.url}")

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            raise ValueError("Unable to read frame from camera")
        return frame

    def release(self):
        self.cap.release()
