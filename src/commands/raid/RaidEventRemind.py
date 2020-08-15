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
        self.respond(f'Sending reminder to {len(raiders)} raiders for {raid_event}')
        for raider in raiders:
            try:
                await raider.send(
                    f'{raider.display_name}, this is a friendly reminder to sign for the upcoming raid for {raid_event}. '
                    f'If you have any further questions please notify {self.member}.'
                )
            except discord.Forbidden:
                self.respond(f'Could not send a reminder to {raider}')

