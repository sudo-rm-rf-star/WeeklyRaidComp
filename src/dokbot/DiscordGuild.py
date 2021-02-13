from dokbot.DiscordUtils import *
from logic.RaidTeam import RaidTeam
from logic.RaidEvent import RaidEvent
from exceptions.InternalBotException import InternalBotException
from dokbot.entities.RaidMessage import RaidMessage
from utils.Constants import DATETIMESEC_FORMAT
from typing import Union
from datetime import datetime
import asyncio
import utils.Logger as Log


class DiscordGuild:
    def __init__(self, client: discord.Client, discord_guild: discord.Guild, raid_team: RaidTeam):
        self.client = client
        self.guild = discord_guild
        self.raid_team = raid_team
        self.id = discord_guild.id

    def set_raid_team(self, raid_team: RaidTeam):
        self.raid_team = raid_team

    async def get_member_by_id(self, user_id: int) -> GuildMember:
        return await get_member_by_id(self.guild, user_id)

    async def get_events_channel(self) -> discord.TextChannel:
        return await get_channel(self.guild, self.raid_team.events_channel)

    async def get_message(self, message_ref: MessageRef) -> Optional[discord.Message]:
        return await get_message(self.guild, message_ref)

    async def get_raiders(self) -> List[GuildMember]:
        raiders = []
        try:
            async for member in self.guild.fetch_members(limit=None):
                if member and any(role.name == self.raid_team.raider_rank for role in member.roles):
                    raiders.append(GuildMember(member, self.guild.id))
        except discord.Forbidden as e:
            raise InternalBotException(f'There are non-transient problems with Discord permissions...\n{e}')
        return raiders

    async def send_message_to_raiders(self, content: str):
        for raider in await self.get_raiders():
            await raider.send(content)

    async def sync_raid_message(self, raid_event: RaidEvent):
        await RaidMessage.sync_message(self.client, self.guild, raid_event)

    def respond(self, content: str, member: discord.Member,
                action: Union[discord.Message, discord.RawReactionActionEvent]):
        action = action.content if isinstance(action, discord.Message) else action.emoji
        log_message = f'{datetime.now().strftime(DATETIMESEC_FORMAT)} - {member.display_name} - {action} - {content} '
        asyncio.create_task(self.log(content=log_message))
        asyncio.create_task(member.send(content=content))

    async def log(self, content: str):
        if self.raid_team:
            logs_channel = await get_channel(self.guild, self.raid_team.logs_channel)
            await logs_channel.send(content)
        Log.info(content)

    @staticmethod
    async def create_helper(client: discord.Client, raid_team: Optional[RaidTeam] = None):
        discord_guild = await client.fetch_guild(raid_team.guild_id)
        return DiscordGuild(client, discord_guild, raid_team)
