import re
from datetime import datetime

import pytz
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFontMetrics, QFont
from PyQt6.QtWidgets import QTableWidgetItem, QToolTip, QPushButton, QComboBox, QLineEdit

import my_classes as myc

cnf = myc.Config()


# Find the last application period
def last_period():
    try:
        q0 = ("SELECT " + cnf.applicationTableFieldNames[3] + " FROM " + cnf.applicationTable + " " +
              "WHERE " + cnf.applicationTableFieldNames[0] + " = (SELECT MAX(" + cnf.applicationTableFieldNames[0] + ") " +
              "FROM " + cnf.applicationTable + ")")
        return execute_read_query(cnf.open_conn(), q0)[0][0]
    except Exception as e:
        raise Exception(f"Error occurred in last_period function: {e}")


# Search function for all modules
def search(filtering_list, headers, filtering_column, searched_text):
    try:
        if filtering_list:
            searched_data = []

            # Search and find results
            for row in filtering_list:
                if (searched_text.strip().lower() in str(row[filtering_column]).strip().lower()
                        and searched_text.strip().lower() != ''):
                    searched_data.append(row)
                elif searched_text == '':
                    searched_data = list(filtering_list)

            if len(searched_data) > 0:  # If there are any found as a result of the search
                filtering_list = searched_data  # Assign as filtering list
            else:
                default_nothing_found = ['Nothing Found!']
                [default_nothing_found.append('-') for _ in range(len(headers) - 1)]
                searched_data.append(default_nothing_found)
                filtering_list = searched_data
        return filtering_list
    except Exception as e:
        raise Exception(f"Error occurred in search function: {e}")


def write2table(page, list_headers, a_list):
    try:
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
                resize_columns(table_widget)
        return True
    except Exception as e:
        raise Exception(f"Error occurred in write2table function: {e}")


def resize_columns(table_widget):
    try:
        # Otomatik olarak sütun genişliklerini içeriğe göre ayarla: bu headers i de kontrol eder: Alternatif kod
        table_widget.resizeColumnsToContents()

        # Sadece contente gore sutun genisligini ayarlar. headers dikkate alinmaz!
        # resize_columns_by_content_only(table_widget)


    except Exception as e:
        raise Exception(f"Error occurred in resize_columns function: {e}")


def resize_columns_by_content_only(table_widget):
    try:
        # Otomatik olarak sütun genişliklerini içeriğe göre ayarla: bu headers i de kontrol eder: Alternatif kod
        table_widget.resizeColumnsToContents()

        # Sütun sayısını al
        column_count = table_widget.columnCount()
        row_count = table_widget.rowCount()

        # Mevcut font ile metin genişliğini hesaplamak için QFontMetrics kullan
        font_metrics = QFontMetrics(table_widget.font())

        # Her sütunun genişliğini hesapla
        for col in range(column_count):
            max_width = 85  # Başlangıçta genişliği sıfır yap
            for row in range(row_count):
                # Her hücrenin içeriğini al
                item = table_widget.item(row, col)
                if item:
                    # Hücredeki metni al ve genişliğini hesapla
                    text = item.text()
                    text_width = font_metrics.horizontalAdvance(text)
                    max_width = max(max_width, text_width)

            # Sütun genişliğini en uzun metne göre ayarla, biraz boşluk bırakmak için +10 ekliyoruz
            table_widget.setColumnWidth(col, max_width + 10)
        # Otomatik olarak sütun genişliklerini içeriğe göre ayarla: bu headers i de kontrol eder: Alternatif kod
        table_widget.resizeColumnsToContents()
    except Exception as e:
        raise Exception(f"Error occurred in resize_columns_by_content_only function: {e}")


