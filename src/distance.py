# Ricky Galliani
# Grit and Grind
# 6/23/18

from utils import get_logger
from load import load_game

import math
import sys


def feet_to_miles(num_feet):
    '''
    Converts feet to miles.
    '''
    return num_feet / 5280.0


def compute_player_distances(game, id_to_player, logger):
    '''
    Computes the distance traveled by each player for a given game.
    '''
    dists = {}  # player -> (cur_x, cur_y, event_dist, total_dist)
    cur_event = 1
    logger.info('Computing distances traveled by each player...')
    for i, moment in enumerate(game.moments):
        player_locs = moment.locations.players
        same_event = moment.event == cur_event
        for player_id in player_locs:
            player = id_to_player[player_id]
            cur_x, cur_y = player_locs[player_id].x, player_locs[player_id].y
            if player in dists:
                prev_x, prev_y, prev_event_dist, prev_total_dist = dists[player]
                if same_event:
                    diff_x = abs(cur_x - prev_x)
                    diff_y = abs(cur_y - prev_y)
                    d_dist = math.sqrt(diff_x ** 2 + diff_y ** 2)
                    # Do not add distance from unrealistic, noisy data
                    if diff_x >= 0.5 or diff_y >= 0.5 or d_dist >= 0.6:
                        event_dist = 0.0
                    else:
                        event_dist = prev_event_dist + d_dist
                    total_dist = prev_total_dist
                else:
                    total_dist = prev_total_dist + prev_event_dist
                    event_dist = 0.0
                    cur_event = moment.event
            else:
                total_dist = 0.0
                event_dist = 0.0
            dists[player] = (cur_x, cur_y, event_dist, total_dist)
    return dists


def log_distances(player_distances, logger):
    '''
    Logs the distance traveled by each player to the console.
    '''
    output = []
    for player, distance_array in player_distances.items():
        team_name = '"{}"'.format(str(player.team_name))
        player_name = '"{}"'.format(
            ' '.join([str(player.first_name), str(player.last_name)])
        )
        dist_miles = str(round(feet_to_miles(distance_array[3]), 3))
        output.append([team_name, dist_miles, player_name])
    output.sort(reverse=True)
    logger.info(
        "\n\nteam_name,dist_miles,player_name\n{}\n\n".format(
            "\n".join(','.join(x) for x in output)
        )
    )


if __name__ == '__main__':

    # Read in command-line arguments
    game_path = sys.argv[1]  # Path to the raw SportVU data

    # Set up a logger
    logger = get_logger("distance-{}".format(game_path))

    # Read in the SportVU data
    game = load_game(game_path, logger)

    # Create a map between player_id and name
    id_to_player = dict(
        [(x.player_id, x) for x in game.home_team.players] +
        [(x.player_id, x) for x in game.away_team.players]
    )

    # Compute distance travelled by each player
    player_distances = compute_player_distances(game, id_to_player, logger)

    # Log player distances to console
    log_distances(player_distances, logger)

