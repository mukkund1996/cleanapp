from cleanapp.config import COLUMNS_ITERABLE


def get_week(date):
    return date.isocalendar()[1]


def find_chore(sheets_df, date, person_name):
    week_no = get_week(date)
    try:
        chore_row = sheets_df.loc[week_no]
    except IndexError as e:
        raise (f'The week number of {week_no} is not found in the sheet.') from e

    for location in COLUMNS_ITERABLE:
        if person_name == chore_row[location].lower():
            return " ".join(location.split("_")).capitalize()


def update_value(sheet, sheet_df, date, person_name, value=1):
    week_no = get_week(date)
    try:
        sheet_df.at[week_no, person_name] = value
    except IndexError as e:
        raise (f'The week number of {week_no} is not found in the sheet.') from e

    update_sheet(sheet, sheet_df)


def format_cell_color(
        spreadsheet,
        cell,
        color=None
):
    color = {"backgroundColor": {"red": 0.0, "green": 0.0, "blue": 0.0}} if color is None else color
    spreadsheet.format(cell, format=color)


def update_sheet(sheet, updated_df):
    corrected_df = updated_df.copy()
    corrected_df.reset_index(level=0, inplace=True)
    sheet.update([corrected_df.columns.values.tolist()] + corrected_df.values.tolist())
