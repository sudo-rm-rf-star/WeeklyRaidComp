from logic.Player import Player
from logic.RaidTeam import RaidTeam
from exceptions.InvalidInputException import InvalidInputException
from dokbot.interactions.OptionInteraction import OptionInteraction
from dokbot.raidteam_actions.CreateRaidTeam import create_raidteam
from persistence.RaidTeamsResource import RaidTeamsResource
from persistence.PlayersResource import PlayersResource
from dokbot.DokBotContext import DokBotContext
from dokbot.player_actions.Register import register

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
            player, _ = await register(self.ctx)

        if response == ADD_RAID_TEAM:
            return await create_raidteam(ctx=self.ctx, first=len(self.raid_teams) == 0)
        for raid_team in self.raid_teams:
            if response == raid_team.name:
                if player.get_selected_raid_team_name(guild_id=self.ctx.guild_id) != raid_team.name:
                    player.set_selected_raid_team_name(guild_id=self.ctx.guild_id, team_name=raid_team.name)
                    players_resource.update_player(player)
                return raid_team
        raise InvalidInputException(f'Please choose on of: {self.options}')
