from requests import post
from dotenv import load_dotenv
import chess

class BestMove:
    def __init__(self):
        load_dotenv()
        pass

    @staticmethod
    def get_best_move(fen: str):
        response = post("https://chess-api.com/v1", json={"fen": fen})
        data = response.json()

        if data['type'] == 'error':
            return None

        return data


    @staticmethod
    def format_fen(fen: str, turn: str = "w", castling: str = "-", en_passant: str = "-", halfmove: int = 0, fullmove: int = 1) -> str:
        """
        Validates, adjusts, and formats the FEN string to ensure it's usable.
        """
        try:

            board = chess.Board(fen)
        except ValueError as e:


            if "KQkq" in fen:
                castling = "-"


            fen_parts = fen.split(" ")
            fen = " ".join(fen_parts[:4])


        formatted_fen = f"{fen} {turn} {castling} {en_passant} {halfmove} {fullmove}"
        return formatted_fen
