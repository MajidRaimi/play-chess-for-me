import numpy as np

from . import ChessPieceMapper

class FENConverter:
    @staticmethod
    def generate_fen(ptsT, ptsL, detections, boxes):
        rows = "87654321"
        cols = "abcdefgh"
        
        # Create a dictionary to store square coordinates
        squares = {}
        for col_idx, (x_start, x_end) in enumerate(zip(ptsT[:-1], ptsT[1:])):
            for row_idx, (y_start, y_end) in enumerate(zip(ptsL[:-1], ptsL[1:])):
                square_name = f"{cols[col_idx]}{rows[row_idx]}"
                squares[square_name] = np.array([[x_start[0], y_start[1]], [x_end[0], y_start[1]], 
                                                 [x_end[0], y_end[1]], [x_start[0], y_end[1]]])

        board_fen = []

        for row in rows:
            row_fen = []
            empty_count = 0
            for col in cols:
                square_name = f"{col}{row}"
                piece = ChessPieceMapper.connect_square_to_detection(detections, squares[square_name], boxes)

                if piece == "empty":
                    empty_count += 1
                else:
                    if empty_count > 0:
                        row_fen.append(str(empty_count))
                        empty_count = 0
                    row_fen.append(piece)
            if empty_count > 0:
                row_fen.append(str(empty_count))
            board_fen.append(''.join(row_fen))

        fen_notation = '/'.join(board_fen)
        return fen_notation
