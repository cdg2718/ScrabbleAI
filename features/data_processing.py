import pandas as pd
import numpy as np
import time
from tqdm import tqdm
from typing import Dict, List

from features.board_parsing import parse_run_tile_representation
from features.bingo_lanes import compute_8_letter_bingo_lanes, compute_7_letter_bingo_lanes

from game_logic.utils import TILE_ORDER, TILE_DIST, transpose
from game_logic.crosschecks import find_anchors_with_cross_checks
from game_logic.dawg import DAWG

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


def parse_scrabble_line(line: str, dawg: DAWG) -> Dict:
    """
    Parse a single line from the Scrabble dataset into structured features.

    Args:
        line (str): A single line from the dataset.
        dawg (DAWG): The DAWG dictionary for cross-check computations.

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

    # Compute cross-checks
    cs_h = find_anchors_with_cross_checks(board, dawg)
    cs_v = transpose(find_anchors_with_cross_checks(transpose(board), dawg))

    # Compute 8-letter bingo lanes
    bingo_lanes_8 = compute_8_letter_bingo_lanes(board, cs_v, cs_h)
    total_bingos_8 = sum(lane[3] for lane in bingo_lanes_8)

    # Compute 7-letter bingo lanes
    bingo_lanes_7 = compute_7_letter_bingo_lanes(board, cs_v, cs_h)
    total_bingos_7 = sum(lane[3] for lane in bingo_lanes_7)

    return {
        "board": board,  # 15x15 matrix representation
        "board_rep": board_state,  # Original compact representation
        "score_diff": score_diff,
        "total_unseen_tiles": sum(unseen_tiles.values()),  # Sanity check
        **{f"leave_{letter}": leave_vector[i] for i, letter in enumerate(TILE_ORDER)},
        **{f"unseen_{letter}": unseen_tiles[letter] for letter in TILE_ORDER},
        "winProb": winProb,
        "expPointDiff": expDiff,
        "cs_h": cs_h,
        "cs_v": cs_v,
        "8_letter_bingo_lanes_list": bingo_lanes_8,
        "8_letter_bingos": total_bingos_8,
        "7_letter_bingo_lanes_list": bingo_lanes_7,
        "7_letter_bingos": total_bingos_7,
    }


def load_scrabble_data(file_path: str, dawg: DAWG) -> pd.DataFrame:
    """
    Loads and processes the Scrabble dataset from a file.

    Args:
        file_path (str): Path to the dataset.
        dawg (DAWG): The DAWG dictionary for cross-check computations.

    Returns:
        pd.DataFrame: A DataFrame containing processed Scrabble game states.
    """
    training_data = []
    start_time = time.time()

    with open(file_path, "r") as file:
        for line in tqdm(file, desc="Processing Scrabble Data"):
            training_data.append(parse_scrabble_line(line, dawg))

    elapsed_time = time.time() - start_time
    print(f"Data loaded in {elapsed_time:.4f} seconds")

    return pd.DataFrame(training_data)
