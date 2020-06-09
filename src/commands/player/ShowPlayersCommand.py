from client.entities.ShowPlayersMessage import ShowPlayersMessage
from commands.player.PlayerCommand import PlayerCommand


class ListPlayersCommand(PlayerCommand):
    def __init__(self):
        subname = 'list'
        description = 'Toon een overzicht van alle spelers in je raid groep'
        super(ListPlayersCommand, self).__init__(subname=subname, description=description)

    async def execute(self, **kwargs):
        destination = self.message.channel
        await ShowPlayersMessage(self.client, self.discord_guild, self.players_resource, self.get_raiders()).send_to(destination)
