from datetime import datetime

import discord
from discord.ext.commands import Cog, Context, command

from dokbot.DokBot import DokBot
from dokbot.DokBotContext import DokBotContext
from dokbot.RaidContext import RaidContext
from dokbot.entities.HelpMessage import HelpMessage
from dokbot.entities.RaidMessage import RaidMessage
from dokbot.entities.RaidTeamMessage import RaidTeamMessage
from dokbot.player_actions.SignupCharacter import signup_character
from dokbot.raid_actions.ActionsRaid import ActionsRaid
from dokbot.raid_actions.CreateRoster import create_roster
from dokbot.raid_actions.Invite import invite
from dokbot.raid_actions.OpenRaid import open_raid
from dokbot.raid_actions.RemoveRaid import remove_raid
from dokbot.raid_actions.SendReminder import send_reminder
from dokbot.raid_actions.UpdateRoster import update_roster
from dokbot.raidteam_actions.ActionsRaidTeam import ActionsRaidTeam
from dokbot.raidteam_actions.AddRaider import add_raider
from dokbot.raidteam_actions.RemoveRaider import remove_raider
from dokbot.raidteam_actions.AddRaiders import add_raiders
from dokbot.raidteam_actions.AddRaidleader import add_raid_leader
from dokbot.raidteam_actions.CreateRaid import create_raid
from dokbot.raidteam_actions.ManageRaid import manage_raid
from dokbot.raidteam_actions.ShowRaidTeam import show_raid_team
from dokbot.raidteam_actions.SwitchRaidTeam import switch_raidteam
from logic.enums.RosterStatus import RosterStatus
from logic.enums.SignupStatus import SignupStatus
from persistence.MessagesResource import MessagesResource
from persistence.RaidTeamsResource import RaidTeamsResource
from exceptions.BotException import BotException
from utils.Constants import MAINTAINER_ID
from .RaidTeamContext import RaidTeamContext
import logging
import traceback


class DokBotCog(Cog, name='DokBot'):
    def __init__(self, bot: DokBot):
        self.bot = bot

    @command()
    async def dokbot(self, ctx: Context):
        """
        Organize and manage your raids for raiding team.
        """
        ctx = DokBotContext.from_context(ctx)
        raid_team = RaidTeamsResource().get_selected_raidteam(guild_id=ctx.guild_id, discord_id=ctx.author.id)
        await RaidTeamMessage.reply_in_channel(ctx, raid_team=raid_team)

    @command()
    async def team(self, ctx: Context, name: str):
        """
        Organize and manage your raids for raiding team.
        """
        ctx = DokBotContext.from_context(ctx)
        await RaidTeamMessage.reply_in_channel(ctx, name=name)

    @command()
    async def raid(self, ctx: Context, raid_name: str, raid_datetime: int, team_name: str):
        """
        Manage a raid.
        """
        ctx = RaidContext(bot=self.bot, guild=ctx.guild, author=ctx.author, channel=ctx.channel, team_name=team_name,
                          raid_name=raid_name, raid_datetime=datetime.fromtimestamp(raid_datetime))
        await RaidMessage.reply_in_channel(ctx, for_raid_leaders=True)

    @Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        message = await verify_and_get_message(self.bot, payload)
        if not message:
            return

        channel = await self.bot.fetch_channel(payload.channel_id)
        user = await self.bot.fetch_user(payload.user_id)
        action_name = payload.emoji.name

        is_raid_action = action_name in ActionsRaid.names()
        is_raid_team_action = action_name in ActionsRaidTeam.names()
        is_signup_action = action_name in SignupStatus.names()
        try:
            if is_raid_team_action:
                team_name = message.embeds[0].title.split(' ')[0].strip('<>')
                if not team_name:
                    return
                guild = await self.bot.fetch_guild(payload.guild_id)
                with RaidTeamContext(bot=self.bot, guild=guild, author=user, channel=channel, team_name=team_name) as ctx:
                    await handle_raid_team_action(ctx=ctx, action=ActionsRaidTeam[action_name])
            elif is_signup_action or is_raid_action:
                message_ref = MessagesResource().get_message(message.id)
                if not message_ref:
                    await user.send("Raid no longer exists")
                    return
                guild = await self.bot.fetch_guild(message_ref.guild_id)
                with RaidContext(bot=self.bot, guild=guild, author=user, channel=channel,
                                 team_name=message_ref.team_name,
                                 raid_name=message_ref.raid_name, raid_datetime=message_ref.raid_datetime) as ctx:
                    if is_raid_action:
                        await handle_raid_action(ctx=ctx, action=ActionsRaid[action_name])
                    elif is_signup_action:
                        if not ctx.raid_event.is_open:
                            await ctx.reply_to_author("An invitation is required to sign.")
                            return
                        await signup_character(ctx=ctx, signup_status=SignupStatus[action_name])

            if not isinstance(channel, discord.DMChannel):
                await message.remove_reaction(payload.emoji, user)

        except BotException as e:
            await channel.send(e.message)
        except Exception as e:
            await channel.send("Unexpected issue! Try again later.")
            maintainer = await self.bot.fetch_user(MAINTAINER_ID)
            error_msg = f"Unexpected issue. {user.name}, {user}, {action_name}, {e}\n{traceback.format_exc()}"
            logging.getLogger().error(error_msg)
            await maintainer.send(f"Unexpected issue. {user.name}, {user.display_name}, {action_name}, {e}")
            raise e


