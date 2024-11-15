from dotenv import load_dotenv
import cv2
from core.shared import CornerDetector, PerspectiveTransformer, GridCalculator, ChessPieceMapper, FENConverter, ImageGenerator, BestMove
from Levenshtein import ratio



def main():
    image_path = f"./tests/rqb1k2r-1p1p1pPp-4p3-1pb5-5P2-2N3P1-PPP1B2P-R2QK2R.JPG"
    original_image = cv2.imread(image_path)
    corners = CornerDetector.detect_corners(original_image)
    transformed_image = PerspectiveTransformer.four_point_transform(image_path, corners)
    ptsT, ptsL = GridCalculator.plot_grid_on_transformed_image(transformed_image)
    detections, boxes = ChessPieceMapper.chess_pieces_detector(transformed_image)
    GridCalculator.grid_drawer(ptsT, ptsL, detections, boxes)
    predicted_fen = FENConverter.generate_fen(ptsT, ptsL, detections, boxes)
    formatted_fen = BestMove.format_fen(predicted_fen)
    best_move = BestMove.get_best_move(formatted_fen)

    if best_move:
        ImageGenerator.generate_image(formatted_fen, best_move)
    else:
        ImageGenerator.generate_image(formatted_fen)

    real_fen = "/".join(image_path.split("/")[-1].split(".")[0].split("-"))

    similarity = ratio(real_fen, predicted_fen) * 100

    print("Real FEN:      ", real_fen)
    print("Predicted FEN: ", predicted_fen)
    print(f"Similarity:     {similarity:.2f}%")

if __name__ == "__main__":
    load_dotenv()
    main()