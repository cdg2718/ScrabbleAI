from typing import Dict, Set
from game_logic.dawg import DAWG
from game_logic.types import Board, CrossCheck, open_square_cross_check
from game_logic.utils import map_key, get_tile_value

def find_anchors_with_cross_checks(board: Board, dawg: DAWG) -> Dict[str, CrossCheck]:
    cross_check_map: Dict[str, CrossCheck] = {}

    if board[7][7] is None:
        cross_check_map[map_key(7, 7)] = open_square_cross_check
        return cross_check_map

    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] is None and has_adjacent_tile(board, row, col):
                cross_check = compute_cross_check(board, row, col, dawg)
                cross_check_map[map_key(row, col)] = cross_check

    return cross_check_map

def has_adjacent_tile(board: Board, row: int, col: int) -> bool:
    return (
        (row > 0 and board[row - 1][col] is not None) or
        (row < len(board) - 1 and board[row + 1][col] is not None) or
        (col > 0 and board[row][col - 1] is not None) or
        (col < len(board[0]) - 1 and board[row][col + 1] is not None)
    )

def compute_cross_check(board: Board, row: int, col: int, dawg: DAWG) -> CrossCheck:
    valid_letters: Set[str] = set()
    prefix, suffix, partial_sum = get_adjacent_letters_and_sum(board, row, col)

    if prefix == "" and suffix == "":
        return open_square_cross_check

    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if dawg.is_valid_word(prefix + letter + suffix):
            valid_letters.add(letter)

    return CrossCheck(valid_letters, partial_sum, False)

def get_adjacent_letters_and_sum(board: Board, row: int, col: int) -> tuple:
    prefix, suffix, partial_sum = "", "", 0

    for r in range(row - 1, -1, -1):
        tile = board[r][col]
        if tile is None:
            break
        prefix = tile + prefix
        partial_sum += get_tile_value(tile)

    for r in range(row + 1, len(board)):
        tile = board[r][col]
        if tile is None:
            break
        suffix += tile
        partial_sum += get_tile_value(tile)

    return prefix, suffix, partial_sum