def auto_resize_window_for_table(dialog, table_widget):
    try:
        # Sütun ve satır sayısını al
        column_count = table_widget.columnCount()
        row_count = table_widget.rowCount()

        # Mevcut font ile metin genişliğini hesaplamak için QFontMetrics kullan
        font_metrics = QFontMetrics(table_widget.font())

        # Toplam genişliği tutmak için
        total_width = 0
        total_height = 0

        # Her sütunun genişliğini hesapla
        for col in range(column_count):
            max_width = 0  # Başlangıçta genişliği sıfır yap

            # Başlık genişliğini hesapla
            header_text = table_widget.horizontalHeaderItem(col).text()
            header_width = font_metrics.horizontalAdvance(header_text)
            max_width = max(max_width, header_width)

            # InterviewDatetime verisinin genişligini hesapla
            item = table_widget.item(0, 0)
            if item:
                # Hücredeki metni al ve genişliğini hesapla
                text = item.text()
                text_width = font_metrics.horizontalAdvance(text)
                max_width = max(max_width, text_width)

            # Sütun genişliğini en uzun metne göre ayarla, biraz boşluk bırakmak için +10 ekliyoruz
            table_widget.setColumnWidth(col, max_width + 10)
            total_width += max_width + 13

        # Satır yüksekliğini hesapla (her bir satır için varsayılan yükseklik)
        for row in range(row_count):
            total_height += table_widget.rowHeight(row)

        # Başlık yüksekliğini ekle
        total_height += table_widget.horizontalHeader().height()

        # Pencere genişliğini ve yüksekliğini ayarlama
        dialog.setFixedSize(QSize(total_width + 20, total_height + 70))
    except Exception as e:
        raise Exception(f"Error occurred in auto_resize_window_for_table function: {e}")


def handle_widget_styles(widgets, form):
    """
    Bu fonksiyon, verilen QPushButton ve QComboBox widget'ları arasında tıklanan widget'ın stilini değiştirir
    ve önceki tıklanan widget'ın orijinal stilini geri yükler.

    :param widgets: Stil değişikliği yapılacak QPushButton ve QComboBox widget'larının listesi
    """
    last_clicked_widget = None
    last_widget_original_style = ""

    # Tıklanan widget'ın stilini değiştir
    push_button_style_sheet = "border-radius:15px;background-color:rgb(20, 135, 135);border:3px solid rgb(162, 0, 0);"
    combo_box_style_sheet = "border-radius:15px;background-color:rgb(20, 135, 135);border:3px solid rgb(162, 0, 0);"

    def on_widget_clicked(clicked_widget):
        nonlocal last_clicked_widget, last_widget_original_style

        form_name = form.objectName()

        # Her bir form veya uzerindeki objelere gore spesifik tanimlamalar yapmak icin olusturulan alan
        if form_name == 'FormApplications':
            pass

        elif form_name == 'FormInterviews':
            # Bu kodlarda garip bir davranis tespit ettim. Eger disable fonksiyonu cagrilirsa hangi context menu
            # olduguna bakmaksizin context menu olusturmayi engelliyor. bu nedenle yaklasim olarak once disable
            # edilecek context menu varsa onu devre disi birakiyorum sonra da aktif etmek istedigimi enable
            # fonksiyonuyla cagiriyorum. Sanirim context menu olusturma veya devredisi birakma ile ilgili kullanilan
            # kodlar buna sebep oluyor.
            if clicked_widget == form.form_interviews.pushButtonUnassignedApplicants:
                disable_context_menu(form.form_interviews, form.show_context_menu_add_to_candidates)    # once disable
                enable_context_menu(form.form_interviews, form.show_context_menu_assign_mentor)         # sonra enable
            elif clicked_widget == form.form_interviews.pushButtonInterviewedApplicants:
                disable_context_menu(form.form_interviews, form.show_context_menu_assign_mentor)        # once disable
                enable_context_menu(form.form_interviews, form.show_context_menu_add_to_candidates)     # sonra enable
            else:
                disable_context_menu(form.form_interviews, form.show_context_menu_add_to_candidates)    # hep disable
                disable_context_menu(form.form_interviews, form.show_context_menu_assign_mentor)        # hep disable

            # If the applicant is determined as a candidate, it is available under the tableWidget in the form and
            # serves an informative function.
            if isinstance(clicked_widget, QPushButton):
                if clicked_widget == form.form_interviews.pushButtonInterviewedApplicants:
                    form.form_interviews.labelInfo1.show()
                    form.form_interviews.labelInfo1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    form.form_interviews.labelInfo1.setToolTip('Aday olarak belirlenmis basvuranlari gosterir')
                else:
                    form.form_interviews.labelInfo1.close()

        elif form_name == 'FormCandidates':
            pass

        # Eğer daha önce bir widget tıklandıysa, eski stiline döndür
        if last_clicked_widget:
            last_clicked_widget.setStyleSheet(last_widget_original_style)

        # Tıklanan widget'ın mevcut stilini sakla
        last_widget_original_style = clicked_widget.styleSheet()

        # Tıklanan widget'ın stilini değiştir
        if isinstance(clicked_widget, QComboBox):
            # QComboBox için varsayılan stil
            clicked_widget.setStyleSheet(combo_box_style_sheet)
        else:
            # QPushButton için varsayılan stil
            clicked_widget.setStyleSheet(push_button_style_sheet)

        # Tıklanan widget'ı güncelle
        last_clicked_widget = clicked_widget

    # QPushButton ve QComboBox'lara sinyal bağla
    for widget in widgets:
        if isinstance(widget, QPushButton):
            widget.clicked.connect(lambda checked, w=widget: on_widget_clicked(w))
        elif isinstance(widget, QComboBox):
            widget.activated.connect(lambda index, w=widget: on_widget_clicked(w))



