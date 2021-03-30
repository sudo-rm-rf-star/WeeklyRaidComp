import discord

from dokbot.utils.DiscordUtils import get_member, get_member_by_id
from dokbot.RaidTeamContext import RaidTeamContext
from dokbot.interactions.TextInteractionMessage import TextInteractionMessage
from exceptions.InvalidInputException import InvalidInputException
from persistence.PlayersResource import PlayersResource
from utils.Constants import BOT_NAME
from logic.Player import Player


class FindPlayerInteraction(TextInteractionMessage):
    def __init__(self, ctx: RaidTeamContext, *args, **kwargs):
        content = f"Please fill in the name of the player, either his Discord name or character name."
        super().__init__(ctx, content=content, *args, **kwargs)

    async def get_response(self) -> Player:
        player_name = await super(FindPlayerInteraction, self).get_response()
        player = PlayersResource().get_player_by_name(name=player_name, raid_team=self.ctx.raid_team)
        if not player:
            member = await get_member(self.ctx.guild, player_name)
            if member:
                player = PlayersResource().get_player_by_id(member.id)
        if not player:
            raise InvalidInputException(f'Could not find a player with the name {player_name}. Try again:')
        return player
