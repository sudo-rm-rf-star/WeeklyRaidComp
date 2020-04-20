import discord
from src.common.Constants import RAID_HELPER_BOT, EVENTS_CHANNEL
from src.disc.ServerUtils import get_channel, get_bot
from src.disc.RaidHelperMessage import RaidHelperMessage
from src.disc.RosterFormatter import RosterFormatter


async def send_file(filename, recipient, content=""):
    file = discord.File(filename)
    await recipient.send(content=content, file=file)


async def delete_bot_messages(client, text_channel):
    is_me = lambda msg: msg.author == client.user
    await text_channel.purge(check=is_me)


async def update_raids(client):
    events_channel = get_channel(client, EVENTS_CHANNEL)
    raid_helper = get_bot(client, RAID_HELPER_BOT)
    async for message in events_channel.history():
        if message.author == raid_helper:
            rhm = RaidHelperMessage(message)
            rhm.to_raid().save()


def get_roster_embed(client, rosters, raid):
    roster_formatter = RosterFormatter(client, raid, rosters)
    return roster_formatter.roster_to_embed()
