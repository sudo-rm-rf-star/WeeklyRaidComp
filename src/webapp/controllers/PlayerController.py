from .AbstractController import AbstractController


class PlayerController(AbstractController):
    def __init__(self, *args, **kwargs):
        super(PlayerController, self).__init__(*args, **kwargs)

    def index(self):
        players = self.players_table.list_players(self.guild)
        return self.view('players', players=players)

    def show(self, discord_id):
        player = self.players_table.get_player_by_id(discord_id)
        return self.view('player', player=player)
