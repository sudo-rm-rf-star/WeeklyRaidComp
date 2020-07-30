from client.entities.ShowSelectedPlayersMessage import ShowSelectedPlayersMessage
from commands.player.PlayerCommand import PlayerCommand


class ListSelectedPlayersCommand(PlayerCommand):
    @classmethod
    def subname(cls) -> str: return "list-selected"

    @classmethod
    def description(cls) -> str: return "Show an overview of all players and their selected character in your raiding group"

    async def execute(self, **kwargs):
        destination = self.message.channel
        raiders = await self.get_raiders()
        players = self.players_resource.list_players(self.discord_guild.id)
        await ShowSelectedPlayersMessage(self.client, self.discord_guild, players, raiders).send_to(destination)
