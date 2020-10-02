from commands.raidgroup.RaidGroupCommand import RaidGroupCommand
from commands.utils.RaidGroupHelper import create_raidgroup


class AddRaidGroup(RaidGroupCommand):
    @classmethod
    def subname(cls) -> str: return "add"

    @classmethod
    def description(cls) -> str: return "Add a new raid group"

    async def execute(self, **kwargs) -> None:
        guild = self.guilds_resource.get_guild(self.discord_guild.id)
        raidgroup = await create_raidgroup(self.client, self.discord_guild, self.member, wl_guild_id=guild.wl_guild_id)
        guild.raid_groups.append(raidgroup)
        self.guilds_resource.update_guild(guild)
        self.respond(f"Your raid group {raidgroup.name} has succesfully been created!")



