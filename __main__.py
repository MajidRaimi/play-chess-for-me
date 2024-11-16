import argparse
from pipeline import pipeline


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the chess program with an image path.")
    parser.add_argument("image_path", type=str, help="Path to the chessboard image.")
    args = parser.parse_args()

    pipeline(args.image_path)
