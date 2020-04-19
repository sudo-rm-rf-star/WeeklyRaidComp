import re
from src.exceptions.InvalidArgumentException import InvalidArgumentException
from src.common.Utils import to_date, to_datetime, from_datetime, from_date, now, today
from src.common.Constants import SUPPORTED_RAIDS


class ArgParser:
    def __init__(self, argformat):
        self.argformat = argformat

    def parse(self, args):
        """argformat specifies name and order of arguments. e.g. "raid_name player [team_index][raid_datetime]" """
        if args is None:
            return {}

        mandatory_argnames = parse_mandatory_args(self.argformat)
        optional_argnames = parse_optional_args(self.argformat)
        """Now hopefully we find the same arguments given by the user"""
        mandatory_args = parse_mandatory_args(args)
        optional_args = parse_optional_args(args)

        if len(mandatory_argnames) != len(mandatory_args):
            raise InvalidArgumentException(
                f"Expected {len(mandatory_argnames)} arguments, but found {len(mandatory_args)}.")

        optional_args += ['' for _ in range(len(optional_argnames) - len(optional_args))]

        return {argname: parse_argvalue(argname, argvalue) for argname, argvalue
                in zip(mandatory_argnames + optional_argnames, mandatory_args + optional_args)}


def parse_mandatory_args(args):
    return [arg for arg in re.findall(r'[^[]*', args)[0].split(' ') if arg]


def parse_optional_args(args):
    return [arg.strip('[]') for arg in re.findall(r'\[[^\]]*]', args)]


def parse_argvalue(argname, argval):
    if argval == '':
        return None

    argparser = {
        'raid_name': get_raidname,
        'raid_datetime': get_datetime,
        'team_index': get_roster_index
    }.get(argname, lambda _: argval)
    return argparser(argval)


def get_raidname(arg):
    raid_name = arg.lower()
    if raid_name not in SUPPORTED_RAIDS:
        raise InvalidArgumentException(f"Expected a valid raid: {', '.join(SUPPORTED_RAIDS)}")
    return raid_name


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


def get_roster_index(arg):
    try:
        return int(arg) - 1
    except ValueError:
        raise InvalidArgumentException(
            f'Invalid team index {arg} was given. Please pass a number.')
