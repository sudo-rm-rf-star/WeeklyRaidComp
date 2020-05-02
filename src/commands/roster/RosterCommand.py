from src.client.GuildClient import GuildClient
from src.commands.BotCommand import BotCommand
from src.logic.RaidEvent import RaidEvent
from src.logic.Players import Players
from src.logic.enums.RosterStatus import RosterStatus
import asyncio


class RosterCommand(BotCommand):
    def __init__(self, subname: str, description: str, argformat: str, required_rank: str, allow_trough_approval: bool = False):
        super(RosterCommand, self).__init__('roster', subname, description, argformat, required_rank, allow_trough_approval)

    def publish_roster_changes(self, client: GuildClient, raid_event: RaidEvent) -> None:
        for player_name, roster_choice in raid_event.rosters.check_roster_updates():
            player = Players().get(player_name)
            verbs = {
                RosterStatus.ACCEPT: 'accepted',
                RosterStatus.EXTRA: 'benched',
                RosterStatus.DECLINE: 'declined'
            }
            if roster_choice != RosterStatus.UNDECIDED:
                verb = verbs[roster_choice]
                formatted_msg = f'{player.name}, you were {verb} for {raid_event.get_name()} on {raid_event.get_date()} ({raid_event.get_weekday()})'
                asyncio.create_task(client.get_member_by_id(player.discord_id).send(content=formatted_msg))



