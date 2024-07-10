import time

import numpy as np
import cv2

from camera import Camera
from sensors import Sensors
from objectDetection import ObjectDetection
from car import Car
from carController import CarController
from laneDetection import LaneDetection

import pygame

DEVICE_IP = '192.168.223.193'  # HOTSPOT

FPS = 20
green = (0, 255, 0)
blue = (0, 0, 128)


class SelfDrivingCar:
    def __init__(self):
        self.camera = Camera(DEVICE_IP, fps=FPS)
        self.sensors = Sensors(DEVICE_IP)
        self.object_detection = ObjectDetection()
        self.lane_detection = LaneDetection()
        self.car = Car()
        self.car_controller = CarController(self.car)
        time.sleep(4)  # Waiting for the connections to established

        self.frame_rate = FPS
        self.prev_frame = 0

        self.object_detection_rate = 2
        self.prev_object_detection = 0
        self.objects = []

    def processing(self, win):
        frame = self.camera.get_frame()
        display_frame = frame.__copy__()
        if time.time() - self.prev_frame > 1. / self.frame_rate:
            self.prev_frame = time.time()

            if time.time() - self.prev_object_detection > 1. / self.object_detection_rate:
                self.prev_object_detection = time.time()
                self.objects = list(self.object_detection.detect(frame))

            display_frame = self.object_detection.draw_objects(display_frame, self.objects)

            lane_lines, steering_angle = self.lane_detection.detect(frame)

            display_frame = self.lane_detection.draw_lane(display_frame, lane_lines, steering_angle)

            objects_names = self.object_detection.get_object_names(self.objects)
            self.car_controller.control(objects_names, self.sensors.get_sensors(), steering_angle)

            # frame = cv2.resize(frame, (640, 480))
            display_frame = cv2.flip(display_frame, 1)

            display_frame = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
            display_frame = np.rot90(display_frame)

            display_frame = pygame.surfarray.make_surface(display_frame)
            win.blit(display_frame, (0, 0))

    def display_sensors(self, win):
        font = pygame.font.Font('freesansbold.ttf', 15)
        # sensors_data = ""
        position_y = win.get_height()
        for key, data in self.sensors.get_sensors().items():
            values = [f'{v:3.2f}' for v in data['values']]
            sensors_data = f"{key: <30}: {values}"

            text = font.render(sensors_data, True, green, blue)
            textRect = text.get_rect()
            textRect.bottomleft = (0, position_y)
            win.blit(text, textRect)
            position_y -= textRect.height

    def main_loop(self):
        pygame.init()
        win = pygame.display.set_mode([640, 480])
        pygame.display.set_caption("View")
        clock = pygame.time.Clock()

        self.car_controller.stop()
        self.car.send_set_speed(160)
        run = True
        while run:
            # clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            self.processing(win)
            self.display_sensors(win)

            pygame.display.update()

            key = cv2.waitKey(1)
            # Pause using 'p' -> continue with any key
            if key == ord('p'):
                cv2.waitKey(-1)

            if key == ord('s'):
                self.car_controller.stop()
            if key == ord('r'):
                self.car_controller.resume()

            # Exit on 'q' key
            elif key == ord('q'):
                break

        pygame.quit()


if __name__ == '__main__':
    SelfDrivingCar().main_loop()
