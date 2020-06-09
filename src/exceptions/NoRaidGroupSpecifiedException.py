from exceptions.BotException import BotException
from logic.Guild import Guild


class NoRaidGroupSpecifiedException(BotException):
    def __init__(self, guild: Guild):
        group_names = ', '.join([group.name for group in guild.raid_groups])
        message = f"There are multiple raid groups available for {guild.name}, please select one of the following groups: {group_names}. " \
                  f"For more information, use the `!raidgroup help` command."
        super(NoRaidGroupSpecifiedException, self).__init__(message)
