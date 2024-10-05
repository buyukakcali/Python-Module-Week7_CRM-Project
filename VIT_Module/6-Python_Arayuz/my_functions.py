import re
from datetime import datetime
import bcrypt
import pytz
from PyQt6.QtCore import Qt, QSize, QObject
from PyQt6.QtGui import QFontMetrics, QFont, QColor
from PyQt6.QtWidgets import (QTableWidgetItem, QToolTip, QPushButton, QComboBox, QTableWidget, QDialog, QVBoxLayout,
                             QLabel, QHBoxLayout, QDateTimeEdit, QLineEdit, QInputDialog)

import my_classes as myc

cnf = myc.Config()


# This is the most complicated and important function, especially for styling and user-friendly interfaces
def handle_widget_styles(self_, widgets):
    """
    Verilen QPushButton ve QComboBox widget'ları arasında tıklanan widget'ın stilini değiştirir,
    önceki tıklanan widget'ın stilini eski haline getirir.

    Ayrıca, obje türüne göre (QPushButton, QComboBox, QToolTip) özel stil tanımlarını uygular.

    :param widgets: Stil değişikliği yapılacak QPushButton ve QComboBox widget'larının listesi
    :param self_: Formun kendisi (widget'ların ait olduğu form)
    """
    last_clicked_widget = None
    last_widget_original_style = "background-color: qlineargradient(spread:pad, x1:0.489, y1:1, x2:0.494, y2:0, stop:0 rgba(71, 71, 71, 255), stop:1 rgba(255, 255, 255, 255));"

    # Farklı obje türleri için stil tanımları
    push_button_style = """
        QPushButton {
            border-radius:15px;
            background-color:rgb(20, 135, 135);
            border:2px solid rgb(162, 0, 0);
        }
    """

    combo_box_style = """
        QComboBox {
            border-radius: 15px;
            background-color: rgb(25, 200, 200);
            color: rgb(255, 255, 255);
            padding: 1px 18px 1px 3px;
            background-color: rgb(20, 135, 135); /* QComboBox arka planı hover anında değişiyor */
            border: 2px solid rgb(162, 0, 0);
        }

        QComboBox:placeholder {
            padding-left: 10px;
            padding-right: 10px;
        }

        QComboBox::drop-down {
            border: none;
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 15px;
            border-left-width: 1px;
            border-left-color: darkgray;
            border-left-style: solid;
            border-top-right-radius: 3px;
            border-bottom-right-radius: 3px;
        }

        QComboBox::down-arrow {
            width: 14px;
            height: 14px;
        }

        QComboBox QAbstractItemView::item {
            background-color: rgb(25, 200, 200);
            color: rgb(255, 255, 255);
        }

        QComboBox QAbstractItemView {
            border: 1px solid darkgray;
            selection-background-color: rgb(20, 135, 135);
            background-color: rgb(25, 200, 200);
            border-radius: 15px;
        }

        QComboBox:hover {
            background-color: rgb(20, 135, 135); /* QComboBox arka planı hover anında değişiyor */
            border: 2px solid rgb(255, 80, 0); /* Hover ile kenar çizgisi ekleniyor */
        }

        QToolTip {
            border-radius: 15px;
            background-color: yellow; 
            color: black; 
            border: 1px solid black;
        }
    """

    global_style = """
        background-color: qlineargradient(spread:pad, x1:0.489, y1:1, x2:0.494, y2:0, stop:0 rgba(71, 71, 71, 255), stop:1 rgba(255, 255, 255, 255));
        color: white;
        QTableWidget { background-color: rgba(0, 0, 0,0%);}
        QToolTip {
            background-color: yellow;
            color: black;
            border: 1px solid black;
        }
    """

    # Changes the style of the clicked widget
    def on_widget_clicked(clicked_widget):
        nonlocal last_clicked_widget, last_widget_original_style

        form_name = self_.objectName()

        # Her bir form veya uzerindeki objelere gore spesifik tanimlamalar yapmak icin olusturulan alan
        if form_name == 'FormApplications':
            # Like __init__ function:
            # -----------------------
            # If you wanna run something at the initializing of the form, add here

            if clicked_widget == self_.form_applications.pushButtonBackMenu:
                pass

            elif clicked_widget == self_.form_applications.pushButtonExit:
                pass

        elif form_name == 'FormInterviews':
            # Like __init__ function:
            # -----------------------
            # If you wanna run something at the initializing of the form, add here

            # Bu kodlarda garip bir davranis tespit ettim. Eger disable fonksiyonu cagrilirsa hangi context menu
            # olduguna bakmaksizin context menu olusturmayi engelliyor. bu nedenle yaklasim olarak once disable
            # edilecek context menu varsa onu devre disi birakiyorum sonra da aktif etmek istedigimi enable
            # fonksiyonuyla cagiriyorum. Sanirim context menu olusturma veya devredisi birakma ile ilgili kullanilan
            # kodlar buna sebep oluyor.
            if clicked_widget == self_.form_interviews.pushButtonUnassignedApplicants:
                disable_cell_entered_signal_f(self_.form_interviews, self_.on_cell_entered)
                disable_context_menu(self_.form_interviews, self_.show_context_menu_add_to_candidates)  # once disable
                enable_context_menu(self_.form_interviews, self_.show_context_menu_assign_mentor)  # sonra enable

                # tableWidget line coloring process
                # The called function paints the background of the records with the specified color.
                highlight_candidates(self_.form_interviews, 23, 1, 'white', QColor("#FF5733"))

                # If the applicant is determined as a candidate, it is available under the tableWidget in the form and
                # serves an informative function.
                self_.form_interviews.labelInfo1.show()
                self_.form_interviews.labelInfo1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self_.form_interviews.labelInfo1.setToolTip('Mulakat zamani atanmis basvuranlari gosterir')
                self_.form_interviews.labelInfo1.setStyleSheet("""
                                    QLabel { background-color: "#FF5733"; color: white; border-radius : 5px; padding: 10px; }
                                    QToolTip { background-color: yellow; color: black; border: 1px solid black; }
                                    """)

            elif clicked_widget == self_.form_interviews.pushButtonAssignedApplicants:
                self_.form_interviews.labelInfo1.close()

            elif clicked_widget == self_.form_interviews.pushButtonInterviewedApplicants:
                self_.form_interviews.labelInfo1.close()
                disable_cell_entered_signal_f(self_.form_interviews, self_.on_cell_entered)
                disable_context_menu(self_.form_interviews, self_.show_context_menu_assign_mentor)  # once disable
                enable_context_menu(self_.form_interviews, self_.show_context_menu_add_to_candidates)  # sonra enable

                # tableWidget line coloring process
                # The function called shows the records determined as candidates with colored lines
                highlight_candidates(self_.form_interviews, 12, 1, 'white', QColor(123, 104, 238))

                highlight_candidates(self_.form_interviews, 12, 2, 'white', QColor(123, 104, 238))

                # If the applicant is determined as a candidate, it is available under the tableWidget in the form and
                # serves an informative function.
                self_.form_interviews.labelInfo1.show()
                self_.form_interviews.labelInfo1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self_.form_interviews.labelInfo1.setToolTip('Aday olarak belirlenmis basvuranlari gosterir')
                self_.form_interviews.labelInfo1.setStyleSheet("""
                    QLabel { background-color: rgb(123,104,238); color: white; border-radius : 5px; padding: 10px; }
                    QToolTip { background-color: yellow; color: black; border: 1px solid black; }
                    """)

            elif clicked_widget == self_.form_interviews.pushButtonBackMenu:
                pass

            elif clicked_widget == self_.form_interviews.pushButtonExit:
                pass

            else:
                re_enable_cell_entered_signal_f(self_.form_interviews, self_.on_cell_entered)
                disable_context_menu(self_.form_interviews, self_.show_context_menu_add_to_candidates)  # hep disable
                disable_context_menu(self_.form_interviews, self_.show_context_menu_assign_mentor)  # hep disable

                # Close labelInfo1 label.
                self_.form_interviews.labelInfo1.close()

        elif form_name == 'FormCandidates':
            # Like __init__ function:
            # -----------------------
            # If you wanna run something at the initializing of the form, add here

            if clicked_widget == self_.form_candidates.pushButtonGetCandidates:
                disable_cell_entered_signal_f(self_.form_candidates, self_.on_cell_entered)
                disable_context_menu(self_.form_candidates, self_.show_context_menu_add_remove_trainees)  # once disable
                enable_context_menu(self_.form_candidates, self_.show_context_menu_assign_mentor)  # sonra enable

                # tableWidget line coloring process
                # The function called shows the records with colored background for displaying INTERVIEW DETERMINED
                highlight_candidates(self_.form_candidates, 9, 2, 'white', 'orange')

                # If a project homework e-mail has been sent to the candidate, it is located under the table widget in
                # the form and serves an informative function.
                self_.form_candidates.labelInfo1.show()
                self_.form_candidates.labelInfo1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self_.form_candidates.labelInfo1.setToolTip(
                    'Proje odev maili gonderilmis ve mulakat tarihi belirlenmis adaylari gosterir')
                self_.form_candidates.labelInfo1.setStyleSheet("""
                                                QLabel { background-color: orange; color: white; border-radius : 5px; padding: 10px; }
                                                QToolTip { background-color: yellow; color: black; border: 1px solid black; }
                                                """)

            elif clicked_widget == self_.form_candidates.pushButtonInterviewedCandidates:
                self_.form_candidates.labelInfo1.close()
                disable_cell_entered_signal_f(self_.form_candidates, self_.on_cell_entered)
                disable_context_menu(self_.form_candidates, self_.show_context_menu_assign_mentor)  # once disable
                enable_context_menu(self_.form_candidates, self_.show_context_menu_add_remove_trainees)  # sonra enable

                # tableWidget line coloring process
                # The function called shows the records with colored background for displaying INTERVIEW DETERMINED
                highlight_candidates(self_.form_candidates, 14, 1, 'white', 'green')

                # If a project homework e-mail has been sent to the candidate, it is located under the table widget in
                # the form and serves an informative function.
                self_.form_candidates.labelInfo1.show()
                self_.form_candidates.labelInfo1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self_.form_candidates.labelInfo1.setToolTip('Kursiyer olarak atanmis kayitlari gosterir')
                self_.form_candidates.labelInfo1.setStyleSheet("""
                                                                QLabel { background-color: rgb(0, 170, 0); color: white; border-radius : 5px; padding: 10px; }
                                                                QToolTip { background-color: yellow; color: black; border: 1px solid black; }
                                                                """)


            elif clicked_widget == self_.form_candidates.comboBoxTrainees:
                self_.form_candidates.labelInfo1.close()
                re_enable_cell_entered_signal_f(self_.form_candidates, self_.on_cell_entered)
                disable_context_menu(self_.form_candidates, self_.show_context_menu_assign_mentor)  # once disable

            elif clicked_widget == self_.form_candidates.pushButtonBackMenu:
                pass

            elif clicked_widget == self_.form_candidates.pushButtonExit:
                pass

            else:
                # disable_context_menu(form.form_candidates, form.show_context_menu_add_to_candidates)  # hep disable
                disable_context_menu(self_.form_candidates, self_.show_context_menu_assign_mentor)  # hep disable
                self_.form_candidates.labelInfo1.close()


        else:  # Else for form names. (FormCandidates, FormApplications etc.)
            pass

        # Önceki tıklanan widget'ın stilini geri yükle
        if last_clicked_widget:
            last_clicked_widget.setStyleSheet(last_widget_original_style)

        # Tıklanan widget'ın mevcut stilini sakla
        last_widget_original_style = clicked_widget.styleSheet()

        # Widget türüne göre stil uygula
        if isinstance(clicked_widget, QPushButton):
            clicked_widget.setStyleSheet(push_button_style)
        elif isinstance(clicked_widget, QComboBox):
            clicked_widget.setStyleSheet(combo_box_style)

        # Tıklanan widget'ı güncelle
        last_clicked_widget = clicked_widget

    # Tüm widget'lara sinyal bağla
    for widget in widgets:
        if isinstance(widget, QPushButton):
            widget.clicked.connect(lambda checked, w=widget: on_widget_clicked(w))
        elif isinstance(widget, QComboBox):
            widget.activated.connect(lambda index, w=widget: on_widget_clicked(w))

    # Global stili buradan uygula
    self_.setStyleSheet(global_style)


