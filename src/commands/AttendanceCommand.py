from src.commands.RosterCommand import RosterCommand
from src.common.Constants import OFFICER_RANK, WHITELISTED_RANK
from src.filehandlers.AttendanceReader import get_raid_attendance_history
from src.filehandlers.WhitelistedFileHandler import get_whitelisted
from datetime import timedelta, datetime


class AttendanceCommand(RosterCommand):
    def __init__(self):
        argformat = "[raid_name][week_count_cutoff]"
        required_rank = OFFICER_RANK
        subname = 'attendance'
        description = f'Toon attendance per {WHITELISTED_RANK}'
        super(AttendanceCommand, self).__init__(subname, description, argformat, required_rank)

    async def run(self, client, message, **kwargs):
        return await self._run(client, message, **kwargs)

    async def _run(self, client, message, raid_name, week_count_cutoff):
        if week_count_cutoff is None:
            week_count_cutoff = 52
        history_cutoff = datetime.now() - timedelta(days=week_count_cutoff * 7)
        presence_history, absence_history = get_raid_attendance_history(raid_name=raid_name, cutoff_date=history_cutoff)
        attendance = sorted([(player, len(presence_history.get(player, []))) for player in get_whitelisted()], key=lambda x: x[1])
        raid_text = '' if not raid_name else f'voor {raid_name.upper()} '
        header = f'**Opkomst van {WHITELISTED_RANK} {raid_text}de voorbije {week_count_cutoff} weken:**'
        content = ', '.join([f'{player}: {count}' for player, count in attendance])
        await message.channel.send(content=f'{header}\n{content}')
