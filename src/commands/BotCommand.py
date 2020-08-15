from exceptions.MissingImplementationException import MissingImplementationException
from exceptions.NoRaidGroupSpecifiedException import NoRaidGroupSpecifiedException
from commands.utils.CommandUtils import check_authority
from client.entities.GuildMember import GuildMember
from utils.Constants import DATETIMESEC_FORMAT
from utils.DiscordUtils import get_members_for_role, get_channel
from discord import Message, TextChannel, RawReactionActionEvent
from datetime import datetime
from typing import Optional, List, Dict, Any
from client.PlayersResource import PlayersResource
from client.RaidEventsResource import RaidEventsResource
from client.GuildsResource import GuildsResource
from client.MessagesResource import MessagesResource
from logic.Player import Player
from logic.Guild import Guild
from logic.RaidGroup import RaidGroup
from logic.MessageRef import MessageRef
import asyncio
import discord
from commands.utils.ArgParser import ArgParser

# Safety measure to avoid infinite loops
MAX_ITERS = 1000000


class BotCommand:
    @classmethod
    def name(cls) -> str:
        raise MissingImplementationException(cls)

    @classmethod
    def subname(cls) -> str:
        raise MissingImplementationException(cls)

    @classmethod
    def description(cls) -> str:
        raise MissingImplementationException(cls)

    @classmethod
    def argformat(cls) -> str:
        return ""

    @classmethod
    def example_args(cls) -> Optional[str]:
        return None

    @classmethod
    def req_manager_rank(cls) -> bool:
        return True

    def __init__(self, client: discord.Client, players_resource: PlayersResource, events_resource: RaidEventsResource, guilds_resource: GuildsResource,
                 messages_resource: MessagesResource, message: Optional[Message], message_ref: Optional[MessageRef],
                 raw_reaction: discord.RawReactionActionEvent,
                 member: GuildMember, player: Player, discord_guild: discord.Guild, guild: Guild, raidgroup: RaidGroup, channel: Optional[TextChannel],
                 logs_channel: TextChannel):
        self.client: discord.Client = client
        self.players_resource: PlayersResource = players_resource
        self.events_resource = events_resource
        self.guilds_resource = guilds_resource
        self.messages_resource = messages_resource
        self.message = message
        self.message_ref = message_ref
        self.raw_reaction = raw_reaction
        self.member = member
        self.player = player
        self.discord_guild = discord_guild
        self.guild = guild
        self.channel = channel
        self._raidgroup = raidgroup
        self._logs_channel = logs_channel

    async def execute(self, **kwargs):
        raise MissingImplementationException(BotCommand)

    async def call(self, **kwargs):
        required_rank = self.guild.manager_rank if self.req_manager_rank() else None
        check_authority(self.member, required_rank)
        await self.execute(**kwargs)

    def respond(self, content: str):
        action = self.message.content if self.message else self.raw_reaction.emoji
        log_message = f'{datetime.now().strftime(DATETIMESEC_FORMAT)} - {self.member.display_name} - {action} - {content} '
        if self._logs_channel:
            asyncio.create_task(self._logs_channel.send(content=log_message))
        asyncio.create_task(self.member.send(content=content))

    def post(self, content: str):
        asyncio.create_task(self.channel.send(content=content))

    async def show_help(self, channel: TextChannel) -> None:
        await channel.send(content=self.get_help())

    @classmethod
    def get_help(cls) -> str:
        prefix = f'!{cls.name()} {cls.subname()}'
        command_with_arg_names = f'\n`{prefix} {cls.argformat()}`'
        example_args = cls.example_args() if cls.example_args() else ArgParser(cls.argformat()).get_example_args()
        command_with_arg_examples = f'\n`{prefix} {example_args}`'
        return f'**{cls.description()}**{command_with_arg_names}{command_with_arg_examples}'

    def get_raidgroup(self) -> RaidGroup:
        if not self._raidgroup:
            raise NoRaidGroupSpecifiedException(self.guild)
        return self._raidgroup

    def get_raider_rank(self) -> str:
        return self.get_raidgroup().raider_rank

    async def get_raiders(self) -> List[GuildMember]:
        member_iterator = self.discord_guild.fetch_members(limit=None)
        raiders = []
        i = 0
        more_items = True
        while i < MAX_ITERS and more_items:
            try:
                member = await member_iterator.next()
                if member and any(role.name == self.get_raider_rank() for role in member.roles):
                    raiders.append(GuildMember(member, self.discord_guild.id))
            except discord.NoMoreItems:
                more_items = False
            i += 1
        return raiders

    async def get_events_channel(self):
        return await get_channel(self.discord_guild, self.get_raidgroup().events_channel)