# Finds the last application period
def last_period():
    try:
        q0 = ("SELECT " + cnf.applicationTableFieldNames[3] + " FROM " + cnf.applicationTable + " " +
              "WHERE " + cnf.applicationTableFieldNames[0] + " = (SELECT MAX(" + cnf.applicationTableFieldNames[
                  0] + ") " +
              "FROM " + cnf.applicationTable + ")")
        return execute_read_query(cnf.open_conn(), q0)[0][0]
    except Exception as e:
        raise Exception(f"Error occurred in last_period function: {e}")


# Search function for all modules
def search(filtering_list: list, headers: list, filtering_column: int, searched_text: str):
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


# Function used to write data to QTableWidget objects
def write2table(form, headers: list, a_list: list):
    try:
        table_widget = form.tableWidget
        table_widget.clearContents()  # Clear table
        table_widget.setColumnCount(len(headers))  # Add title to table
        table_widget.setHorizontalHeaderLabels(headers)
        table_widget.setRowCount(len(a_list))  # Fill in the table

        for i, row in enumerate(a_list):
            for j, col in enumerate(row):
                if isinstance(col, datetime):
                    item = str(col).strip()  # with strip() method, we make maintenance to the data.
                    item = convert_server_time_to_local(item)
                    col = datetime.strptime(item, "%Y-%m-%d %H:%M:%S")
                    item = QTableWidgetItem(col.strftime('%Y-%m-%d %H:%M:%S'))
                    item.setData(Qt.ItemDataRole.UserRole, col)  # Store the datetime object
                else:
                    item = QTableWidgetItem(str(col))
                    if str(col).isdigit():
                        text = str(col)
                        item = myc.NumericItem(
                            text)  # An example of a tableWidget class defined at the top of this page
                    item.setData(Qt.ItemDataRole.UserRole, col)
                table_widget.setItem(i, j, item)
                resize_columns(table_widget)
        return True
    except Exception as e:
        raise Exception(f"Error occurred in write2table function: {e}")


