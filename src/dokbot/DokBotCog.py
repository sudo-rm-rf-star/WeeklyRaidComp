import discord
from discord.ext.commands import Cog, Context, command

from dokbot.DokBot import DokBot
from dokbot.DokBotContext import DokBotContext
from dokbot.RaidContext import RaidContext
from dokbot.raid_actions.ActionsRaid import ActionsRaid
from dokbot.raidteam_actions.ActionsRaidTeam import ActionsRaidTeam
from dokbot.raidteam_actions.AddRaider import add_raider
from dokbot.raidteam_actions.AddRaidleader import add_raidleader
from dokbot.raidteam_actions.CreateRaid import create_raid
from dokbot.raidteam_actions.ManageRaid import manage_raid
from dokbot.raidteam_actions.ShowRaidTeam import show_raid_team
from dokbot.raidteam_actions.SwitchRaidTeam import switch_raidteam
from dokbot.raid_actions.CreateRosterManual import create_roster_manual
from dokbot.raid_actions.CreateRosterAutomatic import create_roster_automatic
from dokbot.raid_actions.Invite import invite
from dokbot.raid_actions.OpenRaid import open_raid
from dokbot.raid_actions.RemoveRaid import remove_raid
from dokbot.raid_actions.SendReminder import send_reminder
from dokbot.raid_actions.UpdateRoster import update_roster
from dokbot.entities.RaidTeamMessage import RaidTeamMessage
from persistence.RaidEventsResource import RaidEventsResource
from persistence.RaidTeamsResource import RaidTeamsResource
from persistence.MessagesResource import MessagesResource
from logic.enums.RosterStatus import RosterStatus
from .RaidTeamContext import RaidTeamContext
from utils.Constants import MAINTAINER_ID
from exceptions.InvalidInputException import InvalidInputException


class DokBotCog(Cog, name='DokBot'):
    def __init__(self, bot: DokBot):
        self.bot = bot
        self.raids_resource = RaidEventsResource()

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
    async def raid(self, ctx: Context, name: str = None):
        """
        Manage a raid.
        """
        ctx = DokBotContext.from_context(ctx)
        await RaidTeamMessage.reply_in_channel(ctx, name=name)

    @Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        message = await verify_and_get_message(self.bot, payload)
        if not message:
            return

        channel = await self.bot.fetch_channel(payload.channel_id)
        user = await self.bot.fetch_user(payload.user_id)
        await message.remove_reaction(payload.emoji, user)
        guild = await self.bot.fetch_guild(payload.guild_id)
        action_name = payload.emoji.name

        try:
            if action_name in ActionsRaidTeam.names():
                team_name = message.embeds[0].title.split(' ')[0].strip('<>')
                if not team_name:
                    return
                ctx = RaidTeamContext(bot=self.bot, guild=guild, author=user, channel=channel, team_name=team_name)
                await handle_raid_team_action(ctx=ctx, action=ActionsRaidTeam[action_name])
            elif action_name in ActionsRaid.names():
                message_ref = MessagesResource().get_message(message.id)
                if not message_ref:
                    return
                ctx = RaidContext(bot=self.bot, guild=guild, author=user, channel=channel,
                                  team_name=message_ref.team_name,
                                  raid_name=message_ref.raid_name, raid_datetime=message_ref.raid_datetime)
                await handle_raid_action(ctx=ctx, action=ActionsRaid[action_name])
        except InvalidInputException:
            pass
        except Exception as e:
            await channel.send("Unexpected issue! Try again later.")
            maintainer = await self.bot.fetch_user(MAINTAINER_ID)
            await maintainer.send(f"Unexpected issue. {user.name}, {user.display_name}, {action_name}, {e}")
            raise e


async def handle_raid_team_action(ctx: RaidTeamContext, action: ActionsRaidTeam):
    if not await verify_authorized(ctx.author.id, ctx):
        return

    if action == ActionsRaidTeam.AddRaid:
        await create_raid(ctx=ctx)
    elif action == ActionsRaidTeam.ManageRaid:
        await manage_raid(ctx=ctx)
    elif action == ActionsRaidTeam.AddRaider:
        await add_raider(ctx=ctx)
    elif action == ActionsRaidTeam.ShowRaidTeam:
        await show_raid_team(ctx=ctx)
    elif action == ActionsRaidTeam.AddRaidLeader:
        await add_raidleader(ctx=ctx)
    elif action == ActionsRaidTeam.SwitchRaidTeam:
        await switch_raidteam(ctx=ctx)
    else:
        return


async def handle_raid_action(ctx: RaidContext, action: ActionsRaid):
    if not await verify_authorized(ctx.author.id, ctx):
        return

    if action == ActionsRaid.AddRaider:
        await invite(ctx)
    elif action == ActionsRaid.OpenRaid:
        await open_raid(ctx)
    elif action == ActionsRaid.RemoveRaid:
        await remove_raid(ctx)
    elif action == ActionsRaid.Accept:
        await update_roster(ctx, RosterStatus.ACCEPT)
    elif action == ActionsRaid.Bench:
        await update_roster(ctx, RosterStatus.EXTRA)
    elif action == ActionsRaid.Decline:
        await update_roster(ctx, RosterStatus.DECLINE)
    elif action == ActionsRaid.CreateRosterAutomatic:
        await create_roster_automatic(ctx)
    elif action == ActionsRaid.CreateRosterManual:
        await create_roster_manual(ctx)
    elif action == ActionsRaid.SendReminder:
        await send_reminder(ctx)
    else:
        return


async def verify_and_get_message(bot: DokBot, payload: discord.RawReactionActionEvent):
    if payload.user_id == bot.user.id:
        return

    message = await bot.message(payload.channel_id, payload.message_id)
    if message.author.id != bot.user.id:
        return

    if not message.embeds or len(message.embeds) != 1:
        return

    return message


async def verify_authorized(user_id, ctx: RaidTeamContext):
    if user_id in ctx.raid_team.manager_ids:
        return True

    await ctx.reply("You are not authorized to do this.")
    return False
