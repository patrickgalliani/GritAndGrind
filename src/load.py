# Ricky Galliani
# Grit and Grind
# 6/23/18

from game import Game
from shot import Shot
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


def load_shots(pbp_path, logger):
    '''
    Loads play-by-play data from the given path and returns Shot objects.
    '''
    logger.info("Reading in the play-by-play data...")
    pbp = pd.read_csv(pbp_path)[[
        "GAME_ID",
        "PLAYER1_ID",
        "EVENTNUM",
        "EVENTMSGTYPE",
    ]]
    logger.info("Extracting shots from the play-by-play data...")
    return [
        Shot(x[0], x[1], x[2], x[3]) for x in 
        pbp[pbp["EVENTMSGTYPE"].isin([1,2])][[
            "GAME_ID",
            "PLAYER1_ID",
            "EVENTNUM",
            "EVENTMSGTYPE"
    ]].values]