# Shows dialog what you want
def set_info_dialog(self_, header: str, message_text: str):
    dialog = QDialog(self_)
    dialog.setWindowTitle(header)

    # Stil ayarlarını QToolTip görünümüne benzer hale getirin
    dialog.setStyleSheet("""
            QDialog {
                background-color: yellow;
                border: 1px solid black;
            }
            QLabel {
                color: black;
                background-color: rgb(0, 0, 0, 0);
                font-size: 14px;
            }
            QPushButton:hover{
                background-color: rgb(20, 135, 135);
                border: 2px solid rgb(255, 80, 0);
            }
            QToolTip {
                background-color: yellow;
                color: black;
                border: 1px solid black;
            }
        """)

    layout = QVBoxLayout(dialog)

    # Bilgi mesajını ekle
    info_label = QLabel(message_text)
    layout.addWidget(info_label)

    # Kapat butonunun genişliğini sınırlamak için maksimum genişliği ayarlayın
    close_button = QPushButton("Close")
    close_button.setMaximumWidth(150)  # Maksimum genişliği 150 piksel ile sınırlıyoruz

    # noinspection PyUnresolvedReferences
    close_button.clicked.connect(dialog.close)

    # Butonu ortalamak için bir QHBoxLayout oluşturun
    button_layout = QHBoxLayout()
    button_layout.addStretch()  # Sol tarafa boşluk ekler
    button_layout.addWidget(close_button)  # Butonu ortalar
    button_layout.addStretch()  # Sağ tarafa boşluk ekler
    layout.addLayout(button_layout)  # Ana layout'a buton layout'unu ekle

    dialog.setLayout(layout)
    dialog.exec()


