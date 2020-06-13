from commands.BotCommand import BotCommand


class RaidGroupCommand(BotCommand):
    @classmethod
    def name(cls) -> str: return "raidgroup"
