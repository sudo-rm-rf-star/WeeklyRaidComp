import discord

from commands.raid.RaidCommand import RaidCommand


class RaidEventRemind(RaidCommand):
    @classmethod
    def sub_name(cls) -> str: return "remind"

    @classmethod
    def argformat(cls) -> str: return "raid_name [raid_datetime]"

    @classmethod
    def description(cls) -> str: return "Sends a reminder to all of the unsigned and tentative players to sign for " \
                                        "the given raid. "

    async def execute(self, raid_name, raid_datetime, **kwargs):
        raid_event = self.get_raid_event(raid_name, raid_datetime)
        unsigned_raiders = await self.get_unsigned_players(raid_event)
        self.respond(f'These players have not signed for {raid_event}: {", ".join(map(str, unsigned_raiders))}')
        for raider in unsigned_raiders:
            try:
                await raider.send(
                    f'{raider.display_name}, this is a friendly reminder to sign for the upcoming raid for {raid_event}. '
                    f'If you have any further questions please notify {self.member}.'
                )
            except discord.Forbidden:
                self.respond(f'Could not send a reminder to {raider}')

        tentative_raiders = await self.get_tentative_players(raid_event)
        self.respond(f'These players are tentative for {raid_event}: {", ".join(map(str, tentative_raiders))}')
        for raider in tentative_raiders:
            try:
                await raider.send(f'Once you know whether or not you can join please change your signup status, thanks!')
            except discord.Forbidden:
                self.respond(f'Could not send a reminder to {raider}')
