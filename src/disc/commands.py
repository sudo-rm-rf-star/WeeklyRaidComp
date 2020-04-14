import discord
from logic.Constant import raid_abbrev_short, supported_raids
from logic.Raid import Raid
from collections import defaultdict
from datetime import datetime
import os
import json

RAID_STORAGE = os.path.join('data', 'raids', 'input')
GUILD = os.getenv('DISCORD_GUILD')


async def save_raids(client, message, *argv):
    if len(argv) != 0:
        return f'Expected 0 arguments.'

    guild = discord.utils.get(client.guilds, name=GUILD)
    raid_helper = discord.utils.get(guild.members, name='Raid-Helper')
    events_channel = discord.utils.get(guild.channels, name='events')
    count = 0
    async for message in events_channel.history():
        if message.author == raid_helper:
            count += 1
            store_raid(message)
    return f"Succesffully stored {count} raids."


async def make_roster(client, message, *argv):
    if len(argv) not in [1, 2]:
        return f'Expected 1 or 2 arguments.'
    raid_name = argv[0].lower()
    if raid_name not in supported_raids:
        return f'I cannot make a raid for "{raid_name}", please try one of the following: {", ".join(supported_raids)}'
    try:
        raid_date = datetime.strptime(argv[1], '%Y-%m-%d') if len(argv) == 2 else None
    except ValueError:
        return f'Invalid date "{argv[1]}" was given. Please format your date as "YYYY-MM-DD".'

    success, filename = Raid.write_roster(raid_name, raid_date)
    if not success:
        return f'Internal server error when executing "{message.content}"'
    else:
        await send_file(filename, message.author, content=f"Successfully made a roster for {raid_name.upper()}:")


async def send_file(filename, recipient, content=""):
    file = discord.File(filename)
    await recipient.send(content=content, file=file)


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