# It is only used within the write2table function and ensures that all tables appear properly.
def resize_columns(table_widget: QTableWidget):
    try:
        # Otomatik olarak sütun genişliklerini içeriğe göre ayarla: bu headers i de kontrol eder: Alternatif kod
        table_widget.resizeColumnsToContents()

        # Sadece contente gore sutun genisligini ayarlar. headers dikkate alinmaz!
        # resize_columns_by_content_only(table_widget)
    except Exception as e:
        raise Exception(f"Error occurred in resize_columns function: {e}")


# Makes the tableWidget (i.e. data) appear properly based on the content only (header is ignored)
def resize_columns_by_content_only(table_widget: QTableWidget):
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


# Function that provides a neat appearance when opening context menus
def auto_resize_dialog_window_for_table(dialog: QDialog, table_widget: QTableWidget):
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


# It is a function that returns a new copy of the data retrieved from the database in the correct data type.
# Not required for currently available data
def remake_it_with_types(a_list: list):
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
                    # # It is disabled here because it is integrated into the write2table function later.
                    # item = convert_server_time_to_local(item)
                    col = datetime.strptime(item, "%Y-%m-%d %H:%M:%S")
                n_row.append(col)
                # print('n_row: ', n_row)
            n_list.append(n_row)
            n_row = []
            # print('n_list: ', n_list)
        return n_list
    except Exception as e:
        raise Exception(f"Error occurred in remake_it_with_types function: {e}")


