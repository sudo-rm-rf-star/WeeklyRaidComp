import xlsxwriter
from Constant import color_per_class, DEFAULT_COLOR
import os

raid_dir = 'data/raids/output'


class RosterWriter:
    def __init__(self, raid_name, raid_date):
        workbook = xlsxwriter.Workbook(filename=os.path.join(raid_dir, f'{raid_name}_{raid_date}.xlsx'))
        self.workbook = workbook
        self.workbook.set_properties({
            'title': f"{raid_name} {raid_date}"
        })

    def write_rosters(self, rosters):
        for i, roster in enumerate(rosters):
            self.write_roster(i, roster.signees)

        self.workbook.close()

    def write_roster(self, i, signees):
        worksheet = self.workbook.add_worksheet(f'Team {i+1}')
        worksheet.set_column(0, 4, 25)

        def write_heading(col_num, value):
            cell_format = self.workbook.add_format()
            cell_format.set_bold()
            cell_format.set_bottom()
            worksheet.write(0, col_num, value.capitalize(), cell_format)

        def write_cell(row_num, col_num, color, value):
            cell_format = self.workbook.add_format()
            cell_format.set_left()
            cell_format.set_right()
            cell_format.set_bg_color(color)
            worksheet.write(row_num, col_num, value.capitalize(), cell_format)

        def write_characters(col_num, characters):
            row_num = 0
            for clazz, chars in characters.groupby('class'):
                color = color_per_class[clazz]
                for _, char in chars.iterrows():
                    write_cell(row_num + 1, col_num, color, char['name'].capitalize())
                    row_num += 1

            color = DEFAULT_COLOR
            for _, char in characters[characters['class'].isnull()].iterrows():
                write_cell(row_num + 1, col_num, color, char['name'].capitalize())
                row_num += 1

        attendees = signees[signees['roster_status'] == 'Accepted']
        for col_num, role in enumerate(['tank', 'healer', 'dps']):
            write_characters(col_num, attendees[attendees['role'] == role].sort_values(by='name'))
            write_heading(col_num, f"{role}")

        col_num = 3
        bench = signees[signees['roster_status'] == 'Bench'].sort_values(by='class', na_position='last')
        write_heading(col_num, 'Bench')
        write_characters(col_num, bench)

        col_num = 4
        absent = signees[signees['roster_status'] == 'Absence']
        write_heading(col_num, 'Absence')
        write_characters(col_num, absent)

