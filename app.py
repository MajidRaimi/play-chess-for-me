
from dotenv import load_dotenv
import cv2
from core.shared import CornerDetector, PerspectiveTransformer, GridCalculator, ChessPieceMapper, FENConverter, ImageGenerator, BestMove
from Levenshtein import ratio

def get_best_move(image_path: str):
    original_image = cv2.imread(image_path)
    corners = CornerDetector.detect_corners(original_image)
    transformed_image = PerspectiveTransformer.four_point_transform(image_path, corners)
    ptsT, ptsL = GridCalculator.plot_grid_on_transformed_image(transformed_image)
    detections, boxes = ChessPieceMapper.chess_pieces_detector(transformed_image)
    predicted_fen = FENConverter.generate_fen(ptsT, ptsL, detections, boxes)
    formatted_fen = BestMove.format_fen(predicted_fen)
    best_move = BestMove.get_best_move(formatted_fen)
    ImageGenerator.generate_image(formatted_fen, best_move)



