from logic.Player import Player
from logic.RaidTeam import RaidTeam
from exceptions.InvalidInputException import InvalidInputException
from dokbot.interactions.OptionInteraction import OptionInteraction
from dokbot.actions.CreateRaidTeam import create_raidteam
from persistence.RaidEventsResource import RaidEventsResource
from persistence.PlayersResource import PlayersResource
from dokbot.commands.raidteam.RaidTeamContext import RaidTeamContext
from utils.Constants import full_raid_names

ADD_RAID_TEAM = 'Add a new raid team.'


class RaidSelectionInteraction(OptionInteraction):
    def __init__(self, ctx: RaidTeamContext, *args, **kwargs):
        self.raids_resource = RaidEventsResource()
        days = 30
        self.raids = self.raids_resource.list_raids_within_days(guild_id=ctx.guild_id, team_name=ctx.team_name, days=30)
        options = [f'{full_raid_names[raid.name]} at {raid.datetime.strftime("%A, %d. %B %Y %H:%M")}'
                   for raid in self.raids]
        message = f"All raids within {days} days for {ctx.team_name}:"
        super().__init__(ctx=ctx, options=options, content=message, *args, **kwargs)

    async def get_response(self) -> RaidTeam:
        response = await super(RaidSelectionInteraction, self).get_response()

        players_resource = PlayersResource()
        player = players_resource.get_player_by_id(self.ctx.author.id)
        if not player:
            player = Player(discord_id=self.ctx.author.id, characters=[])

        if response == ADD_RAID_TEAM:
            return await create_raidteam(self.ctx.bot, self.ctx.guild, self.ctx.author, first=len(self.raid_teams) == 0)
        for raid_team in self.raid_teams:
            if response == raid_team.name:
                player.selected_team_name = raid_team.name
                player.selected_guild_id = self.ctx.guild.id
                players_resource.update_player(player)
                return raid_team
        raise InvalidInputException(f'Please choose on of: {self.options}')
