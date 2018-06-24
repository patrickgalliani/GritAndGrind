# Ricky Galliani
# Grit and Grind
# 6/23/18

class Location:

    def __init__(self, location_array):
        self.x = location_array[2]
        self.y = location_array[3]
        self.z = location_array[4]


class MomentLocations:
    def __init__(self, location_matrix):
        self.ball = Location(location_matrix[0])
        self.players = dict([
            (location_matrix[x][1], Location(location_matrix[x])) 
            for x in range(1, 11)
        ]) 
