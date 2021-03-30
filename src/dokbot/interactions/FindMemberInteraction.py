import discord

from dokbot.utils.DiscordUtils import get_member, get_member_by_id
from dokbot.RaidTeamContext import RaidTeamContext
from dokbot.interactions.TextInteractionMessage import TextInteractionMessage
from exceptions.InvalidInputException import InvalidInputException
from persistence.PlayersResource import PlayersResource
from utils.Constants import BOT_NAME


class FindMemberInteraction(TextInteractionMessage):
    def __init__(self, ctx: RaidTeamContext, *args, **kwargs):
        content = f"Please fill in the name of the player in the Discord server, " \
                  f"or his character name if he has signed up in {BOT_NAME} before."
        super().__init__(ctx, content=content, *args, **kwargs)

    async def get_response(self) -> discord.Member:
        player_name = await super(FindMemberInteraction, self).get_response()
        member = await get_member(self.ctx.guild, player_name)
        if member is None:
            player = PlayersResource().get_player_by_name(name=player_name, raid_team=self.ctx.raid_team)
            if player:
                member = await get_member_by_id(self.ctx.guild, player.discord_id)
        if member is None:
            raise InvalidInputException(f'Could not find a member with the name {player_name} on this Discord. Try again.')
        return member
