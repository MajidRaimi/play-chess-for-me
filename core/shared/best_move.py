from requests import post
from dotenv import load_dotenv

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
    def format_fen(fen: str, turn: str = "w", castling: str = "KQkq", en_passant: str = "-", halfmove: int = 0, fullmove: int = 1) -> str:
        return f"{fen} {turn} {castling} {en_passant} {halfmove} {fullmove}"
