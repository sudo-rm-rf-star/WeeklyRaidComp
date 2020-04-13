import xlsxwriter
from Constant import color_per_class

out_filename = "data/roster.xlsx"


class RosterWriter:
    def __init__(self, raid_name, raid_date):
        workbook = xlsxwriter.Workbook(out_filename)
        workbook.set_properties({
            'title': f"{raid_name} {raid_date}"
        })
        worksheet = workbook.add_worksheet()
        worksheet.set_column(0, 4, 25)
        self.workbook = workbook
        self.worksheet = worksheet

    def write_heading(self, col_num, value):
        cell_format = self.workbook.add_format()
        cell_format.set_bold()
        cell_format.set_bottom()
        self.worksheet.write(0, col_num, value.capitalize(), cell_format)

    def write_cell(self, row_num, col_num, color, value):
        cell_format = self.workbook.add_format()
        cell_format.set_left()
        cell_format.set_right()
        cell_format.set_bg_color(color)
        self.worksheet.write(row_num, col_num, value.capitalize(), cell_format)

    def write_characters(self, col_num, characters):
        row_num = 0
        for clazz, chars in characters.groupby('class'):
            color = color_per_class[clazz]
            for _, char in chars.iterrows():
                self.write_cell(row_num + 1, col_num, color, char['name'].capitalize())
                row_num += 1

    def write_roster(self, signees):
        attendees = signees[signees['roster_status'] == 'Accepted']
        for col_num, role in enumerate(['tank', 'healer', 'dps']):
            self.write_characters(col_num, attendees[attendees['role'] == role])
            self.write_heading(col_num, f"{role}")

        col_num = 3
        bench = signees[signees['roster_status'] == 'Bench'].sort_values(by='class', na_position='last')
        self.write_heading(col_num, 'Bench')
        self.write_characters(col_num, bench)

        col_num = 4
        absent = signees[signees['roster_status'] == 'Absence']
        self.write_heading(col_num, 'Absence')
        self.write_characters(col_num, absent)

        self.workbook.close()
