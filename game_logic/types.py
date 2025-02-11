from typing import List, Tuple, Optional, Dict

# Board representation: each tile is a letter (A-Z for normal, a-z for blanks) or None
Board = List[List[Optional[str]]]

# Tile values based on Scrabble scoring
TILE_VALUES: Dict[str, int] = {
    "A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2, "H": 4, "I": 1,
    "J": 8, "K": 5, "L": 1, "M": 3, "N": 1, "O": 1, "P": 3, "Q": 10, "R": 1,
    "S": 1, "T": 1, "U": 1, "V": 4, "W": 4, "X": 8, "Y": 4, "Z": 10
}

# Blanks (lowercase a-z) have a score of 0
for char in "abcdefghijklmnopqrstuvwxyz":
    TILE_VALUES[char] = 0

def get_tile_value(letter: str) -> int:
    """Returns the score value of a tile, handling blanks (lowercase) as 0."""
    return TILE_VALUES.get(letter.upper(), 0)

# Define CrossCheck structure
class CrossCheck:
    def __init__(self, valid_letters: set, partial_sum: int, is_open_square: bool):
        self.valid_letters = valid_letters
        self.partial_sum = partial_sum
        self.is_open_square = is_open_square

# Open square cross-check (all letters valid)
open_square_cross_check = CrossCheck(set("ABCDEFGHIJKLMNOPQRSTUVWXYZ"), 0, True)

# Mapping functions
def map_key(row: int, col: int) -> str:
    return f"{row}-{col}"

def row_col_from_key(key: str) -> Tuple[int, int]:
    row, col = map(int, key.split("-"))
    return row, col
