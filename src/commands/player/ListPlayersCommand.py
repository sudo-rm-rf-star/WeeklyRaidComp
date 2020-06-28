from client.entities.ShowPlayersMessage import ShowPlayersMessage
from commands.player.PlayerCommand import PlayerCommand


class ListPlayersCommand(PlayerCommand):
    @classmethod
    def subname(cls) -> str: return "list"

    @classmethod
    def description(cls) -> str: return "Show an overview of all players in your raiding group"

    async def execute(self, **kwargs):
        destination = self.message.channel
        await ShowPlayersMessage(self.client, self.discord_guild, self.players_resource, self.get_raiders()).send_to(destination)