# def handle_button_styles(buttons, default_style="border-radius: 15px; "
#                                      "background-color: rgb(20, 135, 135); "
#                                      "border: 2px solid rgb(162, 0, 0);"):
#     """
#     Bu fonksiyon, verilen butonlar arasında tıklanan butonun stilini değiştirir
#     ve önceki tıklanan butonun orijinal stilini geri yükler.
#
#     :param buttons: Stil değişikliği yapılacak butonların listesi
#     :param default_style: Tıklanan butona uygulanacak yeni stil (varsayılan olarak lightblue)
#     """
#     last_clicked_button = None
#     last_button_original_style = ""
#
#     def on_button_clicked(clicked_button):
#         nonlocal last_clicked_button, last_button_original_style
#
#         # Eğer daha önce bir buton tıklandıysa, eski stiline döndür
#         if last_clicked_button:
#             last_clicked_button.setStyleSheet(last_button_original_style)
#
#         # Tıklanan butonun mevcut stilini sakla
#         last_button_original_style = clicked_button.styleSheet()
#
#         # Tıklanan butonun stilini değiştir
#         clicked_button.setStyleSheet(default_style)
#
#         # Tıklanan butonu güncelle
#         last_clicked_button = clicked_button
#
#     # Butonlara sinyal bağla
#     for button in buttons:
#         button.clicked.connect(lambda checked, btn=button: on_button_clicked(btn))


def remake_it_with_types(a_list):
    try:
        n_list = []
        n_row = []
        for i, row in enumerate(a_list):
            for j, col in enumerate(row):
                try:
                    item = str(col).strip()  # with strip() method, we make maintenance to the data.
                    col = int(item)
                    # print(f"Bu bir integer! Değer: {item}")
                except ValueError:
                    pass
                    # print("Bu bir integer değil.")

                if is_valid_date_format(col):
                    item = str(col).strip()  # with strip() method, we make maintenance to the data.
                    item = convert_server_time_to_local(item)
                    col = datetime.strptime(item, "%Y-%m-%d %H:%M:%S")
                n_row.append(col)
                # print('n_row: ', n_row)
            n_list.append(n_row)
            n_row = []
            # print('n_list: ', n_list)
        return n_list
    except Exception as e:
        raise Exception(f"Error occurred in remake_it_with_types function: {e}")


def convert_server_time_to_local(server_date, server_timezone=cnf.server_tz):
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
    except ValueError as err:
        raise ValueError(f"Geçersiz tarih formatı: {err}")
    except pytz.exceptions.UnknownTimeZoneError:
        raise ValueError(f"Bilinmeyen zaman dilimi: {server_timezone}")


# This function is a datetime checker function. It checks a string value is datetime or not.
def is_valid_date_format(date_str):
    try:
        date_str = str(date_str)    # If the parameter is not a string, first convert it to string type
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
    except Exception as e:
        raise Exception(f"Error occurred in is_valid_date_format function: {e}")


def convert_to_local_time(utc_date_str):
    try:
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
    except Exception as e:
        raise Exception(f"Error occurred in convert_to_local_time function: {e}")


def filter_active_options(a_list, filtering_column):
    try:
        option_elements = []
        for row in a_list:
            try:
                value = row[filtering_column]
                # print(f"Row: {row},\n Value: {value}, Type: {type(value)}")  # Debug output
                option_elements.append(str(value).strip())
            except Exception as err:
                print(f"Error processing row {row}: {err}")  # Error output for debugging
                continue

        filter_options = list(set(option_elements))

        if filter_options:
            if filter_options[0].isdigit():
                filter_options = sorted(filter_options, key=int)
            else:
                filter_options.sort()
        return filter_options
    except Exception as e:
        raise Exception(f"Error occurred in filter_active_options function: {e}")


