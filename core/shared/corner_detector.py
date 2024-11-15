from ultralytics import YOLO
from os import path, getenv
from .perspective_transformer import PerspectiveTransformer
from dotenv import load_dotenv

load_dotenv()

model = YOLO(path.join(path.dirname(path.dirname(path.dirname(__file__))), "assets/models/corner-detector.pt"))

class CornerDetector:
    def __init__(self):
        pass


    @staticmethod
    def detect_corners(image):
        results = model.predict(
            source=image,
            line_width=1,
            conf=0.3,
            save=False,
            verbose=False
        )
        
        if getenv("DEBUG"):
            plotted_image = results[0].plot()
            from PIL import Image
            import numpy as np
            
            Image.fromarray(image[..., ::-1] if image.shape[-1] == 3 else image).save("pipe/00_image.png")
            Image.fromarray(plotted_image[..., ::-1]).save("pipe/01_corners.png")
        
        boxes = results[0].boxes
        if len(boxes) < 4: # type: ignore
            return None

        arr = boxes.xywh.numpy() # type: ignore
        points = arr[:, 0:2]

        if len(points) < 4:
            return None

        return PerspectiveTransformer.order_points(points)
