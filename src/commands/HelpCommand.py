from commands.BotCommand import BotCommand
from commands.BotCommands import BOT_COMMANDS
from client.DiscordClient import DiscordClient
from discord import Message


class HelpCommand(BotCommand):
    def __init__(self, name: str):
        subname = 'help'
        description = f"Toon alle commando's die beginnen met `{name}` en hoe ze op te roepen. Merk op, alle argumenten omringd door [ ] zijn optioneel en kunnen weggelaten worden."
        super(HelpCommand, self).__init__(name, subname, description)

    async def execute(self, **kwargs) -> None:
        available_commands = list(BOT_COMMANDS[self.name].values()) + [self]
        text_channel = self.message.channel
        content = '\n'.join([command._help_str() for command in available_commands])
        await text_channel.send(content)
