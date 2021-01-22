from commands.raidgroup.RaidGroupCommand import RaidGroupCommand
from exceptions.InternalBotException import InternalBotException
from exceptions.InvalidArgumentException import InvalidArgumentException


class SelectRaidGroup(RaidGroupCommand):
    @classmethod
    def sub_name(cls) -> str: return "select"

    @classmethod
    def argformat(cls) -> str: return "raidgroup"

    @classmethod
    def description(cls) -> str: return "Select the raid group you'd like to manage"

    async def execute(self, raidgroup: str, **kwargs) -> None:
        raidgroups = [raid_group for raid_group in self.guild.raid_groups if raid_group.name == raidgroup]
        if len(raidgroups) == 0:
            raise InvalidArgumentException('The given raid group does not exist.')
        if len(raidgroups) > 1:
            raise InternalBotException(f"Multiple raid groups exist with the same name {raidgroup}")
        raidgroup = raidgroups[0]
        self.players_resource.select_raidgroup(self.member, raidgroup)
        self.respond(f"You will now manage raids for the {raidgroup.name} group")
