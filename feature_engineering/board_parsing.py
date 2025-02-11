from game_logic.types import Board

def parse_run_tile_representation(data: str) -> Board:
    """
    Parse a Scrabble run-tile representation into a 15x15 board.

    Args:
        data (str): The run-tile representation with rows separated by slashes.

    Returns:
        Board: A 15x15 board where each cell is either None, a letter (A-Z), or a blank (a-z).
    """
    board: Board = [[None for _ in range(15)] for _ in range(15)]  # Initialize 15x15 board with None

    rows = data.split('/')
    for row_index, row_data in enumerate(rows):
        col_index = 0
        i = 0

        while i < len(row_data):
            if row_data[i].isdigit():  # Consecutive empty squares
                num_empty = int(row_data[i])
                while i + 1 < len(row_data) and row_data[i + 1].isdigit():
                    i += 1
                    num_empty = num_empty * 10 + int(row_data[i])
                col_index += num_empty
                i += 1

            elif row_data[i].isalpha():  # Read tiles
                board[row_index][col_index] = row_data[i]
                col_index += 1
                i += 1

            else:  # Ignore unexpected characters
                i += 1

    return board
