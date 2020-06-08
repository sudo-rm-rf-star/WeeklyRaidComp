from commands.raidgroup.RaidGroupCommand import RaidGroupCommand
from utils.Constants import RAIDER_RANK
from exceptions.InternalBotException import InternalBotException
from exceptions.InvalidArgumentException import InvalidArgumentException


class SelectRaidGroup(RaidGroupCommand):
    def __init__(self):
        argformat = "raidgroup"
        subname = 'select'
        description = 'Kies welke raid groep je wilt beheren'
        super(SelectRaidGroup, self).__init__(subname, description, argformat, required_rank=RAIDER_RANK)

    async def execute(self, raidgroup: str, **kwargs) -> None:
        guild = self.get_guild()
        raidgroups = [raid_group for raid_group in guild.raid_groups if raid_group.name == raidgroup]
        if len(raidgroups) == 0:
            raise InvalidArgumentException('The given raid group does not exist.')
        if len(raidgroups) > 1:
            raise InternalBotException(f"Multiple raid groups exist with the same name {raidgroup}")
        raidgroup = raidgroups[0]
        self.players_resource.select_raidgroup(self.member, raidgroup)
        self.respond(f"You will now manage raids for the {raidgroup.name} group")
