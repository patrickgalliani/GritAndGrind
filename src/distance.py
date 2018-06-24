# Ricky Galliani
# Grit and Grind
# 6/23/18

from utils import get_logger
from load import load_game

from collections import defaultdict

import math
import sys

if __name__ == '__main__':

    # Read in command-line arguments
    game_path = sys.argv[1]  # Path to the raw SportVU data
    
    # Set up a logger
    logger = get_logger("distance-{}".format(game_path))
    
    # Read in the SportVU data
    game = load_game(game_path, logger)

    # Compute distance travelled by each player
    player_dists = {}  # Store (cur_x, cur_y, cur_dist)
    for i, moment in enumerate(game.moments):
        player_locs = moment.locations.players
        for player_id in player_locs:
            cur_x, cur_y = player_locs[player_id].x, player_locs[player_id].y
            if player_id in player_dists:
                prev_x, prev_y, prev_dist = player_dists[player_id]
                d_dist = math.sqrt((cur_x - prev_x) ** 2 + (cur_y - prev_y) ** 2)
                cur_dist = prev_dist +  d_dist
            else:
                cur_dist = 0.0 
            player_dists[player_id] = (cur_x, cur_y, cur_dist)
    print([(k, v[2]) for (k, v) in player_dists.items()])



