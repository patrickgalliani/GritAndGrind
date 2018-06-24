# Ricky Galliani
# Grit and Grind
# 6/23/18

from game import Game
from moment import Moment
from player import Player
from team import Team

from datetime import datetime

import json

def load_game(game_path, logger):
    '''
    '''
    with open(game_path, 'r') as g:
        logger.info("Reading the raw SportVU data into memory from {}...".format(game_path))
        d = json.loads(g.read())

        logger.info("Reading in the player and team data...")
        visitor_players = [
            Player(
                x['firstname'], 
                x['lastname'],
                x['jersey'],
                x['playerid'],
                x['position']
            ) for x in d['events'][0]['visitor']['players']
        ]
        home_players = [
            Player(
                x['firstname'],
                x['lastname'],
                x['jersey'],
                x['playerid'],
                x['position']
            ) for x in d['events'][0]['home']['players']
        ]
        visitor_team = Team(
            d['events'][0]['visitor']['name'],
            d['events'][0]['visitor']['teamid'],
            d['events'][0]['visitor']['abbreviation'],
            visitor_players
        )
        home_team = Team(
            d['events'][0]['home']['name'],
            d['events'][0]['home']['teamid'],
            d['events'][0]['home']['abbreviation'],
            home_players
        )
        
        logger.info("Reading in the location data...")
        moments = []
        for moment_array in d['events'][0]['moments']:
            moments.append(Moment(moment_array))
        return Game(d['gamedate'], d['gameid'], home_team, visitor_team, moments)         

