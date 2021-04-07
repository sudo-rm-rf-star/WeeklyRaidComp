from logic.enums.Class import Class
from logic.Character import Character
from logic.Player import Player
from dokbot.interactions.TextInteractionMessage import TextInteractionMessage
from dokbot.interactions.EmojiInteractionMessage import EmojiInteractionMessage
from dokbot.interactions.ChooseSpecMessage import ChooseSpecMessage
from dokbot.DokBotContext import DokBotContext
from persistence.PlayersResource import PlayersResource
import re
from exceptions.InvalidInputException import InvalidInputException
from typing import Tuple, Optional, List

TRIES = 3


async def register(ctx: DokBotContext) -> Tuple[Player, Optional[Character]]:
    players_resource = PlayersResource()
    player_id = ctx.author.id
    player = players_resource.get_player_by_id(player_id)
    char_name = await GetNameMessage.interact_with_author(ctx=ctx, characters=player.characters if player else [])
    klass = await GetClassMessage.interact_with_author(ctx=ctx)
    spec = await ChooseSpecMessage.interact_with_author(ctx=ctx, klass=klass)
    if player is None:
        player = Player(discord_id=player_id, characters=[], selected_char=char_name)
    character = Character(discord_id=player_id, char_name=char_name, klass=klass, spec=spec)
    player.add_character(character)
    players_resource.update_player(player)
    await ctx.author.send(content=f'You have successfully registered: {await ctx.bot.display_character(character)}')
    return player, character


class GetNameMessage(TextInteractionMessage):
    def __init__(self, ctx: DokBotContext, characters: List[Character]):
        content = "Please respond with your character name"
        self.character_names = [char.name for char in characters]
        super(GetNameMessage, self).__init__(ctx=ctx, content=content)

    async def get_response(self) -> str:
        name = (await super(GetNameMessage, self).get_response()).strip().capitalize()
        if re.search(r"\s", name) or re.search(r"\d", name):
            raise InvalidInputException('Please use your character name')
        if name in self.character_names:
            raise InvalidInputException(f"You already have a character named {name}")
        return name


class GetClassMessage(EmojiInteractionMessage):
    def __init__(self, ctx: DokBotContext):
        content = "Please select the class of your character"
        icons = [klass.name.capitalize() for klass in list(Class)]
        super().__init__(ctx=ctx, content=content, reactions=icons)

    async def get_response(self):
        klass = await super(GetClassMessage, self).get_response()
        return Class[klass.upper()]

