# Ricky Galliani
# Grit and Grind
# 6/23/18

from location import LocationMatrix

from datetime import datetime

class Moment:

    def __init__(self, moment_array):
        self.quarter = moment_array[0]
        self.time_string = (
            datetime.fromtimestamp(moment_array[1] / 1000.0).strftime('%Y-%m-%d %H:%M:%S.%f')
        )
        self.seconds_left_quarter = moment_array[2]
        self.seconds_left_shot_clock = moment_array[3]
        self.location_matrix = moment_array_array[4]
