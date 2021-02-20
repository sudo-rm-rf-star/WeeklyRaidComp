from dokbot.entities.RaidNotification import RaidNotification
from typing import List
from dokbot.entities.GuildMember import GuildMember
from logic.RaidEvent import RaidEvent
import utils.Logger as Log
from logic.enums.SignupStatus import SignupStatus
from datetime import datetime
from discord.ext.commands import command, Cog, group, Context
from dokbot.DokBot import DokBot
from dokbot.entities.RaidTeamControlPanel import RaidTeamControlPanel
from dokbot.entities.enums.RaidTeamControlAction import RaidTeamControlAction
from persistence.RaidEventsResource import RaidEventsResource
from exceptions.InvalidInputException import InvalidInputException
import discord


class RaidCog(Cog, name='Raids'):
    def __init__(self, bot: DokBot):
        self.bot = bot
        self.raids_resource = RaidEventsResource()

    @group()
    async def raid(self, ctx: Context, name: str = None):
        f"""
        Organize and manage your raids for raid team.
        """
        await RaidTeamControlPanel.reply_in_channel(ctx, name=name)

    @Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.user_id == self.bot.user.id:
            return

        if payload.emoji.name not in RaidTeamControlAction.names():
            return

        action = RaidTeamControlAction[payload.emoji.name]
        message = await self.bot.message(payload.channel_id, payload.message_id)
        if not message.embeds or len(message.embeds) != 1:
            return

        if message.embeds[0].title != RaidTeamControlPanel.title():
            return

        member = await self.bot.fetch_user(payload.user_id)
        await message.remove_reaction(payload.emoji, member)
        if action == RaidTeamControlAction.AddRaid:
            print("Creating new raid.")
        else:
            return

    @raid.command()
    async def create(self, ctx: Context, raid_name: str, raid_datetime: datetime):
        """
        Create a new raid event.
        <raid_name> Name of the raid
        <raid_datetime> Datetime of the raid
        """
        if raid_datetime < datetime.now():
            raise InvalidInputException('Raid event must be in future')
        raid_event = self.raids_resource.create_raid(raid_name=raid_name, raid_datetime=raid_datetime,
                                                     guild_id=ctx.raid_team.guild_id, team_name=ctx.raid_team.name)
        self.bot.reply(ctx, f'Raid {raid_event} has been successfully created.')
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
