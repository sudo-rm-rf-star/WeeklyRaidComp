from exceptions.MissingImplementationException import MissingImplementationException
from exceptions.NoRaidGroupSpecifiedException import NoRaidGroupSpecifiedException
from commands.utils.CommandUtils import check_authority
from client.entities.GuildMember import GuildMember
from utils.Constants import DATETIMESEC_FORMAT
from utils.DiscordUtils import get_channel
from discord import Message, TextChannel
from datetime import datetime
from typing import Optional, List, Any, Type, Set
from client.PlayersResource import PlayersResource
from client.RaidEventsResource import RaidEventsResource
from client.GuildsResource import GuildsResource
from client.MessagesResource import MessagesResource
from logic.RaidEvent import RaidEvent
from logic.Player import Player
from logic.Guild import Guild
from logic.RaidTeam import RaidTeam
from logic.MessageRef import MessageRef
from events.EventQueue import EventQueue
import asyncio
import discord
from commands.utils.ArgParser import ArgParser
from exceptions.InvalidInputException import InvalidInputException
from commands.utils.PlayerInteraction import interact
from commands.utils.PlayerInteraction import InteractionMessage

# Safety measure to avoid infinite loops
MAX_ITERS = 1000000


class BotCommand:
    @classmethod
    def name(cls) -> str:
        raise MissingImplementationException(cls)

    @classmethod
    def sub_name(cls) -> str:
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

    @classmethod
    def visible(cls) -> bool:
        return True

    def __init__(self, client: discord.Client, players_resource: PlayersResource, events_resource: RaidEventsResource,
                 guilds_resource: GuildsResource, messages_resource: MessagesResource, message: Optional[Message],
                 message_ref: Optional[MessageRef], raw_reaction: discord.RawReactionActionEvent, member: GuildMember,
                 player: Player, discord_guild: discord.Guild, guild: Guild, raidgroup: RaidTeam,
                 channel: Optional[TextChannel], logs_channel: TextChannel, event_queue: EventQueue):
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
        self.event_queue = event_queue
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

    @classmethod
    def get_help(cls) -> str:
        prefix = f'!{cls.name()} {cls.sub_name()}'
        command_with_arg_names = f'\n`{prefix} {cls.argformat()}`'
        example_args = cls.example_args() if cls.example_args() else ArgParser(cls.argformat()).get_example_args()
        command_with_arg_examples = f'\n`{prefix} {example_args}`' if example_args else ''
        return f'**{cls.description()}**{command_with_arg_names}{command_with_arg_examples}'

    def get_raidgroup(self) -> RaidTeam:
        group_ids = [group_id for group_id in self.guild.raid_groups]
        if len(group_ids) != 1 and not self._raidgroup:
            raise NoRaidGroupSpecifiedException(self.guild)
        return self._raidgroup if len(group_ids) != 1 else group_ids[0]

    def get_group_id(self) -> int:
        return self.get_raidgroup().id

    def get_raider_rank(self) -> str:
        return self.get_raidgroup().raider_rank

    async def get_raiders(self) -> List[GuildMember]:
        raiders = []
        try:
            async for member in self.discord_guild.fetch_members(limit=None):
                if member and any(role.name == self.get_raider_rank() for role in member.roles):
                    raiders.append(GuildMember(member, self.discord_guild.id))
        except discord.Forbidden as e:
            self.respond(f'There are non-transient problems with Discord permissions...')
            raise e
        return raiders

    async def get_autoinvited_raiders(self) -> Set[GuildMember]:
        raiders = await self.get_raiders()
        for player in self.players_resource.list_players(self.guild):
            if player.autoinvited:
                member = self.discord_guild.get_member(player.discord_id)
                if member:
                    raiders.append(GuildMember(member, self.guild.id))
        return set(raiders)

    async def get_events_channel(self):
        return await get_channel(self.discord_guild, self.get_raidgroup().events_channel)

    def get_raid_event(self, raid_name: str, raid_datetime: datetime) -> RaidEvent:
        raid_event = self.events_resource.get_raid(discord_guild=self.discord_guild, group_id=self.get_group_id(),
                                                   raid_name=raid_name, raid_datetime=raid_datetime)
        if not raid_event:
            raise InvalidInputException(f'Raid event not found for {raid_name}')
        return raid_event

    def send_message_to_raiders(self, content: str):
        asyncio.create_task(self._send_message_to_raiders(content))

    async def _send_message_to_raiders(self, content: str):
        for raider in await self.get_raiders():
            await raider.send(content)

    async def interact(self, message_type: Type[InteractionMessage], *args, **kwargs) -> Any:
        return await interact(self.member, message_type(self.client, self.discord_guild, *args, **kwargs))

