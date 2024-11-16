import chess
import chess.svg
import os
from contextlib import redirect_stdout
from html2image import Html2Image

class ImageGenerator:

    def __init__(self):
        pass

    @staticmethod
    def generate_image(fen, best_move_output=None):
        # Create the chess board
        board = chess.Board(fen)

        # Add arrows for the best move, if provided
        arrows = []
        if best_move_output:
            from_square = chess.parse_square(best_move_output["from"])
            to_square = chess.parse_square(best_move_output["to"])
            arrows = [(from_square, to_square)]

        # Use chess.svg to generate SVG data with arrows
        svg_data = chess.svg.board(board=board, arrows=arrows)

        # Create output path
        os.makedirs("pipe", exist_ok=True)
        png_path = os.path.join("pipe", "06_digital_image.png")

        # Suppress stdout output from html2image
        with open(os.devnull, 'w') as devnull:
            with redirect_stdout(devnull):
                # Convert SVG to PNG using html2image
                hti = Html2Image(
                    output_path='pipe',
                    custom_flags=['--headless=new', '--disable-gpu', '--log-level=3', '--silent'],
                )

                # Create HTML with the SVG and save as PNG
                html = f'''
                <html>
                    <body style="margin:0;padding:0;display:flex;justify-content:center;align-items:center;background:#fff;">
                        <div style="width:100%;height:100%;">
                            {svg_data.replace('<svg', '<svg width="100%" height="100%"')}
                        </div>
                    </body>
                </html>
                '''
                hti.screenshot(html_str=html, save_as="06_digital_image.png")
