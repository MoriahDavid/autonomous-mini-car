import time
from car import Car

OBJECTS_TO_STOP = ['stop sign', 'cup', 'teddy bear', 'dog']


class CarController:
    def __init__(self, car: Car):
        self.car = car
        self._stop = False

        self._is_reversing = False
        self.reversing_time = None

    def reversing(self):
        self._is_reversing = True
        self.reversing_time = time.time()
        self.car.move_backward(0)

    def stop(self):
        self.car.stop()
        self._stop = True

    def resume(self):
        self._stop = False

    def control(self, objects, sensors, lane_steering_angle):
        if self._stop:
            return

        if self._is_reversing:
            print("is_reversing")

            if time.time() - self.reversing_time > 3:
                self.car.stop()
                self._is_reversing = False
            return

        if any(obj in OBJECTS_TO_STOP for obj in objects):
            self.car.stop()
            return

        gyro = sensors['android.sensor.gyroscope']['values']

        if abs(gyro[1]) > 0.7 and not self._is_reversing:
            print("is_reversing")
            self.car.stop()
            self.reversing()

            return

        angle = lane_steering_angle - 90
        self.car.move_forward(angle)
        print(angle)
