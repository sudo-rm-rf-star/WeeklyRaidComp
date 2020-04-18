import discord
from src.common.Constants import RAID_INFO_EMBEDS
from src.logic.Raid import Raid
from src.logic.Roster import Roster
from src.disc.CommandUtils import delete_bot_messages, send_roster, update_datastores, get_roster_args
from src.disc.ServerUtils import get_channel
import json


async def make_roster(client, message, *argv):
    await update_datastores(client)
    raid_name, raid_datetime = get_roster_args(argv)
    raid = Raid.load(raid_name, raid_datetime)
    rosters = Roster.compose(raid)
    for roster in rosters:
        roster.save()
        await send_roster(client, roster, raid)


async def show_roster(client, message, *argv):
    raid_name, raid_datetime = get_roster_args(argv[2:])
    raid = Raid.load(raid_name, raid_datetime)
    roster = Roster.load(raid_name, raid_datetime)
    await send_roster(client, roster, raid)


async def unsupported(client, message, *argv):
    return f"Aborting. The following message still has to be implemented: '{message.content}'"


async def post_raid_info(client, message, *argv):
    if len(argv) > 0:
        return f'Expected no arguments'

    text_channel = get_channel(client, 'raid-info')
    await delete_bot_messages(client, text_channel)
    with open(RAID_INFO_EMBEDS) as raid_info_file:
        for embed_str in json.loads(raid_info_file.read()):
            await text_channel.send(embed=discord.Embed.from_dict(embed_str))
