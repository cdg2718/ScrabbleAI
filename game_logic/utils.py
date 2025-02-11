from typing import List, Dict, TypeVar

import numpy as np

from game_logic.types import Board, CrossCheckBoard

TILE_DIST = {
    "A": 9, "B": 2, "C": 2, "D": 4, "E": 12, "F": 2, "G": 3, "H": 2, "I": 9,
    "J": 1, "K": 1, "L": 4, "M": 2, "N": 6, "O": 8, "P": 2, "Q": 1, "R": 6,
    "S": 4, "T": 6, "U": 4, "V": 2, "W": 2, "X": 1, "Y": 2, "Z": 1, "?": 2
}

TILE_ORDER = list(TILE_DIST.keys())

SPECIAL_TILE_ICONS = {
    "TWS": "★", 
    "DWS": "✦", 
    "TLS": "▲",
    "DLS": "◆",
}

SPECIAL_TILES_LOCATIONS = [
    ["TWS", None, None, "DLS", None, None, None, "TWS", None, None, None, "DLS", None, None, "TWS"],
    [None, "DWS", None, None, None, "TLS", None, None, None, "TLS", None, None, None, "DWS", None],
    [None, None, "DWS", None, None, None, "DLS", None, "DLS", None, None, None, "DWS", None, None],
    ["DLS", None, None, "DWS", None, None, None, "DLS", None, None, None, "DWS", None, None, "DLS"],
    [None, None, None, None, "DWS", None, None, None, None, None, "DWS", None, None, None, None],
    [None, "TLS", None, None, None, "TLS", None, None, None, "TLS", None, None, None, "TLS", None],
    [None, None, "DLS", None, None, None, "DLS", None, "DLS", None, None, None, "DLS", None, None],
    ["TWS", None, None, "DLS", None, None, None, "★", None, None, None, "DLS", None, None, "TWS"],  # Center square marked ★
    [None, None, "DLS", None, None, None, "DLS", None, "DLS", None, None, None, "DLS", None, None],
    [None, "TLS", None, None, None, "TLS", None, None, None, "TLS", None, None, None, "TLS", None],
    [None, None, None, None, "DWS", None, None, None, None, None, "DWS", None, None, None, None],
    ["DLS", None, None, "DWS", None, None, None, "DLS", None, None, None, "DWS", None, None, "DLS"],
    [None, None, "DWS", None, None, None, "DLS", None, "DLS", None, None, None, "DWS", None, None],
    [None, "DWS", None, None, None, "TLS", None, None, None, "TLS", None, None, None, "DWS", None],
    ["TWS", None, None, "DLS", None, None, None, "TWS", None, None, None, "DLS", None, None, "TWS"],
]

# Tile values based on Scrabble scoring
TILE_VALUES: Dict[str, int] = {
    "A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2, "H": 4, "I": 1,
    "J": 8, "K": 5, "L": 1, "M": 3, "N": 1, "O": 1, "P": 3, "Q": 10, "R": 1,
    "S": 1, "T": 1, "U": 1, "V": 4, "W": 4, "X": 8, "Y": 4, "Z": 10
}

# Blanks (lowercase a-z) have a score of 0
for char in "abcdefghijklmnopqrstuvwxyz":
    TILE_VALUES[char] = 0

T = TypeVar("T")  # Allows any data type

def transpose(matrix: List[List[T]]) -> List[List[T]]:
    """Generically transposes any list of lists."""
    return [list(row) for row in zip(*matrix)]


def get_tile_value(letter: str) -> int:
    """Returns the score value of a tile, handling blanks (lowercase) as 0."""
    return TILE_VALUES.get(letter, 0)

def pretty_print_board(board: Board) -> None:
    """
    Prints a Scrabble board in a human-readable format with special tile indicators.
    
    - Empty squares are represented by special tile indicators where applicable.
    - Tile letters are shown in uppercase for normal tiles, lowercase for blank tiles.
    - Column spacing is increased for better aspect ratio.

    Args:
        board (Board): A 15x15 list of lists, where each cell is None or a letter.
    """
    for row_idx, row in enumerate(board):
        row_str = f""  # Row header
        for col_idx, cell in enumerate(row):
            if cell is not None:  # Letter tile present
                row_str += f" {cell} "
            elif SPECIAL_TILES_LOCATIONS[row_idx][col_idx]:  # Special tile
                row_str += f" {SPECIAL_TILE_ICONS[SPECIAL_TILES_LOCATIONS[row_idx][col_idx]]} "
            else:
                row_str += " . "
        print(row_str)

def pretty_print_board_with_crosschecks(board: Board, cross_check_board: CrossCheckBoard) -> None:
    """
    Prints a Scrabble board with both tile placements and cross-check constraints.

    - Empty squares show either:
      - The number of valid cross-check letters (if cross-checks exist).
      - Special tile indicators (e.g., TWS, DWS, TLS, DLS).
      - A "." if completely empty.
    - Tile letters are shown in uppercase for normal tiles, lowercase for blanks.
    - Ensures consistent spacing even for single/double digit numbers.

    Args:
        board (Board): A 15x15 list of lists, where each cell is None or a letter.
        cross_check_board (CrossCheckBoard): A 15x15 list of lists, where each cell is None or a CrossCheck object.
    """
    CELL_WIDTH = 3  # Fixed width for consistent alignment

    for row_idx in range(15):
        row_str = ""
        for col_idx in range(15):
            tile = board[row_idx][col_idx]
            cross_check = cross_check_board[row_idx][col_idx]

            if tile is not None:  # Letter tile present
                cell_str = tile  # Single letter
            elif cross_check is not None and not cross_check.is_open_square:  # Show valid letter count
                cell_str = str(len(cross_check.valid_letters))  # Show count
            elif cross_check is not None and cross_check.is_open_square:
                cell_str = "○"  # Open squares
            elif SPECIAL_TILES_LOCATIONS[row_idx][col_idx]:  # Special tile
                cell_str = SPECIAL_TILE_ICONS[SPECIAL_TILES_LOCATIONS[row_idx][col_idx]]
            else:
                cell_str = "."  # Empty square
            
            row_str += cell_str.center(CELL_WIDTH)  # Ensures all cells have the same width

        print(row_str)
