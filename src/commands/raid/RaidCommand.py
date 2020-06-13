from commands.BotCommand import BotCommand


class RaidCommand(BotCommand):
    @classmethod
    def name(cls) -> str: return "raid"
