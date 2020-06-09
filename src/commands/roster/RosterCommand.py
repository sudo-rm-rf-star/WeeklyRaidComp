from commands.BotCommand import BotCommand
from logic.Player import Player
from logic.RaidEvent import RaidEvent
from logic.enums.RosterStatus import RosterStatus
from typing import List, Optional
from utils.DiscordUtils import get_member_by_id
import asyncio


class RosterCommand(BotCommand):
    def __init__(self, *, subname: str, description: str, argformat: Optional[str] = None):
        super(RosterCommand, self).__init__(name='roster', subname=subname, description=description, argformat=argformat)

    def publish_roster_changes(self, players: List[Player], raid_event: RaidEvent) -> None:
        for player in players:
            verbs = {
                RosterStatus.ACCEPT: 'accepted',
                RosterStatus.EXTRA: 'benched',
                RosterStatus.DECLINE: 'declined'
            }
            roster_choice = player.roster_status
            if roster_choice != RosterStatus.UNDECIDED:
                verb = verbs[roster_choice]
                formatted_msg = f'{player.name}, you were {verb} for {raid_event.get_name()} on {raid_event.get_date()} ({raid_event.get_weekday()})'
                asyncio.create_task(get_member_by_id(self.discord_guild, player.discord_id).send(content=formatted_msg))



