from dokbot.commands.BotCommand import BotCommand


class CharacterCommand(BotCommand):
    @classmethod
    def name(cls) -> str: return "character"

    @classmethod
    def req_manager_rank(cls) -> bool: return False
