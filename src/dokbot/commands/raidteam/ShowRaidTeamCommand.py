from dokbot.entities.ShowRaidTeamMessage import ShowRaidTeamMessage
from dokbot.commands.raidteam.RaidTeamCommand import RaidTeamCommand


class ShowRaidTeamCommand(RaidTeamCommand):
    @classmethod
    def sub_name(cls) -> str: return "show"

    @classmethod
    def description(cls) -> str: return "Show an overview of the characters in this raid team."

    async def execute(self, **kwargs):
        destination = self.message.channel
        raid_team = await self.get_raidteam()
        raiders = await self.get_raiders()
        players = [self.players_resource.get_player_by_id(raider.discord_id) for raider in raiders]
        await ShowRaidTeamMessage.send_message(self.client, self.discord_guild, raid_team=raid_team, players=players, recipient=destination)
