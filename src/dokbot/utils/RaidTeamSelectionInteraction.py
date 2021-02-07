from logic.Player import Player
from logic.RaidTeam import RaidTeam
from exceptions.InvalidInputException import InvalidInputException
from dokbot.utils.OptionInteraction import OptionInteraction
from dokbot.utils.RaidTeamHelper import create_raidteam
from dokbot.entities.GuildMember import GuildMember
from persistence.RaidTeamsResource import RaidTeamsResource
from persistence.PlayersResource import PlayersResource
import discord

ADD_RAID_TEAM = 'Add a new raid team.'


class RaidTeamSelectionInteraction(OptionInteraction):
    def __init__(self, client: discord.Client, guild: discord.Guild, member: GuildMember, *args, **kwargs):
        self.guild = guild
        self.member = member
        self.raid_team_resource = RaidTeamsResource()

        self.raid_teams = self.raid_team_resource.list_raidteams(self.guild.id)
        options = [raid_team.name for raid_team in self.raid_teams] + [ADD_RAID_TEAM]
        message = "Please choose the raidteam you want to manage or add a new one (Enter a number):"
        super().__init__(client=client, guild=guild, options=options, content=message, *args, **kwargs)

    async def get_response(self) -> RaidTeam:
        response = await super(RaidTeamSelectionInteraction, self).get_response()

        players_resource = PlayersResource()
        player = players_resource.get_player_by_id(self.member.discord_id)
        if not player:
            player = Player(discord_id=self.member.discord_id, characters=[])

        if response == ADD_RAID_TEAM:
            return await create_raidteam(self.client, self.discord_guild, self.member, first=len(self.raid_teams) == 0)
        for raid_team in self.raid_teams:
            if response == raid_team.name:
                player.selected_team_name = raid_team.name
                player.selected_guild_id = self.discord_guild.id
                players_resource.update_player(player)
                return raid_team
        raise InvalidInputException(f'Please choose on of: {self.options}')
