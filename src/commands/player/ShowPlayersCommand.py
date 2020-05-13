from client.entities.ShowPlayersMessage import ShowPlayersMessage
from commands.player.PlayerCommand import PlayerCommand


class ListPlayersCommand(PlayerCommand):
    def __init__(self):
        argformat = ''
        subname = 'list'
        description = 'Toon een overzicht van alle spelers'
        super(ListPlayersCommand, self).__init__(subname, description, argformat)

    async def execute(self, **kwargs):
        destination = self.message.channel
        await ShowPlayersMessage(self.client, self.players_resource).send_to(destination)
