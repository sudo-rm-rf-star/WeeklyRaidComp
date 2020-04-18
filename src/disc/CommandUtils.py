import discord
from src.exceptions.NotAuthorizedException import NotAuthorizedException
from src.exceptions.InvalidArgumentException import InvalidArgumentException
from src.filehandlers.WhitelistedFileHandler import update_whitelisted
from src.common.Constants import RAID_HELPER_BOT, EVENTS_CHANNEL, OFFICER_RANK, SUPPORTED_RAIDS
from src.common.Utils import from_datetime, to_datetime, today, now, from_date, to_date
from src.disc.ServerUtils import get_channel, get_bot, get_user_by_id, get_users
from src.disc.RaidHelperMessage import RaidHelperMessage
from src.disc.RosterFormatter import RosterFormatter


def get_read_roster_args(argv):
    arg_dict = _get_args(argv)
    if 'roster_index' in arg_dict or 'player_index' in arg_dict:
        raise InvalidArgumentException("This command only expects the raid name and an optional datetime.")

    return arg_dict['raid_name'], arg_dict.get('raid_datetime', None)


def get_update_roster_args(argv):
    arg_dict = _get_args(argv)
    if 'player' not in arg_dict:
        raise InvalidArgumentException("This command requires a player name to be given.")

    return arg_dict['raid_name'], arg_dict.get('raid_datetime', None), arg_dict['player'], arg_dict.get('roster_index', 0)


def _get_args(argv):
    """
    Raid name (mandatory),
    Date and time (optional, default is upcoming)
    Roster index (optional)
    e.g "zg -p Dok -d 31-01-2020 19:30 -t 2"
    """
    if len(argv.strip()) == 0:
        raise InvalidArgumentException("Expected at least a raid name")

    args = argv.split('-')

    raid_name = args[0].strip()
    if raid_name not in SUPPORTED_RAIDS:
        raise InvalidArgumentException(f"Expected a valid raid: {', '.join(SUPPORTED_RAIDS)}")
    arguments = {
        'raid_name': raid_name
    }
    named_args = [parse_named_args(arg) for arg in args[1:]]
    arguments.update([arg for arg in named_args if arg is not None])
    return arguments


def parse_named_args(arg):
    if len(arg.strip()) > 0:
        startswith = arg[0]
        arg = arg[1:].strip()
        if startswith == 'd':
            return 'raid_datetime', get_datetime(arg)
        elif startswith == 't':
            return 'roster_index', int(arg) - 1
        elif startswith == 'p':
            return 'player', arg
        else:
            raise InvalidArgumentException(f"Received invalid argument -{arg}")


def get_datetime(arg):
    args = arg.split(' ')
    if len(args) == 0:
        raise InvalidArgumentException(f'Could not find a date.')
    elif len(args) == 1:
        raid_date_arg = args[0]
        try:
            raid_datetime = to_date(raid_date_arg)
        except ValueError:
            raise InvalidArgumentException(
                f'Invalid date "{arg}" was given. Please format your date as {from_date(today())}.')

    elif len(args) == 2:
        raid_datetime_arg = f'{args[0]} {args[1]}'
        try:
            raid_datetime = to_datetime(raid_datetime_arg)
        except ValueError:
            raise InvalidArgumentException(
                f'Invalid datetime "{arg}" was given. Please format your date as {from_datetime(now())}.')
    else:
        raise InvalidArgumentException(
            f'Invalid datetime {arg} given. Please format your date as {from_datetime(now())}.')

    return raid_datetime


async def send_file(filename, recipient, content=""):
    file = discord.File(filename)
    await recipient.send(content=content, file=file)


async def delete_bot_messages(client, text_channel):
    is_me = lambda msg: msg.author == client.id
    await text_channel.purge(check=is_me)


async def update_raids(client):
    events_channel = get_channel(client, EVENTS_CHANNEL)
    raid_helper = get_bot(client, RAID_HELPER_BOT)
    async for message in events_channel.history():
        if message.author == raid_helper:
            rhm = RaidHelperMessage(message)
            rhm.to_raid().save()


async def update_datastores(client):
    await update_raids(client)
    update_whitelisted(client)


def get_roster_embed(client, rosters, raid):
    roster_formatter = RosterFormatter(client, raid, rosters)
    return roster_formatter.roster_to_embed()


def officer_rank(client, author):
    return check_authority(client, author, OFFICER_RANK)


def anyone(*args):
    return True


def check_authority(client, author, required_rank):
    member = get_user_by_id(client, author.id)
    if required_rank not in [role.name for role in member.roles]:
        raise NotAuthorizedException(author, required_rank)
