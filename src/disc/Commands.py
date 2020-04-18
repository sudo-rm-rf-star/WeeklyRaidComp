import discord
from src.common.Constants import SUPPORTED_RAIDS
from src.common.Constants import RAID_INFO_EMBEDS
from src.common.Utils import parse_date
from src.logic.Raid import Raid
from src.logic.Roster import Roster
from src.disc.CommandUtils import delete_bot_messages, send_roster, backup_raids
from src.disc.ServerUtils import get_channel
from src.disc.exceptions.InvalidArgumentException import InvalidArgumentException
from src.common.Constants import DATE_FORMAT
from datetime import datetime
import json


def get_roster_args(argv):
    """Always final two arguments of command. Raid name (mandatory) and date (optional, default is upcoming)"""
    raid_date = None
    if len(argv) in [1, 2]:
        raid_name = argv[0].lower()
        if raid_name not in SUPPORTED_RAIDS:
            return InvalidArgumentException(f"Expected a valid raid: {', '.join(SUPPORTED_RAIDS)}")
        if len(argv) == 2:
            try:
                raid_date = parse_date(argv[1])
            except ValueError:
                raise InvalidArgumentException(
                    f'Invalid date "{argv[1]}" was given. Please format your date as {datetime.strftime(datetime.today(), fmt=DATE_FORMAT)}.')
    else:
        raise InvalidArgumentException("Expected a raid name and an optional raid date")

    return raid_name, raid_date


async def make_roster(client, message, *argv):
    raid_name, raid_date = get_roster_args(argv)
    rhms = await backup_raids(client)
    rhms_for_raid = [rhm for rhm in rhms if rhm.get_short_title() == raid_name]
    if not raid_date:
        today = datetime.today()
        raid_dates = [parse_date(raid.get_date()) for raid in rhms_for_raid]
        raid_date = min([raid_date for raid_date in raid_dates if raid_date > today], key=lambda x: x - today)

    rhms_for_raiddate = [rhm for rhm in rhms_for_raid if parse_date(rhm.get_date()) == raid_date]
    if len(rhms_for_raiddate) < 1:
        raise InvalidArgumentException(f"Could not find existing signup event for {raid_name} on {raid_date}.")
    elif len(rhms_for_raiddate) > 1:
        raise InvalidArgumentException(f"Found multiple of the same raid on the same day. Cannot continue.")

    rosters = Raid.get_rosters(raid_name, raid_date)
    for roster in rosters:
        await send_roster(client, roster, rhms_for_raiddate[0])


async def show_roster(client, message, *argv):
    return f"Aborting. The following message still has to be implemented: '{message.content}'"


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
