# Ricky Galliani
# Grit and Grind
# 6/23/18

from game import Game
from moment import Moment
from player import Player
from team import Team

import json
import pandas as pd


def load_game(game_path, logger):
    '''
    Loads a game from a specified JSON path and returns a Game object.
    '''
    with open(game_path, 'r') as g:
        logger.info(
            "Reading in the raw SportVU data from {}...".format(game_path)
        )
        d = json.loads(g.read())

        logger.info("Reading in the player and team data...")
        visitor_team_name = d['events'][0]['visitor']['name']
        visitor_players = list(set([
            Player(
                x['firstname'],
                x['lastname'],
                visitor_team_name,
                x['jersey'],
                x['playerid'],
                x['position']
            ) for y in d['events']
            for x in y['visitor']['players']
        ]))
        home_team_name = d['events'][0]['home']['name']
        home_players = list(set([
            Player(
                x['firstname'],
                x['lastname'],
                home_team_name,
                x['jersey'],
                x['playerid'],
                x['position']
            ) for y in d['events']
            for x in y['home']['players']
        ]))
        visitor_team = Team(
            visitor_team_name,
            d['events'][0]['visitor']['teamid'],
            d['events'][0]['visitor']['abbreviation'],
            visitor_players
        )
        home_team = Team(
            home_team_name,
            d['events'][0]['home']['teamid'],
            d['events'][0]['home']['abbreviation'],
            home_players
        )
        logger.info("Reading in the location data...")
        moments = []
        for event in d['events']:
            for moment_array in event['moments']:
                moments.append(Moment(moment_array, event['eventId']))
        return Game(
            d['gamedate'],
            d['gameid'],
            home_team,
            visitor_team,
            moments
        )

from location import Location
from shot import Shot

def load_pbp(pbp_path, logger):
    '''
    Loads play-by-play data from the given path. 
    '''
    pbp = pd.read_csv(pbp_path)[[
        "GAME_ID",
        "PLAYER1_ID",
        "EVENTNUM",
        "EVENTMSGTYPE",
    ]]
    makes = [Shot(x[0], x[1], x[2], 1) for x in pbp.loc[pbp["EVENTMSGTYPE"] == 1][
        ["GAME_ID", "PLAYER1_ID", "EVENTNUM", "EVENTMSGTYPE"]
    ].values]
    misses = [Shot(x[0], x[1], x[2], 2) for x in pbp.loc[pbp["EVENTMSGTYPE"] == 2][
        ["GAME_ID", "PLAYER1_ID", "EVENTNUM", "EVENTMSGTYPE"]
    ].values]
    return (makes, misses)

from utils import get_logger
from collections import defaultdict

import math

logger = get_logger('load_pbp_test')

makes, misses = load_pbp('../play-by-play/0021500002.csv', logger)

BALL_SHOOTER_THRESHOLD = 0.25

def get_distance(loc1, loc2):
    '''
    Returns the distance between loc1 and loc2.
    '''
    return math.sqrt((loc1.x - loc2.x) ** 2 + (loc1.y - loc2.y) ** 2)

def get_shot_moments_for_game(game, shots):
    '''
    Takes a Game object as input and a list of shots ([event id, player id])
    and returns a list of Location objects representing the location of 
    the player when he took the shot.
    '''
    events = dict([(shot.event_id, shot.player_id) for shot in shots])
    locations = defaultdict(list)
    for moment in game.moments:
        # If current moment is part of a shot event
        if moment.event_id in events:
            shooter = events[moment.event_id]
            if shooter not in moment.locations.players:
                print("Player ID {} not in event {} location data...".format(
                    shooter, 
                    moment.event_id
                ))
                continue
            loc = moment.locations.players[shooter]
            ball_loc = moment.locations.ball 
            secs_left = moment.seconds_left_quarter
            locations[moment.event_id].append((secs_left, loc, ball_loc))
    shot_locations = {}
    for event in locations:
        # Find location of shooter last time he was less than threshold feet
        # away from the ball
        event_locs = locations[event]
        for (secs_left, loc, ball_loc) in event_locs[::-1]:
            if loc is None or ball_loc is None:
                continue
            dist = get_distance(loc, ball_loc)
            if get_distance(loc, ball_loc) <= BALL_SHOOTER_THRESHOLD:
                shot_locations[event] = loc  
            if event == 384:
                print("{}: dist = {}, {}, {} -> {}, {}, {}".format(secs_left, dist, loc.x, loc.y, ball_loc.x, ball_loc.y, ball_loc.z))
    return shot_locations
            

game = load_game('../games/0021500002.json', logger)
make_moments = get_shot_moments_for_game(game, makes)
event_id = make_moments.keys()[0]
print("event_id = {}".format(event_id))
loc = make_moments[event_id]
print("x, y = {}, {}".format(loc.x, loc.y))
