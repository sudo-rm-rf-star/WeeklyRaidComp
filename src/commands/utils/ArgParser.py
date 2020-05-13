import re
from exceptions.InvalidArgumentException import InvalidArgumentException
from utils.Constants import SUPPORTED_RAIDS
from utils.DateOptionalTime import DateOptionalTime
from utils.Date import Date
from utils.Time import Time
from typing import Optional, Dict, Any, List


class ArgParser:
    def __init__(self, argformat: str):
        self.argformat = argformat
        self.mandatory_argnames = parse_mandatory_args(self.argformat)
        self.optional_argnames = parse_optional_args(self.argformat)
        self.argnames = self.mandatory_argnames + self.optional_argnames

    def parse(self, args: str) -> Dict[str, Any]:
        """argformat specifies name and order of arguments. e.g. "raid_name player [team_index][raid_datetime]" """
        if not args:
            return {}

        mandatory_args = parse_mandatory_args(args)
        optional_args = parse_optional_args(args)

        if len(self.mandatory_argnames) != len(mandatory_args):
            raise InvalidArgumentException(
                f"Expected {len(self.mandatory_argnames)} arguments, but found {len(mandatory_args)}.")

        optional_args += ['' for _ in range(len(self.optional_argnames) - len(optional_args))]

        kwargs = {argname: parse_argvalue(argname, argvalue) for argname, argvalue in zip(self.argnames, mandatory_args + optional_args)}
        if 'raid_date' in kwargs or 'raid_time' in kwargs:
            date = kwargs.get('raid_date', None)
            time = kwargs.get('raid_time', None)
            datetime = None if not date else DateOptionalTime(date, time)
            kwargs['raid_datetime'] = datetime
            del kwargs['raid_date']
            del kwargs['raid_time']
        return kwargs

    def get_example_args(self) -> str:
        example_args = self.argformat
        for argname in self.argnames:
            example_args = example_args.replace(argname, get_example(argname))
        return example_args


def parse_mandatory_args(args: str) -> List[str]:
    if args is None:
        return []
    return [arg.strip() for arg in re.findall(r'[^[]*', args)[0].split(' ') if arg]


def parse_optional_args(args: str) -> List[str]:
    if args is None:
        return []
    return [arg.strip('[] ') for arg in re.findall(r'\[[^\]]*]', args)]


def parse_argvalue(argname: str, argval: str) -> Optional[str]:
    if argval == '':
        return None

    argparser = {
        'raid_name': get_raidname,
        'raid_datetime': get_datetime,
        'raid_date': get_date,
        'raid_time': get_time,
        'team_index': lambda x: parse_int(x) - 1,
        'player': lambda x: x.capitalize(),
        'week_count_cutoff': parse_int
    }.get(argname, lambda _: argval)
    return argparser(argval)


def get_raidname(arg: str) -> str:
    raid_name = arg.lower()
    if raid_name not in SUPPORTED_RAIDS:
        raise InvalidArgumentException(f"Expected a valid raid: {', '.join(SUPPORTED_RAIDS)}")
    return raid_name


def get_date(arg: str) -> Date:
    return Date.from_string(arg)


def get_time(arg: str) -> Time:
    return Time.from_string(arg)


def get_datetime(arg: str) -> DateOptionalTime:
    return DateOptionalTime.from_string(arg)


def parse_int(arg: str) -> int:
    try:
        return int(arg)
    except ValueError:
        raise InvalidArgumentException(
            f'Invalid team index {arg} was given. Please pass a number.')


def get_example(argname: str) -> str:
    return {
        'raid_name': 'BWL',
        'raid_datetime': '20-04-2020 19:30',
        'raid_date': '20-04-2020',
        'raid_time': '19:30',
        'team_index': '1',
        'player': 'Dok',
        'week_count_cutoff': '4',
        'channel_name': 'raid-signups',
        'announcement': 'Goedenavond beste kruisvaarder!',
        'role': 'Kruisvaarder',
    }[argname]
