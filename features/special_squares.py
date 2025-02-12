from typing import List, Tuple
from game_logic.types import Board, CrossCheckBoard
from game_logic.utils import SPECIAL_TILES_LOCATIONS


SPECIAL_TILES_CONNECTIONS = {
    ('TWS', 'TWS'): [
        ((0, 0), (0, 7)), ((0, 7), (0, 14)),
        ((14, 0), (14, 7)), ((14, 7), (14, 14)),
        ((0, 0), (7, 0)), ((7, 0), (14, 0)),
        ((0, 14), (7, 14)), ((7, 14), (14, 14))
    ],
    ('DWS', 'TLS'): [
        ((1, 1), (1, 5)), ((1, 9), (1, 13)),
        ((13, 1), (13, 5)), ((13, 9), (13, 13)),
        ((1, 1), (5, 1)), ((9, 1), (13, 1)),
        ((1, 13), (5, 13)), ((9, 13), (13, 13))
    ],
    ('DWS', 'DWS'): [
        ((4, 4), (4, 10)), ((10, 4), (10, 10)),
        ((4, 4), (10, 4)), ((4, 10), (10, 10)),
    ],
    ('DLS', 'TWS'): [
        ((0, 0), (0, 3)), ((0, 3), (0, 7)), ((0, 7), (0, 11)), ((0, 11), (0, 14)),
        ((7, 0), (7, 3)), ((7, 11), (7, 14)), ((14, 0), (14, 3)), ((14, 3), (14, 7)),
        ((14, 7), (14, 11)), ((14, 11), (14, 14)), ((0, 0), (3, 0)), ((3, 0), (7, 0)),
        ((7, 0), (11, 0)), ((11, 0), (14, 0)), ((0, 7), (3, 7)), ((11, 7), (14, 7)),
        ((0, 14), (3, 14)), ((3, 14), (7, 14)), ((7, 14), (11, 14)), ((11, 14), (14, 14))
    ]
}


def is_accessible_special_tile(
    row: int, col: int, board: Board, crosscheck_board_h: CrossCheckBoard, crosscheck_board_v: CrossCheckBoard
) -> bool:
    """
    Determines if a TWS or DWS tile is accessible to an opponent.

    Args:
        row (int): Row index of the special square.
        col (int): Column index of the special square.
        board (Board): 15x15 Scrabble board.
        crosscheck_board_h (CrossCheckBoard): Horizontal cross-check constraints.
        crosscheck_board_v (CrossCheckBoard): Vertical cross-check constraints.

    Returns:
        bool: True if the special square is accessible, False otherwise.
    """
    # 1️⃣ If a cross-check exists here and has a non-zero valid_letter set → Immediately accessible!
    if ((crosscheck_board_h[row][col] and crosscheck_board_h[row][col].valid_letters) or 
        (crosscheck_board_v[row][col] and crosscheck_board_v[row][col].valid_letters)):
        return True  

    # 2️⃣ Check if the special tile is unoccupied
    if board[row][col] is not None:
        return False  # Tile already occupied

    # 3️⃣ Ensure it's not blocked by **groups of tiles**
    def has_blocking_group(r: int, c: int) -> bool:
        """
        Checks if a tile is blocked by two adjacent tiles in a given direction.
        """
        directions = {
            "left":  [(0, -2), (0, -1)],  # Two spaces left
            "right": [(0, 1), (0, 2)],   # Two spaces right
            "up":    [(-1, 0), (-2, 0)],  # Two spaces above
            "down":  [(1, 0), (2, 0)]    # Two spaces below
        }

        for positions in directions.values():
            if all(0 <= r+dr < 15 and 0 <= c+dc < 15 and board[r+dr][c+dc] is not None for dr, dc in positions):
                return True  # Blocked by at least two tiles in one direction

        return False  # No blocking groups

    def has_immediate_two_adjacent(r: int, c: int, board: Board) -> bool:
        """
        Checks if the special tile is directly next to at least two adjacent tiles, even if they mix directions.
        """
        adjacent_positions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # Left, Right, Up, Down
    
        adjacent_count = sum(
            1 for dr, dc in adjacent_positions
            if 0 <= r + dr < 15 and 0 <= c + dc < 15 and board[r + dr][c + dc] is not None
        )
    
        return adjacent_count >= 2  # Blocked if at least two adjacent tiles exist

    if has_blocking_group(row, col) or has_immediate_two_adjacent(row, col, board):
        return False

    # 4️⃣ Look up to 7 spaces away for isolated tiles or cross-check access
    if (
        can_reach_within_7(row, col, 0, -1, board, crosscheck_board_h) or  # Left
        can_reach_within_7(row, col, 0, 1, board, crosscheck_board_h) or   # Right
        can_reach_within_7(row, col, -1, 0, board, crosscheck_board_v) or  # Up
        can_reach_within_7(row, col, 1, 0, board, crosscheck_board_v)      # Down
    ):
        return True

    return False  # No valid access route


