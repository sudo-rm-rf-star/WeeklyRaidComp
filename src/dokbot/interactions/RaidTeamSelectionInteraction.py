from logic.Player import Player
from logic.RaidTeam import RaidTeam
from exceptions.InvalidInputException import InvalidInputException
from dokbot.interactions.OptionInteraction import OptionInteraction
from dokbot.actions.CreateRaidTeam import create_raidteam
from persistence.RaidTeamsResource import RaidTeamsResource
from persistence.PlayersResource import PlayersResource
from dokbot.DokBotContext import DokBotContext

ADD_RAID_TEAM = 'Add a new raid team.'


class RaidTeamSelectionInteraction(OptionInteraction):
    def __init__(self, ctx: DokBotContext, *args, **kwargs):
        self.raid_team_resource = RaidTeamsResource()
        self.raid_teams = self.raid_team_resource.list_raidteams(ctx.guild_id)
        options = [raid_team.name for raid_team in self.raid_teams] + [ADD_RAID_TEAM]
        message = "Please choose the raidteam you want to manage or add a new one?"
        super().__init__(ctx=ctx, options=options, content=message, *args, **kwargs)

    async def get_response(self) -> RaidTeam:
        response = await super(RaidTeamSelectionInteraction, self).get_response()

        players_resource = PlayersResource()
        player = players_resource.get_player_by_id(self.ctx.author.id)
        if not player:
            player = Player(discord_id=self.ctx.author.id, characters=[])

        if response == ADD_RAID_TEAM:
            return await create_raidteam(ctx=self.ctx, first=len(self.raid_teams) == 0)
        for raid_team in self.raid_teams:
            if response == raid_team.name:
                player.selected_team_name = raid_team.name
                player.selected_guild_id = self.ctx.guild.id
                players_resource.update_player(player)
                return raid_team
        raise InvalidInputException(f'Please choose on of: {self.options}')
