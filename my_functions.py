from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidgetItem
from datetime import datetime
import pytz
import mysql.connector
from mysql.connector import Error
import re

import my_classes as myc
from credentials import configuration_crm as conf

# ......................... KONFIGURASYON DEGERLERI BASLAR .............................#
server_tz = "US/Pacific"


# ......................... KONFIGURASYON DEGERLERI BITER ..............................#
def create_connection(host_name, user_name, user_password, db_name):
    conn = None
    try:
        conn = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        # print("MySQL Database connection successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return conn


# Create a connection to the database
def open_conn():
    return create_connection(conf.host, conf.user, conf.password, conf.database)


# Find the last application period
def last_period():
    q0 = "SELECT BasvuruDonemi FROM form_basvuru WHERE ID = (SELECT MAX(ID) FROM form_basvuru)"
    return execute_read_query(open_conn(), q0)[0][0]


def write2table(page, list_headers, a_list):
    table_widget = page.tableWidget
    table_widget.clearContents()  # Clear table
    table_widget.setColumnCount(len(list_headers))  # Add title to table
    table_widget.setHorizontalHeaderLabels(list_headers)
    table_widget.setRowCount(len(a_list))  # Fill in the table

    for i, row in enumerate(a_list):
        for j, col in enumerate(row):
            if isinstance(col, datetime):
                item = QTableWidgetItem(col.strftime('%Y-%m-%d %H:%M:%S'))
                item.setData(Qt.ItemDataRole.UserRole, col)  # Store the datetime object
            else:
                item = QTableWidgetItem(str(col))
                if str(col).isdigit():
                    text = str(col)
                    item = myc.NumericItem(text)  # An example of a tableWidget class defined at the top of this page
                item.setData(Qt.ItemDataRole.UserRole, col)
            table_widget.setItem(i, j, item)
    return True


def remake_it_with_types(a_list):
    n_list = []
    n_row = []
    for i, row in enumerate(a_list):
        for j, col in enumerate(row):
            item = str(col).strip()  # with strip() method, we make maintenance to the data.
            if item.isdigit():
                item = int(item)
            elif is_valid_date_format(item):
                item = convert_server_time_to_local(item)
                item = datetime.strptime(item, "%Y-%m-%d %H:%M:%S")
                item = item.strftime(
                    "%Y.%m.%d %H:%M:%S")  # Activate it if u want to print datetime data in the format you want.
            n_row.append(item)
        n_list.append(n_row)
        n_row = []
        # print(n_list)
    return n_list


def convert_server_time_to_local(server_date, server_timezone=server_tz):
    """
    Sunucu zaman dilimindeki tarihi yerel zaman dilimine dönüştürür.

    :param server_date: Sunucu tarih (format: 'YYYY-MM-DD HH:MM:SS' veya datetime objesi)
    :param server_timezone: Sunucunun zaman dilimi (örn. 'America/New_York')
    :return: Yerel zaman diliminde formatlanmış tarih string'i
    """
    try:
        # Sunucu zaman dilimini al
        server_tz = pytz.timezone(server_timezone)

        # Eğer server_date string ise datetime'a dönüştür
        if isinstance(server_date, str):
            server_date = datetime.strptime(server_date, '%Y-%m-%d %H:%M:%S')

        # Sunucu tarihini server zaman dilimiyle yerelleştir
        server_date = server_tz.localize(server_date)

        # Yerel zaman dilimini al
        local_tz = datetime.now().astimezone().tzinfo

        # Sunucu zamanından yerel zamana dönüşüm
        local_date = server_date.astimezone(local_tz)

        # Yerel zamanı biçimlendir ve döndür
        return local_date.strftime('%Y-%m-%d %H:%M:%S')
    except ValueError as e:
        raise ValueError(f"Geçersiz tarih formatı: {e}")
    except pytz.exceptions.UnknownTimeZoneError:
        raise ValueError(f"Bilinmeyen zaman dilimi: {server_timezone}")


# This function is a datetime checker function. It checks a string value is datetime or not.
def is_valid_date_format(date_str):
    formats = [
        r'^\d{2}[./-]\d{2}[./-]\d{4}$',
        r'^\d{4}[./-]\d{2}[./-]\d{2}$',
        r'^\d{2}[./-]\d{2}[./-]\d{4} \d{2}[:.]\d{2}[:.]\d{2}$',
        r'^\d{4}[./-]\d{2}[./-]\d{2} \d{2}[:.]\d{2}[:.]\d{2}$',
        r'^\d{1}[./-]\d{2}[./-]\d{4}$',
        r'^\d{2}[./-]\d{1}[./-]\d{4}$',
        r'^\d{1}[./-]\d{1}[./-]\d{4}$',
        r'^\d{4}[./-]\d{2}[./-]\d{1}$',
        r'^\d{4}[./-]\d{1}[./-]\d{2}$',
        r'^\d{4}[./-]\d{1}[./-]\d{1}$',
        r'^\d{1}[./-]\d{2}[./-]\d{4} \d{2}[:.]\d{2}[:.]\d{2}$',
        r'^\d{2}[./-]\d{1}[./-]\d{4} \d{2}[:.]\d{2}[:.]\d{2}$',
        r'^\d{1}[./-]\d{1}[./-]\d{4} \d{2}[:.]\d{2}[:.]\d{2}$',
        r'^\d{4}[./-]\d{2}[./-]\d{1} \d{2}[:.]\d{2}[:.]\d{2}$',
        r'^\d{4}[./-]\d{1}[./-]\d{2} \d{2}[:.]\d{2}[:.]\d{2}$',
        r'^\d{4}[./-]\d{1}[./-]\d{1} \d{2}[:.]\d{2}[:.]\d{2}$',
    ]
    return any(re.match(pattern, date_str) for pattern in formats)


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


def convert_to_local_time(utc_date_str):
    # UTC tarihini oluştur
    utc_date = datetime.fromisoformat(utc_date_str)

    # UTC zaman dilimini oluştur
    utc_zone = pytz.UTC

    # UTC zaman dilimini belirle
    utc_date = utc_date.replace(tzinfo=utc_zone)

    # Sistem yerel zaman dilimini al
    local_tz = datetime.now().astimezone().tzinfo  # Yerel zaman dilimini otomatik olarak al

    # UTC'den yerel zamana dönüşüm
    local_date = utc_date.astimezone(local_tz)

    # Yerel zamanı biçimlendir ve döndür
    return local_date.strftime('%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    # Kullanım örneği
    # utc_date_string = '2024-08-04 07:54:28'
    # local_time = convert_to_local_time(utc_date_string)
    #
    # print(local_time)  # Sistem zaman dilimine bağlı olarak, örneğin: '2024-08-04 15:34:56'

    # Kullanım örneği
    try:
        server_time = "2024-08-04 11:33:32"
        server_timez = "US/Pacific"  # Sunucunun zaman dilimi
        local_time = convert_server_time_to_local(server_time, server_timez)
        print(f"Sunucu Zamanı ({server_timez}): {server_time}")
        print(f"Yerel Zaman: {local_time}")
    except ValueError as e:
        print(f"Hata: {e}")
