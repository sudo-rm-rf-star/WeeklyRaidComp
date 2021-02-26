from utils.Constants import BOT_NAME
from persistence.RaidTeamsResource import RaidTeamsResource
from dokbot.interactions.TextInteractionMessage import TextInteractionMessage
from dokbot.interactions.OptionInteraction import OptionInteraction
from dokbot.interactions.DiscordRoleInteraction import DiscordRoleInteraction
from dokbot.interactions.DiscordChannelInteraction import DiscordChannelInteraction
from logic.RaidTeam import RaidTeam
import discord

INTRODUCTORY_MESSAGE = f'''
Thanks for giving {BOT_NAME} a chance! I hope I'll prove useful for your guild. Let me give a brief introduction 
of my purpose. My main purpose is to make raid organization for your guild as easy to manage as possible. 
I'll help you with some of those time-consuming tasks with organizing raids me. Next to just helping the raid 
leaders life, it also tries to help the raider by serving as a medium between the raider and raid leader. 
You can use me as to create raids, I will send a personal message to every raider on Discord through which 
they can sign for the raid. I'll create a Discord message which contains all of the information of the raid 
which includes all of the raider information such as their character name, their role, their class and how they 
signed for your raid. At any point after raid creation you can decide to create a roster for your raid. The bot 
uses heuristics to create an optimal roster for you and sends status updates to all of the raiders telling them 
whether they got a spot in your raid. Don't worry, you can manually make any changes if you're not happy with 
the outcome. This is a quick summary on my main functionality, for a more detailed guide on how to use me, 
please type: `!dokbot help`. For now, let's start with setting up your guild! Please answer the following 
questions
'''


async def create_raidteam(client: discord.Client, discord_guild: discord.Guild, member: discord.Member,
                          first: bool) -> RaidTeam:
    if first:
        await member.send(INTRODUCTORY_MESSAGE)
    msg = "Please fill in the name for your raid team."
    team_name = await TextInteractionMessage.interact(client=client, guild=discord_guild, member=member, content=msg)
    msg = "Please fill in the realm of your team."
    realm = await TextInteractionMessage.interact(client=client, guild=discord_guild, member=member, content=msg)
    msg = "Please fill in the region of your team."
    options = ["EU"]
    region = await OptionInteraction.interact(client=client, guild=discord_guild, member=member, content=msg,
                                              options=options)
    msg = "Please choose a Discord text channel to post all of the raid events for this raid group."
    events_channel = await DiscordChannelInteraction.interact(client=client, guild=discord_guild, content=msg,
                                                              member=member)
    msg = "Please select a Discord TextChannel to post all of the logs for this bot. This will contain additional " \
          "information on any interaction with this bot."
    logs_channel = await DiscordChannelInteraction.interact(client=client, guild=discord_guild, content=msg,
                                                            member=member)

    msg = "Please choose a Discord role for your raiders. Players with this role will be automatically invited to any " \
          "of your raids."
    raider_rank = await DiscordRoleInteraction.interact(client=client, guild=discord_guild, member=member, content=msg)
    msg = "Please choose the Discord role to manage this raid team. Players with this role can for example create new raids and " \
          "execute other DokBot commands."
    manager_rank = await DiscordRoleInteraction.interact(client=client, guild=discord_guild, member=member, content=msg)
    raid_team = RaidTeam(guild_id=discord_guild.id, team_name=team_name, raider_rank=raider_rank, realm=realm,
                         region=region, officer_rank=manager_rank, events_channel=events_channel,
                         logs_channel=logs_channel)
    RaidTeamsResource().create_raidteam(raid_team)
    await member.send(f"Your raid team {raid_team} has succesfully been created!")
    return raid_team
