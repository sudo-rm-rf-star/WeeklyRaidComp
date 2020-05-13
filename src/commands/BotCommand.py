from exceptions.InternalBotException import InternalBotException
from commands.utils.ArgParser import ArgParser
from commands.utils.CommandUtils import check_authority
from client.DiscordClient import DiscordClient
from client.entities.GuildMember import GuildMember
from utils.Constants import DATETIMESEC_FORMAT, LOGS_CHANNEL
from discord import Message, TextChannel, RawReactionActionEvent
from datetime import datetime
from typing import Optional
from client.PlayersResource import PlayersResource
from client.RaidEventsResource import RaidEventsResource
import asyncio


class BotCommand:
    def __init__(self, name: str, subname: str, description: str, argformat: str = '', required_rank: str = None, example_args: str = None):
        self.name = name
        self.subname = subname
        self.argformat = argformat
        self.argparser = ArgParser(argformat)
        self.description = description
        self.required_rank = required_rank
        if not example_args:
            self.example_args = self.argparser.get_example_args()
        else:
            self.example_args = example_args
        self.client: Optional[DiscordClient] = None
        self.players_resource: Optional[PlayersResource] = None
        self.events_resource: Optional[RaidEventsResource] = None
        self.message: Optional[Message] = None
        self.raw_reaction: Optional[RawReactionActionEvent] = None
        self.member: Optional[GuildMember] = None

    async def execute(self, **kwargs):
        raise InternalBotException("Please specify logic for this command. Do not call this method directly.")

    async def call(self, client: DiscordClient, players_resource, events_resource, message: Optional[Message],
                   raw_reaction: Optional[RawReactionActionEvent], argv: str):
        self.client = client
        self.players_resource = players_resource
        self.events_resource = events_resource
        self.message = message
        self.raw_reaction = raw_reaction
        self.member = client.get_member_by_id(message.author.id) if message else client.get_member_by_id(raw_reaction.user_id)

        if argv.strip() == 'help':
            await self.show_help(message.channel)
        else:
            check_authority(self.member, self.required_rank)
            kwargs = self.argparser.parse(argv)
            await self.execute(**kwargs)

    def respond(self, content: str):
        log_message = f'{datetime.now().strftime(DATETIMESEC_FORMAT)} - {self.member} - {self.message.content if self.message else self.raw_reaction.emoji} - {content}'
        asyncio.create_task(self.client.get_channel(LOGS_CHANNEL).send(content=log_message))
        asyncio.create_task(self.member.send(content=content))

    async def show_help(self, channel: TextChannel) -> None:
        await channel.send(content=self._help_str())

    def _help_str(self) -> str:
        prefix = f'!{self.name} {self.subname}'
        command_with_arg_names = f'\n`{prefix} {self.argformat}`'
        command_with_arg_examples = f'\n`{prefix} {self.example_args}`' if self.example_args else ''
        return f'**{self.description}**{command_with_arg_names}{command_with_arg_examples}'

