import discord
from src.disc.exceptions.NotAuthorizedException import NotAuthorizedException
from src.common.Constants import BOT_NAME, RAID_HELPER_BOT, EVENTS_CHANNEL, OFFICER_RANK
from src.disc.ServerUtils import get_guild, get_channel, get_bot
from src.disc.RaidHelperMessage import RaidHelperMessage
from src.disc.RosterFormatter import RosterFormatter


async def send_file(filename, recipient, content=""):
    file = discord.File(filename)
    await recipient.send(content=content, file=file)


async def delete_bot_messages(client, text_channel):
    guild = get_guild(client)
    bot = discord.utils.get(guild.members, name=BOT_NAME)
    async for message in text_channel.history():
        if message.author == bot:
            await message.delete()


async def send_roster(client, roster, rhm):
    text_channel = get_channel(client, 'test')
    roster_formatter = RosterFormatter(client, rhm, roster)
    embed = roster_formatter.roster_to_embed()
    await text_channel.send(embed=embed)


async def backup_raids(client):
    raid_helper = get_bot(client, RAID_HELPER_BOT)
    events_channel = get_channel(client, EVENTS_CHANNEL)
    rhms = []
    async for message in events_channel.history():
        if message.author == raid_helper:
            rhm = RaidHelperMessage(message)
            rhm.save()
            rhms.append(rhm)
    return rhms


def officer_rank(author):
    return check_authority(author, OFFICER_RANK)


def anyone(*args):
    return True


def check_authority(author, required_rank):
    if required_rank not in author.roles:
        raise NotAuthorizedException()
