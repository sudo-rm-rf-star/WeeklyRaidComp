from commands.raidgroup.RaidGroupCommand import RaidGroupCommand


class AddRaidGroup(RaidGroupCommand):
    def __init__(self):
        argformat = ""
        subname = 'add'
        description = 'Voeg een nieuwe raid group toe'
        super(AddRaidGroup, self).__init__(subname, description, argformat, required_rank=RAIDER_RANK)

    async def execute(self, **kwargs) -> None:
        await register(self.client, self.players_resource, self.member, allow_multiple=True)
