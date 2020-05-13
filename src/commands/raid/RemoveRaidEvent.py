from commands.raid.RaidCommand import RaidCommand
from client.DiscordClient import DiscordClient
from utils.DateOptionalTime import DateOptionalTime

import discord
from utils.Constants import OFFICER_RANK


class CreateRaidCommand(RaidCommand):
    def __init__(self):
        argformat = "raid_name raid_date raid_time"
        subname = 'remove'
        description = 'Verwijder een event voor een raid'
        super(CreateRaidCommand, self).__init__(subname, description, argformat, OFFICER_RANK)

    async def execute(self, raid_name: str, raid_datetime: DateOptionalTime, **kwargs):
        self.respond(await self.events_resource.remove_raid(raid_name, raid_datetime))
