from utils.Constants import BOT_NAME
from persistence.RaidTeamsResource import RaidTeamsResource
from dokbot.interactions.TextInteractionMessage import TextInteractionMessage
from dokbot.interactions.OptionInteraction import OptionInteraction
from dokbot.interactions.DiscordChannelInteraction import DiscordChannelInteraction
from dokbot.DokBotContext import DokBotContext
from logic.RaidTeam import RaidTeam

INTRODUCTORY_MESSAGE = f'''
Welcome to {BOT_NAME}! I'm here to serve you as a raid leader! Please answer the following questions to start.
'''


async def create_raidteam(ctx: DokBotContext,
                          first: bool) -> RaidTeam:
    if first:
        await ctx.channel.send(INTRODUCTORY_MESSAGE)
    msg = "Please fill in the name for your raid team."
    team_name = await TextInteractionMessage.interact(ctx=ctx, content=msg)
    msg = "Please fill in the realm of your team."
    realm = await TextInteractionMessage.interact(ctx=ctx, content=msg)
    msg = "Please fill in the region of your team."
    options = ["EU"]
    region = await OptionInteraction.interact(ctx=ctx, content=msg, options=options)
    msg = "Please choose a channel where I can show raids to your raiders"
    events_channel = await DiscordChannelInteraction.interact(ctx=ctx, content=msg)
    msg = "Please select a channel where you want to manage this raiding team and its raids"
    manager_channel = await DiscordChannelInteraction.interact(ctx=ctx, content=msg)
    msg = "Please select a channel to post all of the logs for this bot. This will contain additional information on any interaction with this bot."
    logs_channel = await DiscordChannelInteraction.interact(ctx=ctx, content=msg)
    raid_team = RaidTeam(guild_id=ctx.guild_id, team_name=team_name, raider_ids=[], realm=realm,
                         region=region, manager_ids=[ctx.author.id], events_channel=events_channel.name,
                         manager_channel=manager_channel.name, logs_channel=logs_channel.name)
    RaidTeamsResource().create_raidteam(raid_team)
    await ctx.author.send(f"Your raid team {raid_team} has successfully been created!")
    return raid_team
