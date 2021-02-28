from datetime import datetime
from discord.ext.commands import Cog, group, Context
from dokbot.DokBot import DokBot
from dokbot.entities.RaidTeamControlPanel import RaidTeamControlPanel
from dokbot.entities.enums.RaidTeamControlAction import RaidTeamControlAction
from persistence.RaidEventsResource import RaidEventsResource
from exceptions.InvalidInputException import InvalidInputException
from .RaidTeamContext import RaidTeamContext
from dokbot.DokBotContext import DokBotContext
import discord
from dokbot.actions.CreateRaid import create_raid


class RaidTeamCog(Cog, name='Raid team'):
    def __init__(self, bot: DokBot):
        self.bot = bot
        self.raids_resource = RaidEventsResource()

    @group()
    async def team(self, ctx: Context, name: str = None):
        f"""
        Organize and manage your raids for raiding team.
        """
        ctx = DokBotContext.from_context(ctx)
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

        team_name = message.embeds[0].title.split(' ')[0]
        if not team_name:
            return

        user = await self.bot.fetch_user(payload.user_id)
        await message.remove_reaction(payload.emoji, user)
        guild = await self.bot.fetch_guild(payload.guild_id)
        channel = await self.bot.fetch_channel(payload.channel_id)
        context = RaidTeamContext(bot=self.bot, guild=guild, author=user, channel=channel, team_name=team_name)
        if action == RaidTeamControlAction.AddRaid:
            await create_raid(ctx=context)
        elif action == RaidTeamControlAction.ShowRaid:
            await show_raid(ctx=context)
        else :
            return
    #
    # async def send_raid_notification(self, raid_event: RaidEvent, raid_team, raiders: List[discord.Member]) -> None:
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
    # async def get_raiders(self) -> List[discord.Member]:
    #     raiders = []
    #     try:
    #         async for member in self.discord_guild.fetch_members(limit=None):
    #             if member and any(role.name == self.raid_team.raider_rank for role in member.roles):
    #                 raiders.append(discord.Member(member, self.discord_guild.id))
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
