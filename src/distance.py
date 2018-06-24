# Ricky Galliani
# Grit and Grind
# 6/23/18

from utils import get_logger
from load import load_game

from collections import defaultdict

import math
import sys

def feet_to_miles(num_feet):
    '''
    Converts feet to miles.
    '''
    return num_feet / 5280.0

def compute_player_distances(game, logger):
    '''
    Computes the distance traveled by each player for a given game.
    '''
    player_dists = {}  # Store player name -> (cur_x, cur_y, event_dist, total_dist)
    cur_event = 1
    logger.info('Computing distances traveled by each player...')
    for i, moment in enumerate(game.moments):
        player_locs = moment.locations.players
        same_event = moment.event == cur_event
        for player_id in player_locs:
            player_name = id_to_name[player_id]
            cur_x, cur_y = player_locs[player_id].x, player_locs[player_id].y
            if player_name in player_dists:
                prev_x, prev_y, prev_event_dist, prev_total_dist = player_dists[player_name]
                if same_event:
                    d_dist = math.sqrt((cur_x - prev_x) ** 2 + (cur_y - prev_y) ** 2)
                    total_dist = prev_total_dist
                    event_dist = prev_event_dist + d_dist
                else:
                    total_dist = prev_total_dist + prev_event_dist
                    event_dist = 0.0
                    cur_event = moment.event
                player_dists[player_name] = (cur_x, cur_y, event_dist, total_dist)
            else:
                total_dist = 0.0
                event_dist = 0.0
                player_dists[player_name] = (cur_x, cur_y, event_dist, total_dist)
    return player_dists

if __name__ == '__main__':

    # Read in command-line arguments
    game_path = sys.argv[1]  # Path to the raw SportVU data
    
    # Set up a logger
    logger = get_logger("distance-{}".format(game_path))
    
    # Read in the SportVU data
    game = load_game(game_path, logger)

    # Create a map between player_id and name
    id_to_name = dict(
        [(x.player_id, ' '.join([x.first_name, x.last_name])) for x in game.home_team.players ] +
        [(x.player_id, ' '.join([x.first_name, x.last_name])) for x in game.away_team.players ]
    )

    # Compute distance travelled by each player
    player_distances = compute_player_distances(game, logger)

    print([(k, round(feet_to_miles(v[3]), 3)) for (k, v) in player_distances.items()])

