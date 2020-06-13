from exceptions.MissingImplementationException import MissingImplementationException
from exceptions.NoRaidGroupSpecifiedException import NoRaidGroupSpecifiedException
from commands.utils.ArgParser import ArgParser
from commands.utils.CommandUtils import check_authority
from client.entities.GuildMember import GuildMember
from utils.Constants import DATETIMESEC_FORMAT
from utils.DiscordUtils import get_member_by_id, get_members_for_role, get_channel
from discord import Message, TextChannel, RawReactionActionEvent
from datetime import datetime
from typing import Optional, List
from client.PlayersResource import PlayersResource
from client.RaidEventsResource import RaidEventsResource
from client.GuildsResource import GuildsResource
from logic.Player import Player
from logic.Guild import Guild
from logic.RaidGroup import RaidGroup
import asyncio
import discord


class BotCommand:
    @classmethod
    def name(cls) -> str: raise MissingImplementationException(cls)

    @classmethod
    def subname(cls) -> str: raise MissingImplementationException(cls)

    @classmethod
    def description(cls) -> str: raise MissingImplementationException(cls)

    @classmethod
    def argformat(cls) -> str: return ""

    @classmethod
    def example_args(cls) -> Optional[str]: return None

    @classmethod
    def req_manager_rank(cls) -> bool: return True

    def __init__(self, client: discord.Client, players_resource: PlayersResource, events_resource: RaidEventsResource, guilds_resource: GuildsResource,
                 message: Optional[Message], raw_reaction: Optional[RawReactionActionEvent], argv: str, member: GuildMember, player: Player,
                 discord_guild: discord.Guild, guild: Guild, raidgroup: RaidGroup, logs_channel: TextChannel):
        assert message or raw_reaction
        self.kwargs = ArgParser(BotCommand.argformat()).parse(argv)
        self.client: discord.Client = client
        self.players_resource: PlayersResource = players_resource
        self.events_resource = events_resource
        self.guilds_resource = guilds_resource
        self.message = message
        self.raw_reaction = raw_reaction
        self.member = member
        self.player = player
        self.discord_guild = discord_guild
        self.guild = guild
        self._raidgroup = raidgroup
        self._logs_channel = logs_channel

    async def execute(self, **kwargs):
        raise MissingImplementationException()

    async def call(self):
        required_rank = self.guild.manager_rank if self.req_manager_rank else None
        check_authority(self.member, required_rank)
        await self.execute(**self.kwargs)

    def respond(self, content: str):
        action = self.message.content if self.message else self.raw_reaction.emoji
        log_message = f'{datetime.now().strftime(DATETIMESEC_FORMAT)} - {self.member.display_name} - {action} - {content} '
        asyncio.create_task(self._logs_channel.send(content=log_message))
        asyncio.create_task(self.member.send(content=content))

    async def show_help(self, channel: TextChannel) -> None:
        await channel.send(content=self.get_help())

    @staticmethod
    def get_help() -> str:
        prefix = f'!{BotCommand.name()} {BotCommand.subname()}'
        command_with_arg_names = f'\n`{prefix} {BotCommand.argformat()}`'
        command_with_arg_examples = f'\n`{prefix} {BotCommand.example_args()}`' if BotCommand.example_args() else ''
        return f'**{BotCommand.description()}**{command_with_arg_names}{command_with_arg_examples}'

    def get_raidgroup(self):
        if not self._raidgroup:
            raise NoRaidGroupSpecifiedException(self.discord_guild)
        return self._raidgroup

    def get_raiders(self) -> List[GuildMember]:
        return get_members_for_role(self.discord_guild, self.get_raidgroup().raider_rank)

    def get_events_channel(self):
        return get_channel(self.discord_guild, self.get_raidgroup().events_channel)
