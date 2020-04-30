import src.client.Logger as Log
from src.exceptions.InternalBotException import InternalBotException
from src.commands.utils.ArgParser import ArgParser
from src.common.Constants import DATETIMESEC_FORMAT, LOGS_CHANNEL
from src.client.GuildClient import GuildClient
from src.commands.utils.CommandUtils import check_authority
from src.logic.Players import Players
from src.logic.RaidEvents import RaidEvents
from discord import Message, User, TextChannel
from datetime import datetime
from typing import Optional


class BotCommand:
    def __init__(self, name: str, subname: str, description: str, argformat: str = '', required_rank: str = None, allow_trough_approval: bool = False, example_args: str = None):
        self.name = name
        self.subname = subname
        self.argformat = argformat
        self.argparser = ArgParser(argformat)
        self.description = description
        self.required_rank = required_rank
        self.allow_trough_approval = allow_trough_approval
        if not example_args:
            self.example_args = self.argparser.get_example_args()
        else:
            self.example_args = example_args

    async def run(self, client: GuildClient, message: Message, **kwargs) -> Optional[str]:
        raise InternalBotException("Please specify logic for this command. Do not call this method directly.")

    async def call(self, client: GuildClient, message: Message, argv: str) -> None:
        needs_approval = not self.check_authority(client, message.author)
        if needs_approval:
            raise InternalBotException(f"Sorry {message.author}, this code path still needs to be implemented...")

        if argv.strip() == 'help':
            await self.show_help(message.channel)
        else:
            kwargs = self.argparser.parse(argv)
            response = await self.run(client, message, **kwargs)
            if response:
                log_message = f'{datetime.now().strftime(DATETIMESEC_FORMAT)} - {message.author} - {message.content} - {response}'
                Log.info(log_message)
                await message.author.send(content=response)
                await client.get_channel(LOGS_CHANNEL).send(content=log_message)
        # TODO: this can be done waaaaaay smarter
        RaidEvents().store()
        Players().store()

    def check_authority(self, server: GuildClient, author: User) -> bool:
        check_authority(server, author, self.required_rank)
        return True

    async def show_help(self, channel: TextChannel) -> None:
        await channel.send(content=self._help_str())

    def _help_str(self) -> str:
        prefix = f'!{self.name} {self.subname}'
        command_with_arg_names = f'\n`{prefix} {self.argformat}`'
        command_with_arg_examples = f'\n`{prefix} {self.example_args}`' if self.example_args else ''
        return f'**{self.description}**{command_with_arg_names}{command_with_arg_examples}'