def can_reach_within_7(r: int, c: int, dr: int, dc: int, board: Board, crosscheck_board: CrossCheckBoard) -> bool:
    """
    Determines if the special square can be reached within 7 spaces.

    Conditions:
    - A **single tile** is fine **if the next space is empty**.
    - A **cross-check** is fine **if no two tiles immediately follow it**.

    Args:
        r (int): Row index of the special square.
        c (int): Column index of the special square.
        dr (int): Row direction (-1 for up, 1 for down, 0 for horizontal).
        dc (int): Column direction (-1 for left, 1 for right, 0 for vertical).
        board (Board): 15x15 Scrabble board.
        crosscheck_board (CrossCheckBoard): Cross-check constraints.

    Returns:
        bool: True if accessible within 7 spaces, False otherwise.
    """
    for i in range(1, 8):  # Max 7 spaces
        r_next, c_next = r + i * dr, c + i * dc

        if not (0 <= r_next < 15 and 0 <= c_next < 15):
            return False  # Out of bounds

        current_tile = board[r_next][c_next]

        # Case 1️⃣: If we hit a tile, check if the next space is empty
        if current_tile is not None:
            r_next_next, c_next_next = r_next + dr, c_next + dc
            if 0 <= r_next_next < 15 and 0 <= c_next_next < 15 and board[r_next_next][c_next_next] is not None:
                return False  # Tile immediately after → Blocked
            return True  # Otherwise, it's accessible

        # Case 2️⃣: If we hit a cross-check, check if the next two spaces are not both occupied
        crosscheck = crosscheck_board[r_next][c_next]
        if crosscheck and crosscheck.is_open_square:
            crosscheck = None

        if(crosscheck and len(crosscheck.valid_letters) == 0):
            return False
            
        if crosscheck and len(crosscheck.valid_letters) > 0:
            r_next_next, c_next_next = r_next + dr, c_next + dc
            r_next_next2, c_next_next2 = r_next_next + dr, c_next_next + dc

            if (0 <= r_next_next < 15 and 0 <= c_next_next < 15 and board[r_next_next][c_next_next] is not None and
                0 <= r_next_next2 < 15 and 0 <= c_next_next2 < 15 and board[r_next_next2][c_next_next2] is not None):
                return False  # Two tiles immediately after cross-check → Blocked
            
            return True  # Otherwise, it's accessible

    return False  # No valid access found


def compute_accessible_special_tiles(board: Board, crosscheck_board_h: CrossCheckBoard, crosscheck_board_v: CrossCheckBoard) -> Tuple[int, int]:
    """
    Computes the number of accessible TWS and DWS tiles on the board.

    Args:
        board (Board): 15x15 Scrabble board.
        crosscheck_board_h (CrossCheckBoard): Horizontal cross-check constraints.
        crosscheck_board_v (CrossCheckBoard): Vertical cross-check constraints.

    Returns:
        (int, int): Tuple containing (accessible TWS count, accessible DWS count)
    """
    tws_count = 0
    dws_count = 0

    for row in range(15):
        for col in range(15):
            tile_type = SPECIAL_TILES_LOCATIONS[row][col]
            if tile_type in {"TWS", "DWS"}:
                if is_accessible_special_tile(row, col, board, crosscheck_board_h, crosscheck_board_v):
                    if tile_type == "TWS":
                        tws_count += 1
                    elif tile_type == "DWS":
                        dws_count += 1

    return tws_count, dws_count


