from dotenv import load_dotenv
from os import getenv
import cv2
from PIL import Image
from core.shared import CornerDetector, PerspectiveTransformer, PiecesDetector, GridCalculator, ChessPieceMapper, FENConverter



def main():
    image_path = "/"
    transformed_image_path = "/"
    original_image = cv2.imread(image_path)
    corners = CornerDetector.detect_corners(original_image)
    transformed_image = PerspectiveTransformer.four_point_transform(image_path, corners)
    transformed_image.save(transformed_image_path)
    transformed_image = Image.open(transformed_image_path)
    ptsT, ptsL = GridCalculator.plot_grid_on_transformed_image(transformed_image)
    detections, boxes = ChessPieceMapper.chess_pieces_detector(transformed_image)
    fen = FENConverter.generate_fen(ptsT, ptsL, detections, boxes)
    print("https://lichess.org/analysis/", fen, sep="")

if __name__ == "__main__":
    main()
