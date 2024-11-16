import cv2
import numpy as np
from PIL import Image
from shapely.geometry import Polygon
import os

class PerspectiveTransformer:
    @staticmethod
    def order_points(pts):
        rect = np.zeros((4, 2), dtype="float32")
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        return rect

    @staticmethod
    def four_point_transform(image_path, pts):
        padding = 30
        img = Image.open(image_path)
        image = np.asarray(img)
        rect = PerspectiveTransformer.order_points(pts)
        (tl, tr, br, bl) = rect

        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB)) + padding * 2

        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB)) + padding * 2

        dst = np.array([
            [padding, padding],
            [maxWidth - 1 - padding, padding],
            [maxWidth - 1 - padding, maxHeight - 1 - padding],
            [padding, maxHeight - 1 - padding]], dtype="float32")

        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
        
        if os.getenv('DEBUG', 'false').lower() == 'true' or True:
            output_path = os.path.join(f'pipe/02_transformed.png')
            cv2.imwrite(output_path, cv2.cvtColor(warped, cv2.COLOR_RGB2BGR))
        return Image.fromarray(warped, "RGB")

    @staticmethod
    def calculate_iou(box_1, box_2):
        poly_1 = Polygon(box_1)
        poly_2 = Polygon(box_2)
        return poly_1.intersection(poly_2).area / poly_1.union(poly_2).area
