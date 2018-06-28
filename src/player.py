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

    def __eq__(self, other):
            return (
                self.first_name == other.first_name and
                self.last_name == other.last_name and
                self.team_name == other.team_name and
                self.jersey == other.jersey and
                self.player_id == other.player_id and
                self.position == other.position
            )

    def __hash__(self):
        return hash(' '.join([self.first_name, self.last_name]))
