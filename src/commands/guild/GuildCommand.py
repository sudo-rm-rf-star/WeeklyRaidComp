from commands.BotCommand import BotCommand


class GuildCommand(BotCommand):
    @classmethod
    def name(cls) -> str: return "guild"
