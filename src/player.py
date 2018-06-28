# Ricky Galliani
# Grit and Grind
# 6/23/18


class Player:

    def __init__(self,
                 first_name,
                 last_name,
                 team_name,
                 jersey,
                 player_id,
                 position):
        self.first_name = first_name
        self.last_name = last_name
        self.team_name = team_name
        self.jersey = jersey
        self.player_id = player_id
        self.position = position

    def __hash__(self):
        return hash(' '.join([self.first_name, self.last_name]))
