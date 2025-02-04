from typing import List, Dict
import numpy as np

from feature_engineering.types import Board

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


def tile_vector(tiles: List[str]) -> np.ndarray:
    """
    Converts a list of letters into a 27D tile count vector.

    Args:
        tiles (List[str]): List of tile characters.

    Returns:
        np.ndarray: 27D vector where each index corresponds to a tile count.
    """
    tile_counts = {tile: 0 for tile in TILE_ORDER}
    for tile in tiles:
        if tile in tile_counts:
            tile_counts[tile] += 1
    
    return np.array([tile_counts[tile] for tile in TILE_ORDER], dtype=np.int32)


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