import gspread
from PyQt6.QtWidgets import QApplication

from oauth2client.service_account import ServiceAccountCredentials


# def connection_hub(credentials, table, worksheet_name):
#     # Authentication information for accessing the Google Sheets API
#     scope = ['https://spreadsheets.google.com/feeds',
#              'https://www.googleapis.com/auth/drive']
#     creds = ServiceAccountCredentials.from_json_keyfile_name(credentials, scope)
#     client = gspread.authorize(creds)  # Sign in with authentication credentials
#     worksheet = client.open(table).worksheet(worksheet_name)  # Access the worksheet
#     return worksheet

def list_exclude(a_list, excluded_column_indexes):
    n_list = []
    for i, row in enumerate(a_list):
        item = []
        for j, col in enumerate(row):
            # if "column index" is inside our exclude list, come inside "if code block" and pass the loop.
            # don't add anything to item
            if j in excluded_column_indexes:
                continue
            # Otherwise add col to the item, which will become a row for new list
            item.append(col)
        n_list.append(item)  # add new item(row) to the new list
    return n_list


def rearrange_the_list(a_list, column):
    data_list = []

    for row in a_list[1:]:
        if str(row[column]).isdigit():
            row[column] = int(row[column])
        data_list.append(row)

    rearranged_list = sorted(data_list, key=lambda x: x[column])
    rearranged_list.insert(0, a_list[0])
    return rearranged_list


if __name__ == '__main__':
    from login import LoginPage

    app = QApplication([])
    window = LoginPage()
    window.show()
    app.exec()
