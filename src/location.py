# Ricky Galliani
# Grit and Grind
# 6/23/18


class Location:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


def contains_ball_location(location_matrix):
    '''
    Returns True if the given location matrix includes the location of the
    ball.
    '''
    return (
        location_matrix[0][0] == -1 and
        location_matrix[0][1] == -1
    )


def get_player_location_indexes(contains_ball_location, location_matrix):
    '''
    Returns the start and end indexes of the player location data in
    the given location matrix.
    '''
    if contains_ball_location:
        return (1, len(location_matrix))
    else:
        return (0, len(location_matrix))


class MomentLocations:
    def __init__(self, location_matrix):
        contains_ball_loc = contains_ball_location(location_matrix)
        player_start, player_end = get_player_location_indexes(
            contains_ball_loc,
            location_matrix
        )
        if contains_ball_loc:
            self.ball = Location(
                location_matrix[0][2], 
                location_matrix[0][3],
                location_matrix[0][4]
        )
        else:
            self.ball = None
        self.players = dict([
            (location_matrix[x][1],
             Location(location_matrix[x][2],
                      location_matrix[x][3],
                      location_matrix[x][4])
             )
            for x in range(player_start, player_end)
        ])