def filter_table_f(form, headers, filtering_list, filtering_column):
    try:
        filtered_data = []
        selected_item = form.comboBoxFilterOptions.currentText().strip()

        for row in filtering_list:
            if str(row[filtering_column]).strip().lower() == str(selected_item).strip().lower():
                filtered_data.append(row)

        if filtered_data and len(filtered_data) > 0:
            pass
        else:
            if filtering_list and len(filtering_list[0]) > 0:
                default_nothing_found = ['Nothing Found!']
                [default_nothing_found.append('-') for i in range(len(filtering_list[0]) - 1)]
                filtered_data.append(default_nothing_found)
            else:
                print("Filtering list is empty")
        return write2table(form, headers, filtered_data)
    except Exception as e:
        raise Exception(f"Error occurred in filter_table function: ") from e


def execute_query(conn, query, args=None):
    if conn:
        cursor = conn.cursor()
    else:
        print('There is no connection! Aborting...')
        return
    try:
        cursor.execute(query, args)
        conn.commit()
        # print("Query executed successfully")
        conn.close()
    except Exception as e:
        conn.close()
        raise Exception(f"Error occurred in execute_query function: ") from e


def execute_read_query(conn, query, args=None):
    if conn:
        cursor = conn.cursor()
    else:
        print('There is no connection! Aborting...')
        return

    result = None

    try:
        cursor.execute(query, args)
        result = cursor.fetchall()
        conn.close()
        return result
    except Exception as e:
        conn.close()
        print(f"Error occurred in execute_read_query function: {e}")
        return result


def enable_context_menu(form, context_menu):
    try:
        form.tableWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        form.tableWidget.customContextMenuRequested.connect(context_menu)
    except Exception as e:
        raise Exception(f"Error occurred in enable_context_menu function: ") from e


def disable_context_menu(form, context_menu):
    try:
        form.tableWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        form.tableWidget.customContextMenuRequested.disconnect(context_menu)
    except TypeError:
        # Eğer bağlantı zaten kesilmişse, bu hatayı görmezden gel
        pass
    except Exception as e:
        raise Exception(f"Error occurred in disable_context_menu function: ") from e


def disable_cell_entered_signal_f(form, method):
    try:
        # Disconnect the cellEntered signal to disable on_cell_entered method
        form.tableWidget.cellEntered.disconnect(method)
    except TypeError:
        # Eğer sinyal bağlantısı zaten kesilmişse, hata oluşur; bu hatayı yok sayarız.
        pass
    except Exception as e:
        raise Exception(f"Error occurred in disconnect_cell_entered_signal function: ") from e


def reenable_cell_entered_signal_f(form, method):
    try:
        # Connect the cellEntered signal to re-enable on_cell_entered method
        form.tableWidget.cellEntered.connect(method)
    except TypeError:
        # Eğer sinyal zaten bağlıysa, hata oluşur; bu hatayı yok sayarız.
        pass
    except Exception as e:
        raise Exception(f"Error occurred in reenable_cell_entered_signal function: ") from e


# This code is written to make the contents appear briefly when hovering over the cell.
def on_cell_entered_f(form, row, column):
    try:
        # Get the text of the cell at the specified row and column
        item_text = form.tableWidget.item(row, column).text()

        # Show a tooltip with the cell text
        tooltip = form.tableWidget.viewport().mapToGlobal(form.tableWidget.visualItemRect(
            form.tableWidget.item(row, column)).topLeft())
        QToolTip.setFont(QFont("SansSerif", 10))
        QToolTip.showText(tooltip, item_text)
    except Exception as e:
        raise Exception(f"Error occurred in on_cell_entered_f function: ") from e


# This code is for cell clicking
# If you want to show a persistent tooltip with the cell text. You need to use this function and its method together.
def on_cell_clicked_f(form, row, column):
    try:
        # Get the text of the clicked cell
        item_text = form.tableWidget.item(row, column).text()

        # Show a persistent tooltip with the cell text
        tooltip = form.tableWidget.viewport().mapToGlobal(form.tableWidget.visualItemRect(
            form.tableWidget.item(row, column)).topLeft())
        QToolTip.setFont(QFont("SansSerif", 10))
        QToolTip.showText(tooltip, item_text, form.tableWidget)
    except Exception as e:
        raise Exception(f"Error occurred in on_cell_clicked_f function: ") from e


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
