from src.commands.BotCommand import BotCommand
from src.commands.BotCommands import BOT_COMMANDS


class HelpCommand(BotCommand):
    def __init__(self, name):
        subname = 'help'
        description = f"Toon alle commando's die beginnen met `{name}` en hoe ze op te roepen. Merk op alle argumenten omringd door [ ] zijn optioneel en kunnen weggelaten worden."
        super(HelpCommand, self).__init__(name, subname, description)

    async def run(self, client, message, **kwargs):
        available_commands = list(BOT_COMMANDS[self.name].values()) + [self]
        text_channel = message.channel
        content = '\n'.join([format_help_command(command) for command in available_commands])
        await text_channel.send(content)


def format_help_command(command):
    prefix = f'!{command.name} {command.subname}'
    example = '' if not command.argformat else f'`{prefix} {command.argparser.get_example_args()}`\n'
    return f'**{command.description}**\n`{prefix} {command.argformat}`\n{example}'
