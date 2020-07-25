from client.entities.ShowPlayersMessage import ShowPlayersMessage
from commands.player.PlayerCommand import PlayerCommand


class ListPlayersCommand(PlayerCommand):
    @classmethod
    def subname(cls) -> str: return "list"

    @classmethod
    def description(cls) -> str: return "Show an overview of all players in your raiding group"

    async def execute(self, **kwargs):
        destination = self.message.channel
        raiders = await self.get_raiders()
        players = self.players_resource.list_players(self.discord_guild.id)
        await ShowPlayersMessage(self.client, self.discord_guild, players, raiders).send_to(destination)
