from commands.raid.RaidCommand import RaidCommand
from utils.DateOptionalTime import DateOptionalTime
import discord


class RaidEventRemind(RaidCommand):
    @classmethod
    def subname(cls) -> str: return "remind"

    @classmethod
    def argformat(cls) -> str: return "raid_name [raid_date][raid_time]"

    @classmethod
    def description(cls) -> str: return "Sends a reminder to all of the unsigned players to sign for the given raid."

    async def execute(self, raid_name, raid_datetime, **kwargs):
        raid_event = self.get_raid_event(raid_name, raid_datetime)
        raiders = await self.get_unsigned_players(raid_event)
        unsigned_raider_ids = {guild_member.id for guild_member in raiders}
        unsigned_raiders = [player.get_selected_char().name for player in
                            self.players_resource.list_players(self.guild)
                            if player.discord_id in unsigned_raider_ids]
        self.respond(f'These players have not signed for {raid_event}: {", ".join(map(str, unsigned_raiders))}')

        for raider in raiders:
            try:
                await raider.send(
                    f'{raider.display_name}, this is a friendly reminder to sign for the upcoming raid for {raid_event}. '
                    f'If you have any further questions please notify {self.member}.'
                )
            except discord.Forbidden:
                self.respond(f'Could not send a reminder to {raider}')

