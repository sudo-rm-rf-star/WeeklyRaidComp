from exceptions.InternalBotException import InternalBotException
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
    def __init__(self, *, name: str, subname: str, description: str, argformat: Optional[str] = None, example_args: Optional[str] = None,
                 req_manager_rank: Optional[bool] = True):
        self.name = name
        self.subname = subname
        self.argformat = argformat
        self.argparser = ArgParser(argformat)
        self.description = description
        self.req_manager_rank = req_manager_rank
        if not example_args:
            self.example_args = self.argparser.get_example_args()
        else:
            self.example_args = example_args
        self.client: Optional[discord.Client] = None
        self.discord_guild: Optional[discord.Guild] = None
        self.players_resource: Optional[PlayersResource] = None
        self.events_resource: Optional[RaidEventsResource] = None
        self.guilds_resource: Optional[GuildsResource] = None
        self.message: Optional[Message] = None
        self.raw_reaction: Optional[RawReactionActionEvent] = None
        self.member: Optional[GuildMember] = None
        self.player: Optional[Player] = None
        self.guild: Optional[Guild] = None
        self._raidgroup: Optional[RaidGroup] = None
        self._logs_channel: Optional[TextChannel] = None

    async def execute(self, **kwargs):
        raise InternalBotException("Please specify logic for this command. Do not call this method directly.")

    async def call(self, client: discord.Client, players_resource, events_resource, guilds_resource, message: Optional[Message],
                   raw_reaction: Optional[RawReactionActionEvent], argv: str):
        self.client = client
        self.players_resource = players_resource
        self.events_resource = events_resource
        self.guilds_resource = guilds_resource
        self.message = message
        self.raw_reaction = raw_reaction
        if raw_reaction:
            self.discord_guild = await client.fetch_guild(self.player.guild_id)
            self.member = get_member_by_id(self.discord_guild, raw_reaction.user_id)
        else:
            self.discord_guild = message.guild
            self.member = get_member_by_id(self.discord_guild, message.author.id)
        self.player = self.players_resource.get_character_by_id(self.member.id)
        self.guild = self.guilds_resource.get_guild(self.member.guild_id)
        self._raidgroup = GuildsResource.get_group(self.guild, self.player)
        self._logs_channel = get_channel(self.discord_guild, self.guild.logs_channel)

        if argv.strip() == 'help':
            await self.show_help(message.channel)
        else:
            required_rank = self.guild.manager_rank if self.req_manager_rank else None
            check_authority(self.member, required_rank)
            kwargs = self.argparser.parse(argv)
            await self.execute(**kwargs)

    def respond(self, content: str):
        action = self.message.content if self.message else self.raw_reaction.emoji
        log_message = f'{datetime.now().strftime(DATETIMESEC_FORMAT)} - {self.member.display_name} - {action} - {content} '
        asyncio.create_task(self._logs_channel.send(content=log_message))
        asyncio.create_task(self.member.send(content=content))

    async def show_help(self, channel: TextChannel) -> None:
        await channel.send(content=self._help_str())

    def _help_str(self) -> str:
        prefix = f'!{self.name} {self.subname}'
        command_with_arg_names = f'\n`{prefix} {self.argformat}`'
        command_with_arg_examples = f'\n`{prefix} {self.example_args}`' if self.example_args else ''
        return f'**{self.description}**{command_with_arg_names}{command_with_arg_examples}'

    def get_raidgroup(self):
        if not self._raidgroup:
            raise NoRaidGroupSpecifiedException(self.discord_guild)
        return self._raidgroup

    def get_raiders(self) -> List[GuildMember]:
        return get_members_for_role(self.discord_guild, self.get_raidgroup().raider_rank)

    def get_events_channel(self):
        return get_channel(self.discord_guild, self.get_raidgroup().events_channel)
