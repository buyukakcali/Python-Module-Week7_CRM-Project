import gspread
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QApplication, QTableWidgetItem
from datetime import datetime
import mysql.connector
from mysql.connector import Error
import re

from oauth2client.service_account import ServiceAccountCredentials


# Class that allows operations to be performed by converting the type of data held in TableWidget cells to integer,
# which is its original type in string.
class NumericItem(QtWidgets.QTableWidgetItem):
    def __lt__(self, other):
        return (self.data(QtCore.Qt.ItemDataRole.UserRole) <
                other.data(QtCore.Qt.ItemDataRole.UserRole))


def create_connection(host_name, user_name, user_password, db_name):
    conn = None
    try:
        conn = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return conn


def execute_query(conn, query, args=None):
    cursor = conn.cursor()
    try:
        cursor.execute(query, args)
        conn.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_read_query(conn, query, args=None):
    cursor = conn.cursor()
    result = None
    try:
        cursor.execute(query, args)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")
        return result


# Database connection parameters
host = "durakokur.com"
user = "durakoku_fth"
password = "fbuyukakcali123"
database = "durakoku_crmv1.0"


# Create a connection to the database
def open_conn():
    return create_connection(host, user, password, database)


def connection_hub(credentials, table, worksheet_name):
    # Authentication information for accessing the Google Sheets API
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials, scope)
    client = gspread.authorize(creds)  # Sign in with authentication credentials
    worksheet = client.open(table).worksheet(worksheet_name)  # Access the worksheet
    return worksheet


def write2table(page, list_headers, a_list):
    table_widget = page.tableWidget
    table_widget.clearContents()  # Clear table
    table_widget.setColumnCount(len(list_headers))  # Add title to table
    table_widget.setHorizontalHeaderLabels(list_headers)
    table_widget.setRowCount(len(a_list))  # Fill in the table
    for i, row in enumerate(a_list):
        for j, col in enumerate(row):
            # with strip() method, we make maintenance to the data.
            # (If it is not made by "remake_it_with_types" function)
            item = QTableWidgetItem(str(col).strip())
            if item.text().isdigit():  #
                text = item.text()  #
                item = NumericItem(text)  # An example of a tableWidget class defined at the top of this page
            item.setData(QtCore.Qt.ItemDataRole.UserRole, col)
            table_widget.setItem(i, j, item)
    return True


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


def filter_active_options(a_list, filtering_column):
    option_elements = []
    for row in a_list:
        try:
            value = row[filtering_column]
            # print(f"Row: {row}, Value: {value}, Type: {type(value)}")  # Debug output
            option_elements.append(str(value).strip())
        except Exception as e:
            print(f"Error processing row {row}: {e}")  # Error output for debugging
            continue

    filter_options = list(set(option_elements))

    if filter_options:
        if filter_options[0].isdigit():
            filter_options = sorted(filter_options, key=int)
        else:
            filter_options.sort()
    return filter_options


def rearrange_the_list(a_list, column):
    data_list = []

    for row in a_list[1:]:
        if str(row[column]).isdigit():
            row[column] = int(row[column])
        data_list.append(row)

    rearranged_list = sorted(data_list, key=lambda x: x[column])
    rearranged_list.insert(0, a_list[0])
    return rearranged_list


def remake_it_with_types(a_list):
    n_list = []
    n_row = []
    for i, row in enumerate(a_list):
        for j, col in enumerate(row):
            item = str(col).strip()  # with strip() method, we make maintenance to the data.
            if item.isdigit():
                item = int(item)
            elif is_valid_date_format(item):
                item = datetime.strptime(item, "%Y-%m-%d %H:%M:%S")
                # item = item.strftime("%Y.%m.%d %H:%M:%S")  # Activate it if u want to print datetime data in the format you want.
            n_row.append(item)
        n_list.append(n_row)
        n_row = []
    return n_list


# This function is a datetime checker function. It checks a string value is datetime or not.
def is_valid_date_format(date_str):
    formats = [r'^\d{2}[./-]\d{2}[./-]\d{4}$',
               r'^\d{4}[./-]\d{2}[./-]\d{2}$',
               r'^\d{2}[./-]\d{2}[./-]\d{4} \d{2}[:.]\d{2}[:.]\d{2}$',
               r'^\d{4}[./-]\d{2}[./-]\d{2} \d{2}[:.]\d{2}[:.]\d{2}$',

               r'^\d{1}[.-/]\d{2}[.-/]\d{4}$',
               r'^\d{2}[.-/]\d{1}[.-/]\d{4}$',
               r'^\d{1}[.-/]\d{1}[.-/]\d{4}$',

               r'^\d{4}[.-/]\d{2}[.-/]\d{1}$',
               r'^\d{4}[.-/]\d{1}[.-/]\d{2}$',
               r'^\d{4}[.-/]\d{1}[.-/]\d{1}$',

               r'^\d{1}[.-/]\d{2}[.-/]\d{4} \d{2}[:.]\d{2}[:.]\d{2}$',
               r'^\d{2}[.-/]\d{1}[.-/]\d{4} \d{2}[:.]\d{2}[:.]\d{2}$',
               r'^\d{1}[.-/]\d{1}[.-/]\d{4} \d{2}[:.]\d{2}[:.]\d{2}$',

               r'^\d{4}[.-/]\d{2}[.-/]\d{1} \d{2}[:.]\d{2}[:.]\d{2}$',
               r'^\d{4}[.-/]\d{1}[.-/]\d{2} \d{2}[:.]\d{2}[:.]\d{2}$',
               r'^\d{4}[.-/]\d{1}[.-/]\d{1} \d{2}[:.]\d{2}[:.]\d{2}$',
               ]
    try:
        for i in formats:
            if re.match(i, date_str) is not None:
                return re.match(i, date_str) is not None
    except ValueError:
        return False

#     VARIABLES FOR EVERYWHERE
# Find the last application period
q0 = "SELECT BasvuruDonemi FROM form_basvuru WHERE ID = (SELECT MAX(ID) FROM form_basvuru)"
last_period = execute_read_query(open_conn(), q0)[0][0]


if __name__ == '__main__':
    from login import LoginPage
    app = QApplication([])
    window = LoginPage()
    window.show()
    app.exec()
