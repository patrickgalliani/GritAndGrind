# Ricky Galliani
# Grit and Grind
# 6/27/18

from utils import (
    get_logger,
    get_distance,
    HOOP1,
    HOOP2,
    BALL_SHOOTER_THRESHOLD
)
from load import load_game, load_shots
from location import Location
from shot import ShotFeature

from collections import defaultdict

import sys


def get_closest_defender_distance(home_players,
                                  away_players,
                                  shooter,
                                  player_locations):
    '''
    Returns the distance of the closest defender to the shooter.
    '''
    assert(shooter in home_players or shooter in away_players)
    shooter_on_home = shooter in home_players
    away_on = list(set(away_players).intersection(player_locations.keys()))
    home_on = list(set(home_players).intersection(player_locations.keys()))
    if shooter_on_home:
        # Check distance between shooter and all away players and return min
        return min([
                get_distance(player_locations[shooter], player_locations[x]) 
                for x in away_on
            ]
        )
    else:  # Shooter is on the away team
        # Check distance between shooter and all home players and return min
        return min([
                get_distance(player_locations[shooter], player_locations[x])
                for x in home_on
            ]
        )


def get_shot_dist(loc):
    '''
    Returns the distance of the shot from its given release location.
    '''
    return min(get_distance(loc, HOOP1), get_distance(loc, HOOP2))


def get_shot_type(loc):
    '''
    Returns the shot type (2 or 3) given the x and y coordinates of where
    the shot was released.
    '''
    def is_corner_three(x, y):
        '''
        Returns true if x, y are in the corner, behind the 3-point line.
        '''
        return (
            (x < 13.5 and y < 2.92) or
            (x < 13.5 and y > 47.08) or
            (x > 80.5 and y < 2.92) or
            (x > 80.5 and y > 47.08)
        )

    def is_regular_three(x, y):
        '''
        Returns true if x, y are behind the regular (non-corner) 3-point line.
        '''
        loc = Location(x, y, 0.0)
        return (
            min(get_distance(loc, HOOP1), get_distance(loc, HOOP2)) >= 23.75
        )
    x, y = loc.x, loc.y
    if is_corner_three(x, y) or is_regular_three(x, y):
        return 3
    else:
        return 2


def get_shot_features_for_game(game, shots):
    '''
    Takes a Game object as input and a list of shots ([event id, player id])
    and returns a list of ShotFeature objects.
    '''
    # Map shooting event ID -> ID of shooter
    shots_map = dict([(shot.event_id, shot) for shot in shots])
    # Map event ID -> [(player loc, ball_loc, closest_defender_dist), ...]
    locations = defaultdict(list)
    home_players = [x.player_id for x in game.home_team.players]
    away_players = [x.player_id for x in game.away_team.players]
    for moment in game.moments:
        # If current moment is part of a shot event
        if moment.event_id in shots_map:
            shooter = shots_map[moment.event_id].player_id
            if shooter not in moment.locations.players:
                print("Player ID {} not in event {} location data...".format(
                    shooter,
                    moment.event_id
                ))
                continue
            loc = moment.locations.players[shooter]
            ball_loc = moment.locations.ball
            clst_def_dist = get_closest_defender_distance(
                home_players,
                away_players,
                shooter,
                moment.locations.players
            )
            locations[moment.event_id].append((loc, ball_loc, clst_def_dist))
    # Map event ID -> ShotFeature Object
    shot_features = {}
    for event in locations:
        # Find location of shooter last time he was less than threshold feet
        # away from the ball
        event_locs = locations[event]
        for (loc, ball_loc, clst_def_dist) in event_locs[::-1]:
            if loc is None or ball_loc is None:
                continue
            if get_distance(loc, ball_loc) <= BALL_SHOOTER_THRESHOLD:
                shot_dist = get_shot_dist(loc)
                shot_type = get_shot_type(loc)
                shot_features[event] = ShotFeature(
                    shots_map[event].game_id,
                    shots_map[event].player_id,
                    event,
                    shots_map[event].result,
                    loc.x,
                    loc.y,
                    clst_def_dist,
                    shot_dist,
                    shot_type
                )
    return shot_features


if __name__ == '__main__':

    # Read in command-line arguments
    game_path = sys.argv[1]  # Path to the raw SportVU data
    pbp_path = sys.argv[2]  # Path to the play-by-play data

    # Set up a logger
    logger = get_logger("game-shot-{}".format(game_path))

    # Read in the SportVU data
    game = load_game(game_path, logger)

    home_players = [x.player_id for x in game.home_team.players]
    away_players = [x.player_id for x in game.away_team.players]

    # Get Shot objects for each make and miss
    shots = load_shots(pbp_path, logger)

    # Compute locations for all makes and all misses
    shot_features = get_shot_features_for_game(game, shots)

    # Log the shot features to the console
    shot_attributes = ",".join([
        'game_id',
        'player_id',
        'event_id',
        'result',
        'x',
        'y',
        'PTS_TYPE',
        'SHOT_DIST',
        'CLOSE_DEF_DIST'
    ]) + "\n"
    report = shot_attributes
    for event, sf in shot_features.items():
        report += ("{},{},{},{},{},{},{},{},{}\n".format(
                sf.game_id,
                sf.player_id,
                sf.event_id,
                sf.result,
                sf.x,
                sf.y,
                sf.closest_defender_distance,
                sf.shot_distance,
                sf.shot_type
            )
        )
    logger.info("Shots\n\n{}".format(report))
    
    # Write out the data to an output file
    with open(sys.argv[3], 'w') as f:
        f.write(report)
    
    # Create a map between player_id and name
    id_to_player = dict(
        [(x.player_id, x) for x in game.home_team.players] +
        [(x.player_id, x) for x in game.away_team.players]
    )
