from client.entities.ShowPlayerActivityMessage import ShowPlayerActivityMessage
from commands.player.PlayerCommand import PlayerCommand
from utils.AttendanceReader import update_raid_presence


class ListPlayerActivityCommand(PlayerCommand):
    @classmethod
    def subname(cls) -> str: return "list-activity"

    @classmethod
    def description(cls) -> str: return "Show an overview of the activity of all players in your raiding group"

    async def execute(self, **kwargs):
        update_raid_presence(self.discord_guild.id, self.get_raidgroup().group_id, self.guild.wl_guild_id, self.events_resource, self.players_resource)
        destination = self.message.channel
        raiders = await self.get_raiders()
        players = self.players_resource.list_players(self.discord_guild.id)
        await ShowPlayerActivityMessage(self.client, self.discord_guild, players, raiders).send_to(destination)
