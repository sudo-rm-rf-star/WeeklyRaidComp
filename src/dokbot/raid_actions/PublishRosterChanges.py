import asyncio
from typing import List

import discord

from dokbot.RaidContext import RaidContext
from logic.Character import Character
from logic.enums.RosterStatus import RosterStatus
from logic.enums.SignupStatus import SignupStatus
from dokbot.utils.DiscordUtils import get_role

VERBS = {
    RosterStatus.Accept: 'accepted',
    RosterStatus.Extra: 'benched',
    RosterStatus.Decline: 'declined'
}


def publish_roster_changes(ctx: RaidContext, characters: List[Character]):
    for character in characters:
        roster_choice = character.get_roster_status()
        if roster_choice != RosterStatus.Undecided:
            asyncio.create_task(_handle_roster_choice(ctx=ctx, character=character))


async def _handle_roster_choice(ctx: RaidContext, character: Character) -> None:
    verb = VERBS[character.get_roster_status()]
    formatted_msg = f'{character.name}, you were {verb} for {ctx.raid_event} organized by {ctx.raid_team}.'
    team_count = max([char.get_team_index() for char in ctx.raid_event.get_signed_characters()])
    if team_count > 0 and character.get_roster_status() == RosterStatus.Accept:
        formatted_msg += f' You are part of group {character.get_team_index() + 1}.'
    member = await ctx.guild.fetch_member(int(character.discord_id))
    await member.send(content=formatted_msg)