def is_accessible_connection(
    start: Tuple[int, int],
    end: Tuple[int, int],
    board: Board,
    crosscheck_board_h: CrossCheckBoard,
    crosscheck_board_v: CrossCheckBoard,
    special_type: str
) -> bool:
    """
    Determines if there is an accessible connection between two special tiles.

    Args:
        start (Tuple[int, int]): Coordinates of the first special tile.
        end (Tuple[int, int]): Coordinates of the second special tile.
        board (Board): 15x15 Scrabble board.
        crosscheck_board_h (CrossCheckBoard): Horizontal cross-check constraints.
        crosscheck_board_v (CrossCheckBoard): Vertical cross-check constraints.
        special_type (str): The type of special tile combination (e.g., "TWS/TWS").

    Returns:
        bool: True if the special tile connection is accessible, False otherwise.
    """
    r1, c1 = start
    r2, c2 = end

    # If either special tile is occupied, connection is blocked
    if board[r1][c1] is not None or board[r2][c2] is not None:
        return False

    # Determine the direction of the connection
    if r1 == r2:  # Horizontal connection
        r, c_min, c_max = r1, min(c1, c2), max(c1, c2)
        crosscheck_board = crosscheck_board_h
    else:  # Vertical connection
        c, r_min, r_max = c1, min(r1, r2), max(r1, r2)
        crosscheck_board = crosscheck_board_v

    num_tiles_between = 0
    num_valid_cross_checks = 0

    # Check if either start or end position has a cross-check
    start_crosscheck = crosscheck_board[r1][c1] if crosscheck_board[r1][c1] and not crosscheck_board[r1][c1].is_open_square else None
    end_crosscheck = crosscheck_board[r2][c2] if crosscheck_board[r2][c2] and not crosscheck_board[r2][c2].is_open_square else None

    # If either start or end position has a cross-check with an empty valid letter set, it's blocked
    if (start_crosscheck and len(start_crosscheck.valid_letters) == 0) or \
       (end_crosscheck and len(end_crosscheck.valid_letters) == 0):
        return False

    # Count valid cross-checks at start and end positions
    if start_crosscheck and len(start_crosscheck.valid_letters) > 0:
        num_valid_cross_checks += 1
    if end_crosscheck and len(end_crosscheck.valid_letters) > 0:
        num_valid_cross_checks += 1

    # Iterate through all spaces between the two tiles
    if r1 == r2:  # Horizontal connection
        for c in range(c_min + 1, c_max):
            if board[r][c] is not None:
                num_tiles_between += 1
            elif crosscheck_board[r][c]:
                crosscheck = crosscheck_board[r][c]
                if crosscheck.is_open_square:
                    continue
                if len(crosscheck.valid_letters) == 0:
                    return False  # Blocked because cross-check has no valid letters
                num_valid_cross_checks += 1
    else:  # Vertical connection
        for r in range(r_min + 1, r_max):
            if board[r][c] is not None:
                num_tiles_between += 1
            elif crosscheck_board[r][c]:
                crosscheck = crosscheck_board[r][c]
                if crosscheck.is_open_square:
                    continue
                if len(crosscheck.valid_letters) == 0:
                    return False  # Blocked because cross-check has no valid letters
                num_valid_cross_checks += 1

    # Access rules:
    if num_tiles_between > 1 or num_valid_cross_checks > 1:
        return False
    if num_tiles_between == 0 and num_valid_cross_checks == 0:
        return False
    if special_type == "TWS/TWS":
        if num_tiles_between == 1 and num_valid_cross_checks == 0:
            return True
        else:
            return False
    if num_tiles_between == 1 or num_valid_cross_checks == 1:
        return True

    return False  # No valid connection found


def compute_accessible_special_connections(
    board: Board, crosscheck_board_h: CrossCheckBoard, crosscheck_board_v: CrossCheckBoard
) -> Dict[str, int]:
    """
    Computes the number of accessible special tile connections.

    Args:
        board (Board): 15x15 Scrabble board.
        crosscheck_board_h (CrossCheckBoard): Horizontal cross-check constraints.
        crosscheck_board_v (CrossCheckBoard): Vertical cross-check constraints.

    Returns:
        Dict[str, int]: Dictionary with counts of accessible connections for each combination type.
    """
    accessible_connections = {
        "TWS/TWS": 0,
        "DWS/TLS": 0,
        "DWS/DWS": 0,
        "DLS/TWS": 0
    }

    for special_type, pairs in SPECIAL_TILES_CONNECTIONS.items():
        for start, end in pairs:
            if is_accessible_connection(start, end, board, crosscheck_board_h, crosscheck_board_v, "/".join(special_type)):
                accessible_connections["/".join(special_type)] += 1

    return accessible_connections

