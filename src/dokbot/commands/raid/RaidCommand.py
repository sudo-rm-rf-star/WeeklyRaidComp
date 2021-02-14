from dokbot.commands.AbstractCog import AbstractCog
from dokbot.entities.RaidNotification import RaidNotification
from typing import List
from dokbot.entities.GuildMember import GuildMember
from logic.RaidEvent import RaidEvent
import utils.Logger as Log
from logic.enums.SignupStatus import SignupStatus
from datetime import datetime
from discord.ext import commands, Context
from persistence.RaidEventsResource import RaidEventsResource
from exceptions.InvalidInputException import InvalidInputException


class RaidCommand(AbstractCog):
    def __init__(self):
        super().__init__()
        self.raids_resource = RaidEventsResource()

    @commands.command()
    async def create_raid(self, ctx: Context, raid_name: str, raid_datetime: datetime):
        if raid_datetime < datetime.now():
            raise InvalidInputException('Raid event must be in future')
        raid_event = self.raids_resource.create_raid(raid_name=raid_name, raid_datetime=raid_datetime,
                                                     guild_id=self.raid_team.guild_id, team_name=self.raid_team.name)
        self.reply(ctx, f'Raid {raid_event} has been successfully created.')
        return raid_event
    #
    # async def create_raid(self, raid_name: str, raid_datetime: datetime, is_open: bool):
    #
    # async def send_raid_notification(self, raid_event: RaidEvent, raid_team, raiders: List[GuildMember]) -> None:
    #     Log.info(f'Sending {len(raiders)} invitations for {raid_event}')
    #     for raider in raiders:
    #         if not raid_event.has_user_signed(raider.id) or len(raiders) == 1:
    #             msg = await RaidNotification(self.client, self.discord_guild, raid_event, raid_team).send_to(raider)
    #             if msg:
    #                 self.messages_resource.create_personal_message(message_id=msg.id, guild_id=self.discord_guild.id,
    #                                                                user_id=raider.id, raid_name=raid_event.name,
    #                                                                raid_datetime=raid_event.datetime,
    #                                                                team_name=raid_event.team_name)
    #
    # async def get_unsigned_players(self, raid_event: RaidEvent):
    #     return [raider for raider in await self.get_raiders() if not raid_event.has_user_signed(raider.id)]
    #
    # async def get_tentative_players(self, raid_event: RaidEvent):
    #     return [raider for raider in await self.get_raiders() if raid_event.has_user_signed_as(raider.id, SignupStatus.TENTATIVE)]
    #
    # async def get_raiders(self) -> List[GuildMember]:
    #     raiders = []
    #     try:
    #         async for member in self.discord_guild.fetch_members(limit=None):
    #             if member and any(role.name == self.raid_team.raider_rank for role in member.roles):
    #                 raiders.append(GuildMember(member, self.discord_guild.id))
    #     except discord.Forbidden as e:
    #         self.respond(f'There are non-transient problems with Discord permissions...')
    #         raise e
    #     return raiders
    #
    # async def get_raid_event(self, raid_name: str, raid_datetime: datetime) -> RaidEvent:
    #     raid_team = await self.get_raidteam()
    #     raid_event = self.raids_resource.get_raid(guild_id=raid_team.guild_id, team_name=raid_team.name,
    #                                               raid_name=raid_name, raid_datetime=raid_datetime)
    #     if not raid_event:
    #         raise InvalidInputException(f'Raid event not found for {raid_name}')
    #     return raid_event
    #
    # def send_message_to_raiders(self, content: str):
    #     asyncio.create_task(self._send_message_to_raiders(content))
    #
    # async def _send_message_to_raiders(self, content: str):
    #     for raider in await self.get_raiders():
    #         await raider.send(content)
