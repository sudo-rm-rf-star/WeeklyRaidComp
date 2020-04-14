import discord
from collections import defaultdict
from src.logic.Constant import raid_abbrev_short
from src.disc.constants import GUILD, RAID_STORAGE, BOT_NAME
import json
import os


async def send_file(filename, recipient, content=""):
    file = discord.File(filename)
    await recipient.send(content=content, file=file)


async def delete_bot_messages(client, text_channel):
    guild = get_guild(client)
    raid_helper = discord.utils.get(guild.members, name=BOT_NAME)
    async for message in text_channel.history():
        if message.author == raid_helper:
            await text_channel.delete(message)


def get_guild(client):
    print(GUILD)
    return discord.utils.get(client.guilds, name=GUILD)


def get_bot(client, bot_name=BOT_NAME):
    return discord.utils.get(get_guild(client).members, name=bot_name)


def get_channel(client, channel_name):
    return discord.utils.get(get_guild(client).channels, name=channel_name)


def store_raid(message):
    rows = [field.value for embed in message.embeds for field in embed.fields]
    title_i = 0
    date_i = 3
    accepted_i = 5
    other_i = 15
    title = ''.join([chars[-1] for chars in rows[title_i].split('_')][:-1])
    if title not in raid_abbrev_short:
        return

    title = raid_abbrev_short[title]
    date = rows[date_i].split(']')[0].split('[')[-1]
    signees = defaultdict(list)

    for entries in rows[accepted_i:other_i]:
        for entry in entries.splitlines()[1:]:
            cols = entry.split(' ')
            signup_choice = cols[0].split(':')[1]
            charname = cols[-1].split('**')[1]
            signees[signup_choice].append(charname)

    for entry in rows[other_i].splitlines()[1:]:
        signup_choice = entry.split(':')[1]
        for charname in entry.split('**')[1::2]:
            signees[signup_choice].append(charname)

    with open(os.path.join(RAID_STORAGE, f'{title}_{date}.csv'), 'w+') as out_file:
        out_file.write(json.dumps({
            'name': title,
            'date': date,
            'signees': signees
        }))
