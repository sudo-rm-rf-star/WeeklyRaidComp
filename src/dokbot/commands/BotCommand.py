from exceptions.MissingImplementationException import MissingImplementationException
from dokbot.utils.CommandUtils import check_authority
from dokbot.utils.RaidTeamSelectionInteraction import RaidTeamSelectionInteraction
from dokbot.entities.GuildMember import GuildMember
from utils.Constants import DATETIMESEC_FORMAT
from dokbot.DiscordUtils import get_channel
from discord import Message, TextChannel
from datetime import datetime
from typing import Optional, List, Any, Type, Set
from persistence.MessagesResource import MessagesResource
from persistence.RaidEventsResource import RaidEventsResource
from persistence.PlayersResource import PlayersResource
from persistence.RaidTeamsResource import RaidTeamsResource
from logic.RaidEvent import RaidEvent
from logic.Player import Player
from logic.RaidTeam import RaidTeam
from logic.MessageRef import MessageRef
from events.EventQueue import EventQueue
import asyncio
import discord
from dokbot.utils.ArgParser import ArgParser
from exceptions.InvalidInputException import InvalidInputException
from dokbot.utils.PlayerInteraction import _interact, InteractionMessage
import utils.Logger as Log

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

    def __init__(self, client: discord.Client,
                 message: Optional[Message],
                 message_ref: Optional[MessageRef], raw_reaction: discord.RawReactionActionEvent, member: GuildMember,
                 player: Player, discord_guild: discord.Guild, raidteam: RaidTeam, channel: Optional[TextChannel]):
        self.players_resource: PlayersResource = PlayersResource()
        self.raids_resource: RaidEventsResource = RaidEventsResource()
        self.teams_resource: RaidTeamsResource = RaidTeamsResource()
        self.messages_resource = MessagesResource()
        self.event_queue = EventQueue()
        self.client: discord.Client = client
        self.message = message
        self.message_ref = message_ref
        self.raw_reaction = raw_reaction
        self.member = member
        self.player = player
        self.discord_guild = discord_guild
        self.channel = channel
        self.raid_team = raidteam

    async def execute(self, **kwargs):
        raise MissingImplementationException(BotCommand)

    async def call(self, **kwargs):
        if self.req_manager_rank():
            raid_team = await self.get_raidteam()
            required_rank = raid_team.officer_rank
            check_authority(self.member, required_rank)
        await self.execute(**kwargs)

    async def get_raidteam(self) -> RaidTeam:
        if not self.raid_team:
            self.raid_team = await self.interact(RaidTeamSelectionInteraction)
        return self.raid_team

    def respond(self, content: str):
        action = self.message.content if self.message else self.raw_reaction.emoji
        log_message = f'{datetime.now().strftime(DATETIMESEC_FORMAT)} - {self.member.display_name} - {action} - {content} '
        asyncio.create_task(self.log(content=log_message))
        asyncio.create_task(self.member.send(content=content))

    async def log(self, content: str):
        if self.raid_team:
            await get_channel(self.discord_guild, self.raid_team.logs_channel)
        Log.info(content)

    def post(self, content: str):
        asyncio.create_task(self.channel.send(content=content))

    @classmethod
    def get_help(cls) -> str:
        prefix = f'!{cls.name()} {cls.sub_name()}'
        command_with_arg_names = f'\n`{prefix} {cls.argformat()}`'
        example_args = cls.example_args() if cls.example_args() else ArgParser(cls.argformat()).get_example_args()
        command_with_arg_examples = f'\n`{prefix} {example_args}`' if example_args else ''
        return f'**{cls.description()}**{command_with_arg_names}{command_with_arg_examples}'

    async def get_raiders(self) -> List[GuildMember]:
        raiders = []
        try:
            async for member in self.discord_guild.fetch_members(limit=None):
                if member and any(role.name == self.raid_team.raider_rank for role in member.roles):
                    raiders.append(GuildMember(member, self.discord_guild.id))
        except discord.Forbidden as e:
            self.respond(f'There are non-transient problems with Discord permissions...')
            raise e
        return raiders

    async def get_raid_event(self, raid_name: str, raid_datetime: datetime) -> RaidEvent:
        raid_team = await self.get_raidteam()
        raid_event = self.raids_resource.get_raid(guild_id=raid_team.guild_id, team_name=raid_team.name,
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
        return await message_type.interact(member=self.member, client=self.client, guild=self.discord_guild, *args, **kwargs)

