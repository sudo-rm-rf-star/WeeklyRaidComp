from src.commands.BotCommand import BotCommand
from src.commands.BotCommands import BOT_COMMANDS
from src.client.GuildClient import GuildClient
from discord import Message


class HelpCommand(BotCommand):
    def __init__(self, name: str):
        subname = 'help'
        description = f"Toon alle commando's die beginnen met `{name}` en hoe ze op te roepen. Merk op, alle argumenten omringd door [ ] zijn optioneel en kunnen weggelaten worden."
        super(HelpCommand, self).__init__(name, subname, description)

    async def run(self, client: GuildClient, message: Message, **kwargs) -> None:
        available_commands = list(BOT_COMMANDS[self.name].values()) + [self]
        text_channel = message.channel
        content = '\n'.join([command._help_str() for command in available_commands])
        await text_channel.send(content)
