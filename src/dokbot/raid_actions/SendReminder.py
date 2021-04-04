from typing import List

from dokbot.RaidContext import RaidContext
from logic.Character import Character
from logic.enums.SignupStatus import SignupStatus


async def send_reminder(ctx: RaidContext):
    unsigned_raiders = ctx.raid_event.get_characters(signup_choice=SignupStatus.Unknown)
    tentative_raiders = ctx.raid_event.get_characters(signup_choice=SignupStatus.Tentative)
    await ctx.reply(f'These players have not signed for {ctx.raid_event}: {_to_names(unsigned_raiders)}')
    await ctx.reply(f'These players are tentative for {ctx.raid_event}: {_to_names(tentative_raiders)}')
    msg = f'This is a friendly reminder to sign for the upcoming raid for {ctx.raid_event}.'
    await ctx.send_to_raiders(unsigned_raiders, msg)
    msg = f'Once you know whether or not you can join {ctx.raid_event}, please update your status by signing again.'
    await ctx.send_to_raiders(tentative_raiders, msg)


def _to_names(raiders: List[Character]):
    return ", ".join(map(lambda raider: raider.name, raiders))
