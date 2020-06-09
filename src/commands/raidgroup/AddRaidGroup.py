from commands.raidgroup.RaidGroupCommand import RaidGroupCommand
from commands.utils.RaidGroupHelper import create_raidgroup


class AddRaidGroup(RaidGroupCommand):
    def __init__(self):
        subname = 'add'
        description = 'Voeg een nieuwe raid group toe'
        super(AddRaidGroup, self).__init__(subname=subname, description=description)

    async def execute(self, **kwargs) -> None:
        guild = self.guilds_resource.get_guild(self.discord_guild.id)
        raidgroup = create_raidgroup(self.client, self.discord_guild, self.member)
        guild.raid_groups.append(raidgroup)
        self.guilds_resource.update_guild(guild)
        self.respond(f"Your raid group {raidgroup.name} has succesfully been created!")



