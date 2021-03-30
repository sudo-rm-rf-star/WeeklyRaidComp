from dokbot.commands.CogMixin import CogMixin
from logic.Character import Character
from logic.RaidEvent import RaidEvent
from logic.enums.RosterStatus import RosterStatus
from typing import List
from dokbot.utils.DiscordUtils import get_member_by_id, set_roster_status
import asyncio
import discord

VERBS = {
    RosterStatus.ACCEPT: 'accepted',
    RosterStatus.EXTRA: 'benched',
    RosterStatus.DECLINE: 'declined'
}


class RosterCommand(CogMixin):
    @classmethod
    def name(cls) -> str:
        return "roster"

    def publish_roster_changes(self, characters: List[Character], raid_event: RaidEvent) -> None:
        for character in characters:
            roster_choice = character.get_roster_status()
            if roster_choice != RosterStatus.UNDECIDED:
                asyncio.create_task(_handle_roster_choice(self.discord_guild, raid_event, character))


async def _handle_roster_choice(discord_guild: discord.Guild, raid_event: RaidEvent, character: Character) -> None:
    verb = VERBS[character.get_roster_status()]
    formatted_msg = f'{character.name}, you were {verb} for {raid_event.get_name()} on {raid_event.get_date()} ({raid_event.get_weekday()})'
    member = await get_member_by_id(discord_guild, character.discord_id)
    await member.send(content=formatted_msg)
    await set_roster_status(discord_guild, member, character)
