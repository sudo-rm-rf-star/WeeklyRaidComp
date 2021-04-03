from logic.enums.Class import Class
from logic.Character import Character
from logic.Player import Player
from dokbot.interactions.TextInteractionMessage import TextInteractionMessage
from dokbot.interactions.EmojiInteractionMessage import EmojiInteractionMessage
from dokbot.entities.GuildMember import GuildMember
from persistence.PlayersResource import PlayersResource
import asyncio
import discord
import re
from exceptions.InvalidInputException import InvalidInputException
from typing import Tuple, Optional

TRIES = 3


async def register(client: discord.Client, guild: discord.Guild, member: GuildMember,
                   allow_multiple_chars: bool = False) -> Tuple[Player, Optional[Character]]:
    players_resource = PlayersResource()
    player = players_resource.get_player_by_id(member.id)
    if player and len(player.characters) >= 1 and not allow_multiple_chars:
        member.send(f'You have already signed up: {player}')
        return player, None

    char_name = await GetNameMesage.interact(member=member, player=player, client=client, guild=guild)

    klass = await GetClassMessage.interact(member=member, client=client, guild=guild)
    spec = await GetSpecMessage.interact(member=member, client=client, guild=guild, klass=klass)
    role = klass.get_role(spec)
    if player is None:
        player = Player(discord_id=member.id, characters=[], selected_char=char_name)
    character = Character(discord_id=member.id, char_name=char_name, role=role, klass=klass, spec=spec)
    player.characters.append(character)
    players_resource.update_player(player)
    asyncio.create_task(member.send(content=f'You have successfully registered: {character}'))
    return player, character


class GetNameMesage(TextInteractionMessage):
    def __init__(self, client: discord.Client, guild: discord.Guild, player: Player, *args, **kwargs):
        self.player = player
        content = "Please respond with your character name"
        super(GetNameMesage, self).__init__(client, guild, content, *args, **kwargs)

    async def get_response(self) -> str:
        name = (await super(GetNameMesage, self).get_response()).strip().capitalize()
        if re.search(r"\s", name):
            raise InvalidInputException(f'Please use your character name')
        if self.player and name in [char.name for char in self.player.characters]:
            raise InvalidInputException(f"You've already chosen this name")
        return name


class GetClassMessage(EmojiInteractionMessage):
    def __init__(self, client: discord.Client, guild: discord.Guild, *args, **kwargs):
        content = "Please select the class of your character"
        icons = [klass.name.capitalize() for klass in list(Class)]
        super().__init__(client, guild, content=content, emojis=icons, *args, **kwargs)

    async def get_response(self):
        klass = await super(GetClassMessage, self).get_response()
        return Class[klass.upper()]


class GetSpecMessage(EmojiInteractionMessage):
    def __init__(self, client: discord.Client, guild: discord.Guild, klass: Class, *args, **kwargs):
        self.klass = klass
        content = "Please select the spec of your character"
        icons = [f'{spec[0]}_{klass.name.capitalize()}' for spec in klass.specs]
        super().__init__(client, guild, content=content, emojis=icons, *args, **kwargs)

    async def get_response(self):
        spec = await super(GetSpecMessage, self).get_response()
        spec = spec.split('_')[0]
        return spec