async def handle_raid_team_action(ctx: RaidTeamContext, action: ActionsRaidTeam):
    if not ctx.raid_team or not await verify_authorized(ctx.author.id, ctx):
        return

    if action == ActionsRaidTeam.AddRaid:
        await create_raid(ctx=ctx)
    elif action == ActionsRaidTeam.ManageRaid:
        await manage_raid(ctx=ctx)
    elif action == ActionsRaidTeam.AddRaider:
        await add_raider(ctx=ctx)
    elif action == ActionsRaidTeam.AddRaiders:
        await add_raiders(ctx=ctx)
    elif action == ActionsRaidTeam.RemoveRaider:
        await remove_raider(ctx=ctx)
    elif action == ActionsRaidTeam.ShowRaidTeam:
        await show_raid_team(ctx=ctx)
    elif action == ActionsRaidTeam.AddRaidLeader:
        await add_raid_leader(ctx=ctx)
    elif action == ActionsRaidTeam.SwitchRaidTeam:
        await switch_raidteam(ctx=ctx)
    elif action == ActionsRaidTeam.HelpRaidTeam:
        await HelpMessage.reply_in_channel(ctx=ctx, actions=ActionsRaidTeam)
    else:
        return


async def handle_raid_action(ctx: RaidContext, action: ActionsRaid):
    if not ctx.raid_team or not await verify_authorized(ctx.author.id, ctx):
        return

    if action == ActionsRaid.InviteRaider:
        await invite(ctx)
    elif action == ActionsRaid.OpenRaid:
        await open_raid(ctx)
    elif action == ActionsRaid.RemoveRaid:
        await remove_raid(ctx)
    elif action == ActionsRaid.RosterAccept:
        await update_roster(ctx, RosterStatus.Accept)
    elif action == ActionsRaid.RosterBench:
        await update_roster(ctx, RosterStatus.Extra)
    elif action == ActionsRaid.RosterDecline:
        await update_roster(ctx, RosterStatus.Decline)
    elif action == ActionsRaid.CreateRoster:
        await create_roster(ctx)
    elif action == ActionsRaid.SendReminder:
        await send_reminder(ctx)
    elif action == ActionsRaid.HelpRaid:
        await HelpMessage.reply_in_channel(ctx=ctx, actions=ActionsRaid)
    else:
        return


async def verify_and_get_message(bot: DokBot, payload: discord.RawReactionActionEvent):
    if payload.user_id == bot.user.id:
        return

    message = await bot.message(payload.channel_id, payload.message_id)
    if message.author.id != bot.user.id:
        return

    return message


async def verify_authorized(user_id, ctx: RaidTeamContext):
    if user_id in ctx.raid_team.manager_ids:
        return True

    await ctx.reply("You are not authorized to do this.")
    return False
