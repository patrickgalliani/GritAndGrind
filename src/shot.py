# Ricky Galliani
# Grit and Grind
# 6/27/18


class Shot:

    def __init__(self, game_id, player_id, event_id, result):
        self.game_id = game_id
        self.player_id = player_id
        self.event_id = event_id
        self.result = result # 1 for a make, 2 for a miss
