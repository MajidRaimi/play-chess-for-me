from dotenv import load_dotenv
from core.constants import error_messages
import cv2
from core.shared import (
    CornerDetector,
    PerspectiveTransformer,
    GridCalculator,
    ChessPieceMapper,
    FENConverter,
    ImageGenerator,
    BestMove,
)
import os
from core.functions import clear_console

def pipeline(image_path):
    load_dotenv()
    clear_console()
    step = 0
    if not os.path.exists("pipe"):
        os.makedirs("pipe")

    try:

        step = 0
        original_image = cv2.imread(image_path)
        if original_image is None:
            raise FileNotFoundError(f"Image not found at path: {image_path}")
        print("1/10 Image Successfully Read ✅")
        

        step = 1
        corners = CornerDetector.detect_corners(original_image)
        print("2/10 Corners Detected ✅")
        

        step = 2
        transformed_image = PerspectiveTransformer.four_point_transform(image_path, corners)
        print("3/10 Perspective Transformation Completed ✅")
        

        step = 3
        ptsT, ptsL = GridCalculator.plot_grid_on_transformed_image(transformed_image)
        print("4/10 Grid Points Calculated ✅")
        

        step = 4
        detections, boxes = ChessPieceMapper.chess_pieces_detector(transformed_image)
        print("5/10 Chess Piece Detections ✅")
        

        step = 5
        GridCalculator.grid_drawer(ptsT, ptsL, detections, boxes)
        print("6/10 Grid and Pieces Mapped Successfully ✅")
        

        step = 6
        predicted_fen = FENConverter.generate_fen(ptsT, ptsL, detections, boxes)
        print("7/10 Generated FEN ✅")
        

        step = 7
        formatted_fen = BestMove.format_fen(predicted_fen)
        print("8/10 FEN Formatted ✅")

        step = 8
        best_move = BestMove.get_best_move(formatted_fen)
        if best_move:
            print("9/10 Best Move Found ✅")
        else:
            print("9/10 No Best Move Found ❌")

        step = 9
        if best_move:
            ImageGenerator.generate_image(formatted_fen, best_move)
        else:
            ImageGenerator.generate_image(formatted_fen)
        clear_console()
        print("10/10 Final Image Generated Successfully ✅")
        print("Pipeline Completed Successfully 🎉")
        print(f"You can check the image from here \033[92m{os.getcwd()}/pipe\033[0m folder 📁")
    except Exception as e:

        print(error_messages.get(step, "An unknown error occurred ❌"))
        print(f"Details: {e}")
