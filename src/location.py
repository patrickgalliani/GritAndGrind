# Ricky Galliani
# Grit and Grind
# 6/23/18

class Location:

    def __init__(self, location_array):
        self.team_id = location_array[0]
        self.object_id = location_array[1]
        self.x = location_array[2]
        self.y = location_array[3]
        self.z = location_array[4]


class LocationMatrix:

    def __init__(self, location_array):
        self.ball_location = Location(location_array[0])
        self.player_locations = [Location(location_array[x]) for x in range(1, 12)] 
