from commands.raidgroup.RaidGroupCommand import RaidGroupCommand
from exceptions.InternalBotException import InternalBotException
from exceptions.InvalidArgumentException import InvalidArgumentException


class SelectRaidGroup(RaidGroupCommand):
    def __init__(self):
        argformat = "raidgroup"
        subname = 'select'
        description = 'Kies welke raid groep je wilt beheren'
        super(SelectRaidGroup, self).__init__(subname=subname, description=description, argformat=argformat)

    async def execute(self, raidgroup: str, **kwargs) -> None:
        raidgroups = [raid_group for raid_group in self.guild.raid_groups if raid_group.name == raidgroup]
        if len(raidgroups) == 0:
            raise InvalidArgumentException('The given raid group does not exist.')
        if len(raidgroups) > 1:
            raise InternalBotException(f"Multiple raid groups exist with the same name {raidgroup}")
        raidgroup = raidgroups[0]
        self.players_resource.select_raidgroup(self.member, raidgroup)
        self.respond(f"You will now manage raids for the {raidgroup.name} group")
