from commands.BotCommand import BotCommand


class RaidInfoCommand(BotCommand):
    @classmethod
    def name(cls) -> str: return "raidinfo"

    @classmethod
    def visible(cls) -> bool: return False
