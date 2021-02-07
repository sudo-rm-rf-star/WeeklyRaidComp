from dokbot.commands.BotCommand import BotCommand


class PlayerCommand(BotCommand):
    @classmethod
    def name(cls) -> str: return "player"
