from ultralytics import YOLO
from os import path
import numpy as np
from . import PerspectiveTransformer

model = YOLO(path.join(path.dirname(path.dirname(path.dirname(__file__))), "assets/models/pieces-detector.pt"))

class PiecesDetector:
    def __init__(self):
        pass

    @staticmethod
    def detect_pieces(image):
        results = model.predict(source=image, line_width=1, conf=0.4, save=False, verbose=False)
        
        # Filter overlapping detections
        boxes = results[0].boxes
        if len(boxes) > 0:
            detections = boxes.xyxy.numpy()  # type: ignore
            confidences = boxes.conf.numpy()  # type: ignore
            classes = boxes.cls.numpy()  # type: ignore
            
            # Sort all detections by confidence (highest first)
            sorted_indices = np.argsort(-confidences)  # negative for descending order
            indices_to_keep = []
            
            while len(sorted_indices) > 0:
                # Keep the current highest confidence detection
                current_idx = sorted_indices[0]
                indices_to_keep.append(current_idx)
                
                # Remove the current index from sorted_indices
                sorted_indices = sorted_indices[1:]
                
                if len(sorted_indices) == 0:
                    break
                
                # Compare current box with all remaining boxes
                current_box = detections[current_idx]
                current_box_points = np.array([
                    [current_box[0], current_box[1]],  # top-left
                    [current_box[2], current_box[1]],  # top-right
                    [current_box[2], current_box[3]],  # bottom-right
                    [current_box[0], current_box[3]]   # bottom-left
                ])
                
                indices_to_remove = []
                for i, idx in enumerate(sorted_indices):
                    compare_box = detections[idx]
                    compare_box_points = np.array([
                        [compare_box[0], compare_box[1]],
                        [compare_box[2], compare_box[1]],
                        [compare_box[2], compare_box[3]],
                        [compare_box[0], compare_box[3]]
                    ])
                    
                    iou = PerspectiveTransformer.calculate_iou(current_box_points, compare_box_points)
                    
                    # If boxes overlap significantly, mark for removal
                    if iou > 0.3:
                        indices_to_remove.append(i)
                
                # Remove overlapping boxes
                sorted_indices = np.delete(sorted_indices, indices_to_remove)
            
            # Update results with filtered detections
            results[0].boxes.data = results[0].boxes.data[indices_to_keep]
        
        return results