import discord
from src.common.Constants import RAID_INFO_EMBEDS, COMPS_CHANNEL, INFO_CHANNEL, LOGS_CHANNEL, DATETIMESEC_FORMAT
from src.common.Utils import now, from_datetime
from src.logic.Raid import Raid
from src.logic.Rosters import Rosters
from src.disc.CommandUtils import delete_bot_messages, get_roster_embed, update_datastores, get_read_roster_args, \
    get_update_roster_args
from src.disc.ServerUtils import get_channel
from src.exceptions.EventDoesNotExistException import EventDoesNotExistException
import json


async def make_roster(client, message, argv):
    await update_datastores(client)
    raid_name, raid_datetime = get_read_roster_args(argv)
    raid = Raid.load(raid_name, raid_datetime)
    text_channel = get_channel(client, COMPS_CHANNEL)

    try:
        rosters = Rosters.load(raid_name, raid_datetime)
        created_at = rosters.created_at
        old_message = await text_channel.fetch_message(rosters.message_id)
        rosters = Rosters.compose(raid)
        rosters.created_at = created_at
        await old_message.edit(embed=get_roster_embed(client, rosters, raid))
    except EventDoesNotExistException:
        rosters = Rosters.compose(raid)
        msg = await text_channel.send(embed=get_roster_embed(client, rosters, raid))
        rosters.set_message_id(msg.id)

    rosters.save()


async def show_roster(client, message, argv):
    raid_name, raid_datetime = get_read_roster_args(argv)
    raid = Raid.load(raid_name, raid_datetime)
    rosters = Rosters.load(raid_name, raid_datetime)
    embed = get_roster_embed(client, rosters, raid)
    await message.author.send(embed=embed)


async def accept_player(client, message, argv):
    update_command = lambda roster, player: roster.accept_player(player)
    await update_roster_command(client, message, argv, update_command)


async def bench_player(client, message, argv):
    update_command = lambda roster, player: roster.bench_player(player)
    await update_roster_command(client, message, argv, update_command)


async def remove_player(client, message, argv):
    update_command = lambda roster, player: roster.remove_player(player)
    await update_roster_command(client, message, argv, update_command)


async def update_roster_command(client, message, argv, update_command):
    await update_datastores(client)
    text_channel = get_channel(client, COMPS_CHANNEL)
    logs_channel = get_channel(client, LOGS_CHANNEL)
    raid_name, raid_datetime, player, roster_index = get_update_roster_args(argv)
    raid = Raid.load(raid_name, raid_datetime)
    rosters = Rosters.load(raid_name, raid_datetime)
    success, response = update_command(rosters.get(roster_index), player)
    await message.author.send(content=response)
    if success:
        old_message = await text_channel.fetch_message(rosters.message_id)
        await old_message.edit(embed=get_roster_embed(client, rosters, raid))
        await logs_channel.send(content=f'{from_datetime(now(), DATETIMESEC_FORMAT)} - {message.author} - {response}')
        rosters.save()


async def unsupported(client, message, *argv):
    return f"Aborting. The following message still has to be implemented: '{message.content}'"


async def post_raid_info(client, message, *argv):
    if len(argv) > 0:
        return f'Expected no arguments'

    text_channel = get_channel(client, INFO_CHANNEL)
    await delete_bot_messages(client, text_channel)
    with open(RAID_INFO_EMBEDS) as raid_info_file:
        for embed_str in json.loads(raid_info_file.read()):
            await text_channel.send(embed=discord.Embed.from_dict(embed_str))
