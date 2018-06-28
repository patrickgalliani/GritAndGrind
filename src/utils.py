# Ricky Galliani
# Grit and Grind
# 6/23/18

from location import Location

import logging
import math

BALL_SHOOTER_THRESHOLD = 1.5
HOOP1 = Location(5.2, 25.0, 0.0)
HOOP2 = Location(88.8, 25.0, 0.0)


def get_logger(program_name):
    # create logger
    logger = logging.getLogger(program_name)
    logger.setLevel(logging.INFO)
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    # create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)
    return logger


def get_distance(loc1, loc2):
    '''
    Returns the distance between loc1 and loc2.
    '''
    return math.sqrt((loc1.x - loc2.x) ** 2 + (loc1.y - loc2.y) ** 2)
