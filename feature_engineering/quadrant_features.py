from feature_engineering.types import Board
from typing import Dict

def count_tiles_in_quadrants(board: Board) -> Dict[str, int]:
    """
    Counts the number of tiles in each quadrant of a Scrabble board.
    The middle row and middle column (row 7 and col 7) are excluded.

    Quadrants:
        - Upper Left  (UL)  → Rows 0-6, Cols 0-6
        - Upper Right (UR)  → Rows 0-6, Cols 8-14
        - Lower Left  (LL)  → Rows 8-14, Cols 0-6
        - Lower Right (LR)  → Rows 8-14, Cols 8-14

    Args:
        board (Board)

    Returns:
        Dict[str, int]: A dictionary with counts of tiles in each quadrant.
    """
    quadrant_counts = {
        "upper_left": 0,
        "upper_right": 0,
        "lower_left": 0,
        "lower_right": 0
    }

    for row in range(15):
        for col in range(15):
            if row == 7 or col == 7:  # Skip middle row and column
                continue

            if board[row][col] is not None:  # Tile is placed
                if row < 7 and col < 7:
                    quadrant_counts["upper_left"] += 1
                elif row < 7 and col > 7:
                    quadrant_counts["upper_right"] += 1
                elif row > 7 and col < 7:
                    quadrant_counts["lower_left"] += 1
                elif row > 7 and col > 7:
                    quadrant_counts["lower_right"] += 1

    return quadrant_counts
