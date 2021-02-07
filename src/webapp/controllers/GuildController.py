from .AbstractController import AbstractController


class GuildController(AbstractController):
    def __init__(self, *args, **kwargs):
        super(GuildController, self).__init__(*args, **kwargs)

    def view_directory(self):
        return 'guild'

    def index(self):
        guilds = [self.guilds_table.get_raidteam(guild_id) for guild_id in self.player.guild_ids]
        guilds = [guild for guild in guilds if guild is not None]
        return self.view('index', guilds=guilds)

    def show(self, guild_id):
        guild = self.guilds_table.get_raidteam(guild_id)
        return self.view('show', guild=guild)
