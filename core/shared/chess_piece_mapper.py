from shapely.geometry import Polygon
import numpy as np
from . import PiecesDetector, PerspectiveTransformer

class ChessPieceMapper:
    @staticmethod
    def chess_pieces_detector(image):
        results = PiecesDetector.detect_pieces(image)
        boxes = results[0].boxes
        detections = boxes.xyxy.numpy() # type: ignore

        return detections, boxes

    @staticmethod
    def connect_square_to_detection(detections, square, boxes, iou_threshold=0.1, padding=30):
        di = {0: 'b', 1: 'k', 2: 'n', 3: 'p', 4: 'q', 5: 'r', 6: 'B', 7: 'K', 8: 'N', 9: 'P', 10: 'Q', 11: 'R'}
        list_of_iou = []

        for i, detection in enumerate(detections):
            # Adjust detection for padding
            box_x1, box_y1 = detection[0] - padding, detection[1] - padding
            box_x2, box_y2 = detection[2] - padding, detection[1] - padding
            box_x3, box_y3 = detection[2] - padding, detection[3] - padding
            box_x4, box_y4 = detection[0] - padding, detection[3] - padding
            
            if box_y4 - box_y1 > 60:
                box_complete = np.array([[box_x1, box_y1 + 40], [box_x2, box_y2 + 40], [box_x3, box_y3], [box_x4, box_y4]])
            else:
                box_complete = np.array([[box_x1, box_y1], [box_x2, box_y2], [box_x3, box_y3], [box_x4, box_y4]])

            if ChessPieceMapper.is_valid_polygon(box_complete) and ChessPieceMapper.is_valid_polygon(square):
                try:
                    iou = PerspectiveTransformer.calculate_iou(box_complete, square)
                    list_of_iou.append(iou)
                except Exception as e:
                    list_of_iou.append(0)
            else:
                list_of_iou.append(0)

        max_iou = max(list_of_iou)
        num = list_of_iou.index(max_iou)
        piece = boxes.cls[num].tolist()


        return di[piece] if max_iou > iou_threshold else "empty"

    @staticmethod
    def is_valid_polygon(points):
        return len(points) >= 3 and Polygon(points).is_valid
