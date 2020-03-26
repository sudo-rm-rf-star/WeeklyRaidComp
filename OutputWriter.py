import xlsxwriter
from Constant import color_per_class, out_filename


def write_roster(attendees, standby):
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

    def _write_characters(col_num, characters):
        row_num = 0
        for clazz, chars in characters.groupby('class'):
            color = color_per_class[clazz]
            for _, char in chars.iterrows():
                _write_cell(row_num+1, col_num, color, char['name'].capitalize())
                row_num += 1

    for col_num, role in enumerate(['tank', 'healer', 'dps']):
        _write_characters(col_num, attendees[attendees['role'] == role])
        _write_heading(col_num, f"{role}")

    col_num = 3
    _write_heading(col_num, "Standby")
    _write_characters(col_num, standby)

    workbook.close()
