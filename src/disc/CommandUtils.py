import discord
from src.exceptions.NotAuthorizedException import NotAuthorizedException
from src.exceptions.InvalidArgumentException import InvalidArgumentException
from src.filehandlers.WhitelistedFileHandler import update_whitelisted
from src.common.Constants import BOT_NAME, RAID_HELPER_BOT, EVENTS_CHANNEL, OFFICER_RANK, SUPPORTED_RAIDS
from src.common.Utils import from_datetime, to_datetime, today, now, from_date, to_date
from src.disc.ServerUtils import get_guild, get_channel, get_bot, get_user_by_id
from src.disc.RaidHelperMessage import RaidHelperMessage
from src.disc.RosterFormatter import RosterFormatter


def get_roster_args(argv):
    """
    Always final two arguments of command. Raid name (mandatory), date and time (optional, default is upcoming)
    e.g "zg 31-01-2020 19:30"
    """
    raid_datetime = None
    if len(argv) in [1, 2, 3]:
        raid_name = argv[0].lower()

        if raid_name not in SUPPORTED_RAIDS:
            return InvalidArgumentException(f"Expected a valid raid: {', '.join(SUPPORTED_RAIDS)}")

        if len(argv) == 2:
            raid_date_arg = argv[1]
            try:
                raid_datetime = to_date(raid_date_arg)
            except ValueError:
                raise InvalidArgumentException(
                    f'Invalid date "{raid_date_arg}" was given. Please format your date as {from_date(today())}.')

        if len(argv) == 3:
            raid_datetime_arg = f'{argv[1]} {argv[2]}'
            try:
                raid_datetime = to_datetime(raid_datetime_arg)
            except ValueError:
                raise InvalidArgumentException(
                    f'Invalid datetime "{raid_datetime_arg}" was given. Please format your date as {from_datetime(now())}.')
    else:
        raise InvalidArgumentException("Expected a raid name and an optional raid date")

    return raid_name, raid_datetime


async def send_file(filename, recipient, content=""):
    file = discord.File(filename)
    await recipient.send(content=content, file=file)


async def delete_bot_messages(client, text_channel):
    guild = get_guild(client)
    bot = discord.utils.get(guild.members, name=BOT_NAME)
    async for message in text_channel.history():
        if message.author == bot:
            await message.delete()


async def send_roster(client, roster, raid):
    text_channel = get_channel(client, 'test')
    roster_formatter = RosterFormatter(client, raid, roster)
    embed = roster_formatter.roster_to_embed()
    await text_channel.send(embed=embed)


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


def officer_rank(client, author):
    return check_authority(client, author, OFFICER_RANK)


def anyone(*args):
    return True


def check_authority(client, author, required_rank):
    member = get_user_by_id(client, author.id)
    if required_rank not in [role.name for role in member.roles]:
        raise NotAuthorizedException(author, required_rank)
