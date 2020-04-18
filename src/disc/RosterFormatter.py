import discord
from datetime import datetime

from src.disc.ServerUtils import get_emoji
from src.common.Constants import signup_status_to_role_class, role_to_emoji_name, CALENDAR_EMOJI, \
    CLOCK_EMOJI, abbrev_to_full, WEEKDAYS, TEAM_EMOJI, MISSING_EMOJI, BENCH_EMOJI
from src.common.Utils import parse_name

EMPTY_FIELD = '\u200e'


class RosterFormatter:
    def __init__(self, client, raid_helper_msg, roster):
        self.client = client
        self.rhm = raid_helper_msg
        self.roster = roster
        self.char_to_choice = {parse_name(char): choice for char, choice in self.rhm.get_choice_per_signee().items()}
        self.char_to_role = {parse_name(char): role for char, role in self._char_to_role().items()}

    def roster_to_embed(self):
        embed = {'title': self.get_title(),
                 'description': self.get_description(),
                 'fields': self.get_fields(),
                 'footer': self.get_footer(),
                 'color': 2171428,
                 'type': 'rich'}
        return discord.Embed.from_dict(embed)

    def get_title(self):
        return f'{abbrev_to_full[self.rhm.get_short_title()]} op {WEEKDAYS[self.rhm.get_weekday()]}'

    def get_description(self):
        team_description = '' if self.roster.index is None else f'{self._get_emoji(TEAM_EMOJI)} Team {self.roster.index + 1}\n'
        return f'{team_description}{self._get_emoji(CALENDAR_EMOJI)} {self.rhm.get_date()}\n{self._get_emoji(CLOCK_EMOJI)} {self.rhm.get_time()}'

    def get_fields(self):
        return [
            self.format_role_field('tank'),
            self.format_role_field('healer'),
            _empty_field(),

            self.format_role_field('melee'),
            self.format_role_field('ranged'),
            _empty_field(),

            _empty_field(),
            _empty_field(),
            _empty_field(),

            self.format_bench_field(),
            self.format_missing_field()
        ]

    def get_footer(self):
        fmt = "%Y-%m-%d %H:%M:%S"
        now = datetime.now()
        return {'text': f'Created at: {now.strftime(fmt)}.Last updated at: {now.strftime(fmt)}'}

    def format_role_field(self, role):
        accepted_for_role = [char for char in self.roster.accepted if self.get_role_for_player(char) == role]
        emoji_and_player = {(self.get_emoji_for_player(signee), signee) for signee in accepted_for_role}
        signee_fields = '\n'.join([f"{emoji} **{player}**" for emoji, player in sorted(emoji_and_player)])

        emoji_name = role_to_emoji_name[role]
        value = f'{self._get_emoji(role_to_emoji_name[role])} **__{emoji_name}__** ({len(accepted_for_role)}):\n{signee_fields}'
        return _field(value)

    def format_bench_field(self):
        benched = self.roster.bench
        value = f'{self._get_emoji(BENCH_EMOJI)} **__{BENCH_EMOJI}__** ({len(benched)}): {", ".join(map(lambda x: f"**{x}**", benched))}'
        return _field(value, inline=False)

    def format_missing_field(self):
        missing_roles = self.roster.missing_roles
        if len(missing_roles.keys()) == 0:
            return _empty_field(inline=True)
        else:
            value = f'{self._get_emoji(MISSING_EMOJI)} **__{MISSING_EMOJI}__**: {", ".join([f"**{role.capitalize()}** ({count})" for role, count in missing_roles.items()])}'
            return _field(value, inline=True)

    def get_emoji_for_player(self, signee):
        emoji_name = self.char_to_choice[signee]
        return self._get_emoji(emoji_name)

    def get_role_for_player(self, signee):
        return self.char_to_role[signee]

    def _char_to_role(self):
        char_to_role = {}
        for signee, signup_choice in self.char_to_choice.items():
            char_to_role[signee] = signup_status_to_role_class[signup_choice][0]
        return char_to_role

    def _get_emoji(self, name):
        return get_emoji(self.client, name)


def _field(content, inline=True):
    return {'name': EMPTY_FIELD, 'value': content, 'inline': inline}


def _empty_field(inline=True):
    return _field(EMPTY_FIELD, inline)
