from typing import List, Tuple, Optional, Dict

# Board representation: each tile is a letter (A-Z for normal, a-z for blanks) or None
Board = List[List[Optional[str]]]

# Define CrossCheck structure
class CrossCheck:
    def __init__(self, valid_letters: set, partial_sum: int, is_open_square: bool):
        self.valid_letters = valid_letters
        self.partial_sum = partial_sum
        self.is_open_square = is_open_square

CrossCheckBoard = List[List[Optional[CrossCheck]]]
# Open square cross-check (all letters valid)
open_square_cross_check = CrossCheck(set("ABCDEFGHIJKLMNOPQRSTUVWXYZ"), 0, True)