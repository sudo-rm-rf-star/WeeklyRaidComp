import random
from InputReader import read_signups
from CharacterSet import CharacterSet
from Constants import expected_raid_size, min_per_role, max_per_role, max_per_class_role, max_per_class_role, out_filename, color_per_class
import xlsxwriter

class Roster:
    def __init__(self, signups):
        random.shuffle(signups)  # Introduce some randomness
        self.attendees = CharacterSet()
        self.standby = CharacterSet()
        self.undecided = signups
        self.desperate_roles = []
        self.cur_raid_size = 0

    def make_roster(self):
        self._process_undecided()
        self._process_desperate_roles()
        self._process_undecided()
        for char in self.undecided:
            self.standby.add(char)

    def _process_undecided(self):
        tmp_undecided = []
        while len(self.undecided) > 0 and self.cur_raid_size < expected_raid_size:
            signup = self.undecided.pop(0)
            should_pick = self._evaluate(signup)
            if should_pick:
                role = signup.role
                if role in self.desperate_roles and self.attendees.role_count(role) >= min_per_role[role]:
                    self.desperate_roles.remove(role)
                self.attendees.add(signup)
                self.cur_raid_size += 1
            else:
                # Delay decision of bench until the desperate roles have been decided. This allows us to make a safe and
                # final vote whether we want to bench someone based on any roles for which players are lacking.
                if not(len(self.desperate_roles)):
                    tmp_undecided.append(signup)
                else:
                    self.standby.add(signup)
        self.undecided.extend(tmp_undecided)

    def _process_desperate_roles(self):
        for role, min_role_count in min_per_role.items():
            if self.attendees.role_count(role) < min_per_role[role]:
                self.desperate_roles.append(role)

    def write_roster(self):
        workbook = xlsxwriter.Workbook(out_filename)
        worksheet = workbook.add_worksheet()
        worksheet.set_column(0, 3, 25)

        def _write_heading(col_num, val):
            cell_format = workbook.add_format()
            cell_format.set_bold()
            cell_format.set_bottom()
            worksheet.write(0, col_num, val.capitalize(), cell_format)

        def _write_cell(row_num, col_num, color, val):
            cell_format = workbook.add_format()
            cell_format.set_left()
            cell_format.set_right()
            cell_format.set_bg_color(color)
            worksheet.write(row_num, col_num, val.capitalize(), cell_format)

        def _write_attendees_per_class(col_num, attendees_per_class, row_num=1):
            for clss, attendees in attendees_per_class.items():
                color = color_per_class[clss]
                for attendee in attendees:
                    _write_cell(row_num, col_num, color, attendee.charname.capitalize())
                    row_num += 1
            return row_num

        for col_num, role in enumerate(['tank', 'healer', 'dps']):
            row_count = _write_attendees_per_class(col_num, self.attendees.characters_per_role_and_class[role])
            _write_heading(col_num, f"{role} ({row_count - 1})")

        col_num = 3
        row_num = 1
        _write_heading(col_num, "standby")
        for attendees_per_class in self.standby.characters_per_role_and_class.values():
            row_num = _write_attendees_per_class(col_num, dict(sorted(attendees_per_class.items(), key=lambda x: x[0])), row_num)
        _write_heading(col_num, f"Standby ({row_num - 1})")

        workbook.close()

    def _evaluate(self, signup):
        if signup.event_status != 'Accepted':
            return False

        clss = signup.clss
        role = signup.role

        if role in self.desperate_roles:
            return True
        else:
            if self.attendees.role_class_count(role, clss) >= max_per_class_role[role][clss]:
                return False
            if self.attendees.role_count(role) >= max_per_role[role]:
                return False
            if not signup.is_kruisvaarder:
                return False
        return True

    def __str__(self):
        return str(self.attendees)


if __name__ == '__main__':
    signups = read_signups()
    roster = Roster(signups)
    roster.make_roster()
    roster.write_roster()
