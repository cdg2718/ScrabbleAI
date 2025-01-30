from typing import List, Dict
import numpy as np

TILE_DIST = {
    "A": 9, "B": 2, "C": 2, "D": 4, "E": 12, "F": 2, "G": 3, "H": 2, "I": 9,
    "J": 1, "K": 1, "L": 4, "M": 2, "N": 6, "O": 8, "P": 2, "Q": 1, "R": 6,
    "S": 4, "T": 6, "U": 4, "V": 2, "W": 2, "X": 1, "Y": 2, "Z": 1, "?": 2
}

TILE_ORDER = list(TILE_DIST.keys())  # A-Z + blank

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
