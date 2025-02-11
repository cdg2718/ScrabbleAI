from typing import List, Tuple
from game_logic.types import Board, CrossCheckBoard

def compute_7_letter_bingo_lanes(
    board: Board, crosscheck_board_h: CrossCheckBoard, crosscheck_board_v: CrossCheckBoard
) -> List[Tuple[int, int, str, int]]:
    """
    Computes 7-letter bingo lanes by checking valid cross-check spaces.
    A play can only go through one cross-check constraint before stopping.

    Args:
        board (Board): The Scrabble board (15x15 grid).
        crosscheck_board_h (CrossCheckBoard): Horizontal cross-check constraints.
        crosscheck_board_v (CrossCheckBoard): Vertical cross-check constraints.

    Returns:
        List[Tuple[int, int, str, int]]: A list of (row, col, direction, lane_size) tuples.
    """

    # If board is empty, the only valid lane is (7, 7, "H", 1)
    if board[7][7] is None:
        return [(7, 7, "H", 1)]

    bingo_lanes = []

    def is_valid_bingo_start(r, c, crosscheck_board, direction):
        """Checks if a space is a valid starting point for a 7-letter bingo."""
        if board[r][c] is not None:
            return False  # Cannot play through an existing tile
        if crosscheck_board[r][c] is None or crosscheck_board[r][c].is_open_square:
            return False  # Must be a constrained space
        if len(crosscheck_board[r][c].valid_letters) == 0:
            return False  # No valid letters to play through

        # Ensure the space is not trapped between two tiles
        if direction == "H":
            if (c > 0 and board[r][c - 1] is not None) or (c < 14 and board[r][c + 1] is not None):
                return False  # Tile on both left & right
        elif direction == "V":
            if (r > 0 and board[r - 1][c] is not None) or (r < 14 and board[r + 1][c] is not None):
                return False  # Tile above & below

        return True  # Valid starting point

    def count_empty_spaces(r, c, dr, dc, crosscheck_board):
        """Counts empty spaces until hitting a tile or another cross-check."""
        count = 0

        for i in range(1, 7):  # Maximum 7-letter word placement
            r_next, c_next = r + i * dr, c + i * dc

            # Out of bounds check
            if not (0 <= r_next < 15 and 0 <= c_next < 15):
                break  

            # Stop at the first occupied tile
            if board[r_next][c_next] is not None:
                break  

            # Stop at the first cross-check (we only play through one)
            if crosscheck_board[r_next][c_next] is not None:
                break  

            count += 1  # Valid empty space

        return count

    # Iterate through the board looking for valid cross-check spaces
    for row in range(15):
        for col in range(15):
            # Check horizontal lanes
            if is_valid_bingo_start(row, col, crosscheck_board_h, "H"):
                left_spaces = count_empty_spaces(row, col, 0, -1, crosscheck_board_h)
                right_spaces = count_empty_spaces(row, col, 0, 1, crosscheck_board_h)
                lane_size_h = max(0, left_spaces + right_spaces - 5)  # Need 6 open spaces around a tile
                if lane_size_h > 0:
                    bingo_lanes.append((row, col, "H", lane_size_h))

            # Check vertical lanes
            if is_valid_bingo_start(row, col, crosscheck_board_v, "V"):
                up_spaces = count_empty_spaces(row, col, -1, 0, crosscheck_board_v)
                down_spaces = count_empty_spaces(row, col, 1, 0, crosscheck_board_v)
                lane_size_v = max(0, up_spaces + down_spaces - 5)  # Need 6 open spaces around a tile
                if lane_size_v > 0:
                    bingo_lanes.append((row, col, "V", lane_size_v))

    return bingo_lanes



def compute_8_letter_bingo_lanes(
    board: Board, crosscheck_board_h: CrossCheckBoard, crosscheck_board_v: CrossCheckBoard
) -> List[Tuple[int, int, str, int]]:
    """
    Computes 8-letter bingo lanes by checking spaces around existing tiles.

    Args:
        board (Board): The Scrabble board (15x15 grid).
        crosscheck_board_h (CrossCheckBoard): Horizontal cross-check constraints.
        crosscheck_board_v (CrossCheckBoard): Vertical cross-check constraints.

    Returns:
        List[Tuple[int, int, str, int]]: A list of (row, col, direction, lane_size) tuples.
    """
    bingo_lanes = []

    def is_valid_extension(r, c, r_next, c_next, crosscheck_board):
        """Returns True if we can extend a word into this space and the next space."""
        if not (0 <= r < 15 and 0 <= c < 15):
            return False  # Out of bounds
        if board[r][c] is not None:
            return False  # Occupied
        if crosscheck_board[r][c] is not None and len(crosscheck_board[r][c].valid_letters) == 0:
            return False  # Cross-check restriction
        if 0 <= r_next < 15 and 0 <= c_next < 15 and (
            board[r_next][c_next] is not None
        ):
            return False  # Next space blocked
        return True

    def has_adjacent_tile_in_direction(r, c, direction):
        """Checks if a tile has an adjacent tile in the given direction."""
        if direction == "H":
            return (c > 0 and board[r][c - 1] is not None) or (c < 14 and board[r][c + 1] is not None)
        if direction == "V":
            return (r > 0 and board[r - 1][c] is not None) or (r < 14 and board[r + 1][c] is not None)
        return False

    # Scan board for existing tiles
    for row in range(15):
        for col in range(15):
            if board[row][col] is None:
                continue  # Skip empty spaces

            # Horizontal playability: Skip if adjacent horizontal tile exists
            if not has_adjacent_tile_in_direction(row, col, "H"):
                left_spaces = 0
                right_spaces = 0

                for i in range(1, 8):
                    if is_valid_extension(row, col - i, row, col - i - 1, crosscheck_board_h):
                        left_spaces += 1
                    else:
                        break

                for i in range(1, 8):
                    if is_valid_extension(row, col + i, row, col + i + 1, crosscheck_board_h):
                        right_spaces += 1
                    else:
                        break

                lane_size_h = max(0, left_spaces + right_spaces - 6)
                if lane_size_h > 0:
                    bingo_lanes.append((row, col, "H", lane_size_h))

            # Vertical playability: Skip if adjacent vertical tile exists
            if not has_adjacent_tile_in_direction(row, col, "V"):
                up_spaces = 0
                down_spaces = 0

                for i in range(1, 8):
                    if is_valid_extension(row - i, col, row - i - 1, col, crosscheck_board_v):
                        up_spaces += 1
                    else:
                        break

                for i in range(1, 8):
                    if is_valid_extension(row + i, col, row + i + 1, col, crosscheck_board_v):
                        down_spaces += 1
                    else:
                        break

                lane_size_v = max(0, up_spaces + down_spaces - 6)
                if lane_size_v > 0:
                    bingo_lanes.append((row, col, "V", lane_size_v))

    return bingo_lanes