# Colors rows in tableWidget objects according to parameter values
def highlight_candidates(form, control_column: int, control_value: int, text_color: str or QColor,
                         background_color: str or QColor):
    try:
        # Get number of rows and columns of table in desired form
        row_count = form.tableWidget.rowCount()
        column_count = form.tableWidget.columnCount()

        # form_candidates tablosundaki her satırı kontrol et
        for row in range(row_count):
            # Get crm_IsApplicantACandidate data in column control_column
            crm_id_item = form.tableWidget.item(row, control_column)
            # If crm_id_item meets the condition, paint the background and text color
            if crm_id_item:
                if int(crm_id_item.text()) == control_value:
                    for col in range(column_count):
                        item = form.tableWidget.item(row, col)
                        if item:  # Eğer item mevcutsa
                            # Stilleri zorla ayarla
                            item.setBackground(QColor(background_color))  # Arka plan rengini ayarla
                            item.setForeground(QColor(text_color))  # Yazı rengini ayarla

                            # Stil özelliğini zorlamak için stil sayfası kullan
                            # item.setStyle(f"background-color: {background_color}; color: {text_color};")

    except Exception as e:
        raise Exception(f"Error occurred in highlight_candidates function: {e}")


# It synchronizes the server-time where the DB is located with the time when the application is used.
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
def is_valid_date_format(date_str: str):
    try:
        date_str = str(date_str)  # If the parameter is not a string, first convert it to string type
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


def convert_to_local_time(utc_date_str: str):
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


def filter_active_options(a_list: list, filtering_column: int):
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


def filter_table_f(form, headers: list, filtering_list: list, filtering_column: int):
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


def execute_write_query(conn, query: str, args: tuple = None):
    if conn:
        cursor = conn.cursor()
    else:
        print('There is no connection! Aborting...')
        return
    try:
        cursor.execute(query, args)
        affected_rows = cursor.rowcount  # Etkilenen satır sayısını alıyoruz
        conn.commit()
        conn.close()
        return affected_rows
    except Exception as e:
        conn.close()
        raise Exception(f"Error occurred in execute_query function: ") from e


def execute_read_query(conn, query: str, args: tuple = None):
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


