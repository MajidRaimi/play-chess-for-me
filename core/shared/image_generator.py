import chess
import chess.svg
from PIL import Image
import cairosvg
import os
from io import BytesIO


class ImageGenerator:
    def __init__(self):
        pass

    @staticmethod
    def generate_image(fen, best_move_output=None):
        board = chess.Board(fen)

        # Generate arrows for the best move if provided
        arrows = []
        if best_move_output:
            from_square = chess.parse_square(best_move_output["from"])
            to_square = chess.parse_square(best_move_output["to"])
            arrows = [(from_square, to_square)]

        # Create the SVG representation of the chessboard
        svg_data = chess.svg.board(board=board, arrows=arrows)

        # Use CairoSVG to convert SVG to PNG directly
        png_output_path = os.path.join("pipe/06_digital_image.png")
        os.makedirs(os.path.dirname(png_output_path), exist_ok=True)  # Ensure directory exists

        # Convert SVG data to PNG using cairosvg
        cairosvg.svg2png(bytestring=svg_data.encode("utf-8"), write_to=png_output_path)
