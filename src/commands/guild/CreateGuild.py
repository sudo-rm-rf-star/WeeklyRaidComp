from commands.guild.GuildCommand import TeamCommand


class CreateTeam(TeamCommand):
    def __init__(self, subname: str, description: str, argformat: str, required_rank: str = None, example_args: str = None):
        argformat = ""
        subname = 'add'
        description = 'Voeg een character toe'
        super(AddCharacter, self).__init__(subname, description, argformat, required_rank=RAIDER_RANK)

    async def execute(self, **kwargs) -> None:
        await register(self.client, self.players_resource, self.member, allow_multiple=True)