# be able to add tooltips to these: QPushButton, QComboBox, QLabel, QLineEdit, QTableWidget, QDateTimeEdit, QInputDialog
def add_tooltip_to_any_form_object(obj: QObject, tooltip_text: str):
    """
    Verilen QPushButton veya QComboBox objesine bir tooltip ekler ve arka planını sarı yapar.

    :param obj: bir QPushButton veya QComboBox nesnesi
    :param tooltip_text: Tooltip'te gösterilecek metin
    """
    try:
        if isinstance(obj, (QPushButton, QComboBox, QLabel, QLineEdit, QTableWidget, QDateTimeEdit, QInputDialog)):
            obj.setToolTip(tooltip_text)

            # Tooltip stilini ayarlayın
            QToolTip.setFont(QFont('SansSerif', 10))  # Tooltip yazı tipi ve boyutu
            style_sheet = obj.styleSheet()
            style_sheet = style_sheet + ("""
                QToolTip {
                    background-color: yellow;
                    color: black;
                    border: 1px solid black;
                }
            """)
            obj.setStyleSheet(style_sheet)
        else:
            raise TypeError("Object must be either a QPushButton or QComboBox\nOR you shuld add more control and codes")
    except Exception as e:
        raise Exception(f"Error occurred in add_tooltip_to_any_form_object function: {e}")


# Function for adding Tooltip to the header section of the QTableWidget object
def add_tooltip_to_header(table_widget: QTableWidget, column_index: int, tooltip_text: str):
    """
    Verilen sütun başlığına bir tooltip ekler.

    :param table_widget: QTableWidget nesnesi
    :param column_index: Tooltip eklenecek sütunun index'i
    :param tooltip_text: Tooltip'te gösterilecek metin
    """
    try:
        header_item = table_widget.horizontalHeaderItem(column_index)
        if header_item:
            header_item.setToolTip(tooltip_text)
    except Exception as e:
        raise Exception(f"Error occurred in add_tooltip_to_header function: {e}")


# This is a function specific to this project.
# The first object should be a combobox with items, the second should be a combobox for filtering.
def normalise_combo_boxes(objects: list, args: list = None):
    try:
        if isinstance(objects[0], QComboBox):
            objects[0].clear()
            objects[0].setPlaceholderText(args[0])
            objects[0].addItems([args[1], args[2]])

        if isinstance(objects[1], QComboBox):
            objects[1].clear()
            objects[1].setPlaceholderText("Filter Area")
    except Exception as e:
        raise Exception(f"Error occurred in normalise_combo_boxes function: {e}")


# Password hashing function by bcrypt
def hash_password(password: str):
    try:
        # Hash the password by generating a salt
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password
    except Exception as e:
        raise Exception(f"Error occurred in hash_password function: {e}")


# Password verification function
def check_password(password: str, hashed_password):
    try:
        # Verilen şifreyi hashleyerek karşılaştır
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    except Exception as e:
        raise Exception(f"Error occurred in check_password function: {e}")


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


def re_enable_cell_entered_signal_f(form, method):
    try:
        # Connect the cellEntered signal to re-enable on_cell_entered method
        form.tableWidget.cellEntered.connect(method)
    except TypeError:
        # Eğer sinyal zaten bağlıysa, hata oluşur; bu hatayı yok sayarız.
        pass
    except Exception as e:
        raise Exception(f"Error occurred in reenable_cell_entered_signal function: ") from e


# This code is written to make the contents appear briefly when hovering over the cell.
def on_cell_entered_f(form, row: int, column: int):
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
def on_cell_clicked_f(form, row: int, column: int):
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
    pass
    # # Kullanım örneği
    # # utc_date_string = '2024-08-04 07:54:28'
    # # local_time = convert_to_local_time(utc_date_string)
    # #
    # # print(local_time)  # Sistem zaman dilimine bağlı olarak, örneğin: '2024-08-04 15:34:56'
    #
    # # Kullanım örneği
    # try:
    #     server_time = "2024-08-04 11:33:32"
    #     server_timez = "US/Pacific"  # Sunucunun zaman dilimi
    #     local_time = convert_server_time_to_local(server_time, server_timez)
    #     print(f"Sunucu Zamanı ({server_timez}): {server_time}")
    #     print(f"Yerel Zaman: {local_time}")
    # except ValueError as e:
    #     print(f"Hata: {e}")
