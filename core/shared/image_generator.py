import chess
import chess.svg
from PIL import Image
import cairosvg
import os

class ImageGenerator:

    def __init__(self):
        pass

    @staticmethod
    def generate_image(fen, best_move_output=None):
        board = chess.Board(fen)
        
        arrows = []
        if best_move_output:
            from_square = chess.parse_square(best_move_output["from"])
            to_square = chess.parse_square(best_move_output["to"])
            arrows = [(from_square, to_square)]

        svg_data = chess.svg.board(board=board, arrows=arrows)

        output_path = os.path.join("pipe/06_digital_image.png")
        png_data = cairosvg.svg2png(bytestring=svg_data)
        with open(output_path, "wb") as f:
            f.write(png_data)



fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
best_move_output = {
    'from': 'e2',
    'to': 'e4',
    'move': 'e2e4',
    'san': 'e4'
}

ImageGenerator.generate_image(fen, best_move_output)
