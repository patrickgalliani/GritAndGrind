# Ricky Galliani
# Grit and Grind
# 6/27/18

from utils import get_logger
from load import load_game, load_pbp

import math
import sys


if __name__ == '__main__':

    # Read in command-line arguments
    game_path = sys.argv[1]  # Path to the raw SportVU data
    pbp_path = sys.argv[2]  # Path to the play-by-play data

    # Set up a logger
    logger = get_logger("game-shot-{}".format(game_path))

    # Read in the SportVU data
    game = load_game(game_path, logger)

    # Read in the play-by-play data
    pbp = load_pbp(pbp_path, logger)

    # Create a map between player_id and name
    id_to_player = dict(
        [(x.player_id, x) for x in game.home_team.players] +
        [(x.player_id, x) for x in game.away_team.players]
    )
