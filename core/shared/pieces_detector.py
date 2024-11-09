from ultralytics import YOLO
from os import path

model = YOLO(path.join(path.dirname(path.dirname(path.dirname(__file__))), "assets/models/pieces-detector.pt"))

class PiecesDetector:
    def __init__(self):
        pass

    @staticmethod
    def detect_pieces(image):
        results = model.predict(source=image, line_width=1, conf=0.2, save=True)
        return results