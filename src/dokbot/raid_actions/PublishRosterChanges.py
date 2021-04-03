import asyncio
from typing import List

import discord

from dokbot.RaidContext import RaidContext
from logic.Character import Character
from logic.enums.RosterStatus import RosterStatus
from logic.enums.SignupStatus import SignupStatus
from dokbot.utils.DiscordUtils import get_role

VERBS = {
    RosterStatus.ACCEPT: 'accepted',
    RosterStatus.EXTRA: 'benched',
    RosterStatus.DECLINE: 'declined'
}


def publish_roster_changes(ctx: RaidContext, characters: List[Character]):
    for character in characters:
        roster_choice = character.get_roster_status()
        if roster_choice != RosterStatus.UNDECIDED:
            asyncio.create_task(_handle_roster_choice(ctx=ctx, character=character))


async def _handle_roster_choice(ctx: RaidContext, character: Character) -> None:
    verb = VERBS[character.get_roster_status()]
    formatted_msg = f'{character.name}, you were {verb} for {ctx.raid_event.get_name()} on {ctx.raid_event.get_date()} ({ctx.raid_event.get_weekday()})'
    member = await ctx.guild.fetch_member(character.discord_id)
    await member.send(content=formatted_msg)
    await _set_roster_status(ctx=ctx, character=character, member=member)


async def _set_roster_status(ctx: RaidContext, character: Character, member: discord.Member):
    roster_status = character.get_roster_status()
    signup_status = character.get_signup_status()
    roster_role = await get_role(ctx.guild, "Roster")
    if roster_status in [RosterStatus.ACCEPT, RosterStatus.EXTRA] and signup_status != SignupStatus.DECLINE:
        await member.add_roles(roster_role)
    else:
        await member.remove_roles(roster_role)
