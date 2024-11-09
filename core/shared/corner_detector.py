from ultralytics import YOLO
from os import path
from .perspective_transformer import PerspectiveTransformer

model = YOLO(path.join(path.dirname(path.dirname(path.dirname(__file__))), "assets/models/corner-detector.pt"))

class CornerDetector:
    def __init__(self):
        pass

    @staticmethod
    def detect_corners(image):
        results = model.predict(source=image, line_width=1, conf=0.25, save=True)
        boxes = results[0].boxes
        if len(boxes) < 4: # type: ignore
            return None

        arr = boxes.xywh.numpy() # type: ignore
        points = arr[:, 0:2]

        if len(points) < 4:
            return None

        return PerspectiveTransformer.order_points(points)
