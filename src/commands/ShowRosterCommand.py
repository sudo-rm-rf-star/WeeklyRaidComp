from src.commands.RosterCommand import RosterCommand


class ShowRosterCommand(RosterCommand):
    def __init__(self):
        argformat = "raid_name [raid_datetime]"
        subname = 'show'
        description = 'Stuur een persoonlijk bericht met de raid compositie'
        super(RosterCommand, self).__init__('roster', subname, description, argformat)

    async def run(self, client, message, **kwargs):
        return self._run(client, message, **kwargs)

    async def _run(self, client, message, raid_name, raid_datetime):
        rosters = self.load_rosters(raid_name, raid_datetime)
        embed = self.get_roster_embed(client, rosters)
        await message.author.send(embed=embed)
