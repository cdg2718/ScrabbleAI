import pandas as pd
import time
from typing import Dict
from feature_engineering.board_parsing import parse_run_tile_representation
from game_logic.utils import TILE_ORDER, TILE_DIST

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


def parse_scrabble_line(line: str) -> Dict:
    """
    Parse a single line from the Scrabble dataset into structured features.

    Args:
        line (str): A single line from the dataset.

    Returns:
        dict: A dictionary with structured Scrabble game state features.
    """
    parts = line.strip().split()

    board_state = parts[0]
    board = parse_run_tile_representation(board_state)
    leave = list(parts[1].replace("/", ""))
    opp_score, player_score = map(int, parts[2].split("/"))
    score_diff = player_score - opp_score
    _, winProb, expDiff = map(float, parts[3].split(","))

    leave_vector = tile_vector(leave)
    
    unseen_tiles = dict(TILE_DIST)
    for el in board_state:
        if not el.isalpha():
            continue
        if el.islower():
            unseen_tiles["?"] -= 1
        else:
            unseen_tiles[el] -= 1

    for el in leave:
        unseen_tiles[el] -= 1
    
    return {
        "board": board,  # 15x15 matrix representation
        "board_rep": board_state,  # Original compact representation
        "score_diff": score_diff,
        "total_unseen_tiles": sum([v for _, v in unseen_tiles.items()]),  # Sanity check
        **{f"leave_{letter}": leave_vector[i] for i, letter in enumerate(TILE_ORDER)},
        **{f"unseen_{letter}": unseen_tiles[letter] for letter in TILE_ORDER},
        "winProb": winProb,
        "expPointDiff": expDiff
    }


def load_scrabble_data(file_path: str) -> pd.DataFrame:
    """
    Loads and processes the Scrabble dataset from a file.

    Args:
        file_path (str): Path to the dataset.

    Returns:
        pd.DataFrame: A DataFrame containing processed Scrabble game states.
    """
    training_data = []
    start_time = time.time()

    with open(file_path, 'r') as file:
        for line in file:
            training_data.append(parse_scrabble_line(line))

    elapsed_time = time.time() - start_time
    print(f"Data loaded in {elapsed_time:.4f} seconds")

    return pd.DataFrame(training_data)
