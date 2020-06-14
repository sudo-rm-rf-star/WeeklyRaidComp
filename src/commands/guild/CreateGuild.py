from commands.guild.GuildCommand import GuildCommand
from commands.utils.GuildHelper import create_guild


class CreateGuild(GuildCommand):
    @classmethod
    def subname(cls) -> str: return "create"

    @classmethod
    def description(cls) -> str: return "Make a new guild"

    async def execute(self, **kwargs) -> None:
        create_guild(guilds_resource=self.guilds_resource, client=self.client, discord_guild=self.discord_guild, member=self.member)



