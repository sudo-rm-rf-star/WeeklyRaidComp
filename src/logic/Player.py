from logic.Character import Character
from typing import Set, Optional, List
from exceptions.InternalBotException import InternalBotException


class Player:
    def __init__(self, *, discord_id: int, realm: str, region: str, characters: List[Character], selected_char: str,
                 created_at: float, selected_raidgroup_id: Optional[int] = None, guild_ids: Set[int] = None,
                 selected_guild_id: int = None, autoinvited=False):
        self.discord_id = discord_id
        self.realm = realm
        self.region = region
        self.characters = characters
        self.selected_char = selected_char
        self.created_at = created_at
        self.selected_raidgroup_id = None if not selected_raidgroup_id else selected_raidgroup_id
        self.guild_ids = set(guild_ids) if guild_ids else set()
        self.selected_guild_id = selected_guild_id if selected_guild_id is not None else list(guild_ids)[0] \
            if guild_ids and len(guild_ids) > 0 else None
        self.autoinvited = autoinvited

    def get_selected_char(self) -> Character:
        return self.get_char(self.selected_char)

    def get_char(self, name):
        for character in self.characters:
            if character.name == name:
                return character
        raise InternalBotException("No character was selected")

    def set_selected_char(self, character_name: str):
        self.selected_char = character_name

    def __eq__(self, other) -> bool:
        return self.discord_id == other.discord_id

    def __hash__(self):
        return hash(self.discord_id)

    def __str__(self):
        return str(self.characters)
