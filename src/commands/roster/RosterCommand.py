from commands.BotCommand import BotCommand
from logic.Character import Character
from logic.RaidEvent import RaidEvent
from logic.enums.RosterStatus import RosterStatus
from typing import List, Optional
from utils.DiscordUtils import get_member_by_id
import asyncio


class RosterCommand(BotCommand):
    @classmethod
    def name(cls) -> str: return "roster"

    async def publish_roster_changes(self, characters: List[Character], raid_event: RaidEvent) -> None:
        for player in characters:
            verbs = {
                RosterStatus.ACCEPT: 'accepted',
                RosterStatus.EXTRA: 'benched',
                RosterStatus.DECLINE: 'declined'
            }
            roster_choice = player.roster_status
            if roster_choice != RosterStatus.UNDECIDED:
                verb = verbs[roster_choice]
                formatted_msg = f'{player.name}, you were {verb} for {raid_event.get_name()} on {raid_event.get_date()} ({raid_event.get_weekday()})'
                member = await get_member_by_id(self.discord_guild, player.discord_id)
                asyncio.create_task(member.send(content=formatted_msg))



