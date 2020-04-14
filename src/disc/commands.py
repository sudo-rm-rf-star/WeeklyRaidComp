import discord
from src.logic.Constant import supported_raids
from src.disc.constants import RAID_INFO_EMBEDS
from src.logic.Raid import Raid
from src.disc.commands_util import send_file, store_raid, get_channel, get_bot, delete_bot_messages
from datetime import datetime
import json


async def save_raids(client, message, *argv):
    if len(argv) != 0:
        return f'Expected 0 arguments.'

    raid_helper = get_bot(client, 'Raid-Helper')
    events_channel = get_channel(client, 'events')
    count = 0
    async for message in events_channel.history():
        if message.author == raid_helper:
            count += 1
            store_raid(message)
    return f"Successfully stored {count} raids."


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


async def post_raid_info(client, message, *argv):
    if len(argv):
        return f'Expected no arguments'

    text_channel = get_channel(client, 'raid-info')
    await delete_bot_messages(client, text_channel)
    with open(RAID_INFO_EMBEDS) as raid_info_file:
        for embed_str in json.loads(raid_info_file.read()):
            await text_channel.send(embed=discord.Embed.from_dict(embed_str))

