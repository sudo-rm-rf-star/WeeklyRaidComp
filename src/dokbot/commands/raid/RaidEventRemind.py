import discord

from dokbot.commands.raidteam.RaidTeamCog import RaidTeamCog
from logic.enums.SignupStatus import SignupStatus


class RaidEventRemind(RaidTeamCog):
    @classmethod
    def sub_name(cls) -> str: return "remind"

    @classmethod
    def argformat(cls) -> str: return "raid_name [raid_datetime]"

    @classmethod
    def description(cls) -> str: return "Sends a reminder to all of the unsigned and tentative players to sign for " \
                                        "the given raid. "

    async def execute(self, raid_name, raid_datetime, **kwargs):
        raid_event = await self.get_raid_event(raid_name, raid_datetime)
        unsigned_raiders = raid_event.get_characters(signup_choice=SignupStatus.UNDECIDED)
        self.respond(
            f'These players have not signed for {raid_event}: '
            f'{", ".join(map(lambda raider: raider.name, unsigned_raiders))}'
        )
        for raider in unsigned_raiders:
            try:
                user = await self.client.fetch_user(raider.discord_id)
                await user.send(
                    f'{raider.name}, this is a friendly reminder to sign for the upcoming raid for {raid_event}. '
                    f'If you have any further questions please notify {self.member}.'
                )
            except discord.Forbidden:
                self.respond(f'Could not send a reminder to {raider}')

        tentative_raiders = raid_event.get_characters(signup_choice=SignupStatus.TENTATIVE)
        self.respond(f'These players are tentative for {raid_event}: {", ".join(map(str, tentative_raiders))}')
        for raider in tentative_raiders:
            try:
                user = await self.client.fetch_user(raider.discord_id)
                await user.send(f'Once you know whether or not you can join please change your signup status, thanks!')
            except discord.Forbidden:
                self.respond(f'Could not send a reminder to {raider}')
