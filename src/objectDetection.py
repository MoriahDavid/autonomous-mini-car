import cv2
from ultralytics import YOLO


class ObjectDetection:
    threshold = 0.4

    def __init__(self, gpu_device='mps'):

        # Load YOLO model
        self.yolo = YOLO('yolov8s.pt')
        self.gpu_device = gpu_device

    def detect(self, frame):
        results = self.yolo(frame, stream=True, device=self.gpu_device)

        return results

    def draw_objects(self, frame, results):

        for result in results:
            # get the classes names
            classes_names = result.names

            # iterate over each box
            for box in result.boxes:
                # check if confidence is greater than 40 percent
                if box.conf[0] > self.threshold:
                    # get coordinates
                    [x1, y1, x2, y2] = box.xyxy[0]
                    # convert to int
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                    # get the class
                    cls = int(box.cls[0])

                    # get the class name
                    class_name = classes_names[cls]

                    # get the respective colour
                    colour = self.get_colors(cls)

                    # draw the rectangle
                    cv2.rectangle(frame, (x1, y1), (x2, y2), colour, 2)

                    # put the class name and confidence on the image
                    cv2.putText(frame, f'{classes_names[int(box.cls[0])]} {box.conf[0]:.2f}', (x1, y1),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, colour, 2)
        return frame

    def get_object_names(self, results):
        names = []
        for result in results:
            # get the classes names
            classes_names = result.names

            # iterate over each box
            for box in result.boxes:
                # check if confidence is greater than 40 percent
                if box.conf[0] > self.threshold:
                    names.append(classes_names[int(box.cls[0])])

        return names

    def get_colors(self, cls_num):
        base_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        color_index = cls_num % len(base_colors)
        increments = [(1, -2, 1), (-2, 1, -1), (1, -1, 2)]
        color = [base_colors[color_index][i] + increments[color_index][i] *
                 (cls_num // len(base_colors)) % 256 for i in range(3)]
        return tuple(color)


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    objectDetection = ObjectDetection()

    while True:
        check, frame = cap.read()
        results = objectDetection.detect(frame)
        frame = objectDetection.draw_objects(frame, results)
        cv2.imshow('Object Detection', frame)

        cv2.waitKey(200)

