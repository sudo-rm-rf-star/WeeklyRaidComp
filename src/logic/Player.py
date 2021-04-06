from logic.Character import Character
from typing import Optional, List, Dict
from datetime import datetime


class Player:
    def __init__(self, *, discord_id: int, characters: List[Character] = None, selected_char: Optional[str] = None,
                 created_at: Optional[float] = None, selected_teams: Optional[Dict[str, str]] = None):
        self.discord_id = discord_id
        self.selected_char = selected_char
        self.characters = characters if characters else []
        self.created_at = created_at if created_at else datetime.now().timestamp()
        self.selected_teams = selected_teams if selected_teams else {}

    def get_selected_char(self) -> Character:
        return self.get_char(self.selected_char)

    def get_char(self, name):
        for character in self.characters:
            if character.name == name:
                return character
        return self.characters[0]  # Recovery from unexpected situation

    def set_selected_char(self, character_name: str):
        self.selected_char = character_name

    def get_selected_raid_team_name(self, guild_id: int):
        return self.selected_teams.get(str(guild_id))

    def set_selected_raid_team_name(self, guild_id: int, team_name: str):
        self.selected_teams[str(guild_id)] = team_name

    def __eq__(self, other) -> bool:
        return self.discord_id == other.discord_id

    def __hash__(self):
        return hash(self.discord_id)

    def __str__(self):
        return str(self.characters)
