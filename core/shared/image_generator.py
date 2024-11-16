import chess
import chess.svg
import svgwrite
from PIL import Image, ImageDraw
import os
import sys
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO

class ImageGenerator:

    def __init__(self):
        pass

    @staticmethod
    def generate_image(fen, best_move_output=None):
        # Create the chess board
        board = chess.Board(fen)

        # Use chess.svg to generate SVG data
        svg_data = chess.svg.board(board=board)

        # Create output path
        os.makedirs("pipe", exist_ok=True)
        png_path = os.path.join("pipe", "06_digital_image.png")

        # Redirect stdout to devnull to suppress output
        import sys
        with open(os.devnull, 'w') as devnull:
            with redirect_stdout(devnull):
                # Convert SVG to PNG using html2image
                from html2image import Html2Image
                hti = Html2Image(
                    output_path='pipe',
                    custom_flags=['--headless=new', '--disable-gpu', '--log-level=3', '--silent'],
                    size=(400, 400)
                )
                
                # Create HTML with the SVG and save as PNG
                html = f'<html><body style="margin:0;padding:0;">{svg_data}</body></html>'
                hti.screenshot(html_str=html, save_as="06_digital_image.png", size=(400, 400))
