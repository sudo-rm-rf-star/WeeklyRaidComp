from commands.BotCommand import BotCommand
from logic.Player import Player
from logic.RaidEvent import RaidEvent
from logic.enums.RosterStatus import RosterStatus
from typing import List
import asyncio


class RosterCommand(BotCommand):
    def __init__(self, subname: str, description: str, argformat: str, required_rank: str):
        super(RosterCommand, self).__init__('roster', subname, description, argformat, required_rank)

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
                asyncio.create_task(self.client.get_member_by_id(player.discord_id).send(content=formatted_msg))



