import gspread
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (QWidget, QApplication, QToolTip, QMenu, QDialog, QVBoxLayout, QPushButton,
                             QTableWidget, QMessageBox)
from oauth2client.service_account import ServiceAccountCredentials

import my_functions as myf
from UI_Files.interviews_ui import Ui_FormInterviews
from my_classes import Config


class InterviewsPage(QWidget):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user  # Variable name is absolutely perfect for why it is here
        self.sort_order = {}  # Dictionary to keep track of sort order for each column
        self.open_appointments = None
        self.basvuran_ids = None
        self.event_ids = None  # Mentor atamasinda Attendee bilgilerinin sheet dosyasina yazilirken karsilastirma icin
        self.active_list = None
        self.filtering_column = 2
        self.headers = []
        self.filtering_list = []
        self.form_interviews = Ui_FormInterviews()
        self.form_interviews.setupUi(self)

        myf.write2table(self.form_interviews, self.headers, [])  # This code updates the tableWidget headers
        self.menu_admin = None
        self.menu_user = None

        # Google Drivedaki sheet dosyasına bağlanma
        self.google_sheet_name = 'IlkMulakat'  # Your Google Sheet name
        self.google_credentials_file = 'credentials/key.json'  # Your credentials file

        # Google Sheets API bağlantısını ayarla
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://spreadsheets.google.com/feeds",
                 "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(self.google_credentials_file, scope)
        self.client = gspread.authorize(creds)

        # Connect signals to slots
        self.form_interviews.lineEditSearch.textEdited.connect(self.search_name_live)
        self.form_interviews.lineEditSearch.returnPressed.connect(self.search_name)
        self.form_interviews.pushButtonUnassignedApllicants.clicked.connect(self.mentor_not_assigned_applicants)
        self.form_interviews.pushButtonBackMenu.clicked.connect(self.back_menu)
        self.form_interviews.pushButtonExit.clicked.connect(self.app_exit)

        # Connect the combobox signal
        self.normalise_combobox_assigned_applicants()
        self.form_interviews.comboBoxAssignedApplicants.currentIndexChanged.connect(self.mentor_assigned_applicants)

        # Connect the cellEntered signal to the on_cell_entered method
        self.form_interviews.tableWidget.cellClicked.connect(self.on_cell_clicked)

        # Connect the header's sectionClicked signal to the on_header_clicked method
        self.form_interviews.tableWidget.horizontalHeader().sectionClicked.connect(self.on_header_clicked)

        # This code enables mouse tracking on tableWidget. It is needed for all mouse activity options above!
        self.form_interviews.tableWidget.setMouseTracking(True)

    # Method to automatically adjust the display settings of the comboBoxAssignedApplicants object
    def normalise_combobox_assigned_applicants(self):
        self.form_interviews.comboBoxAssignedApplicants.clear()
        self.form_interviews.comboBoxAssignedApplicants.setPlaceholderText('Assigned Applicants')
        self.form_interviews.comboBoxAssignedApplicants.addItems(['Last Period', 'All Periods'])

    def search_name(self):
        # If the search field data changes, update self.filtering_list with the entire list
        if self.active_list:
            self.filtering_list = list(self.active_list)  # Assigned for filtering.

        if self.filtering_list:
            searched_applications = []
            for application in self.filtering_list:
                if (self.form_interviews.lineEditSearch.text().strip().lower() in application[
                    self.filtering_column].strip().lower()
                        and self.form_interviews.lineEditSearch.text().strip().lower() != ''):
                    searched_applications.append(application)
                elif self.form_interviews.lineEditSearch.text() == '':
                    searched_applications = list(self.active_list)

            # Make empty the search area
            self.form_interviews.lineEditSearch.setText('')

            if len(searched_applications) > 0:  # If the searched_people variable is not empty!
                self.filtering_list = searched_applications  # Assigned for filtering.
                # self.form_interviews.comboBoxFilterOptions.clear()
                # self.form_interviews.comboBoxFilterOptions.addItems(
                #     main.filter_active_options(self.filtering_list, self.filtering_column))
            else:
                # self.form_interviews.comboBoxFilterOptions.clear()  # clears the combobox
                no_application = ['Nothing Found!']
                [no_application.append('-') for i in range(len(self.headers) - 1)]
                searched_applications.append(no_application)
                self.filtering_list = searched_applications
            return myf.write2table(self.form_interviews, self.headers, self.filtering_list)

    def search_name_live(self):
        # If the search field data changes, update self.filtering_list with the entire list
        if self.active_list:
            self.filtering_list = list(self.active_list)  # Assigned for filtering.

        if self.filtering_list:
            searched_applications = []
            for application in self.filtering_list:
                if (self.form_interviews.lineEditSearch.text().strip().lower() in application[
                    self.filtering_column].strip().lower()
                        and self.form_interviews.lineEditSearch.text().strip().lower() != ''):
                    searched_applications.append(application)
                elif self.form_interviews.lineEditSearch.text() == '':
                    searched_applications = list(self.active_list)

            # Make empty the search area
            # self.form_interviews.lineEditSearch.setText('')

            if len(searched_applications) > 0:  # If the searched_people variable is not empty!
                self.filtering_list = searched_applications  # Assigned for filtering.
                # self.form_interviews.comboBoxFilterOptions.clear()
                # self.form_interviews.comboBoxFilterOptions.addItems(
                #     main.filter_active_options(self.filtering_list, self.filtering_column))
            else:
                # self.form_interviews.comboBoxFilterOptions.clear()  # clears the combobox
                no_application = ['Nothing Found!']
                [no_application.append('-') for i in range(len(self.headers) - 1)]
                searched_applications.append(no_application)
                self.filtering_list = searched_applications
            return myf.write2table(self.form_interviews, self.headers, self.filtering_list)

    def show_context_menu(self, pos):
        item = self.form_interviews.tableWidget.itemAt(pos)
        if item is None or self.form_interviews.tableWidget.rowCount() == 0:
            return  # Eğer geçerli bir öğe yoksa veya tablo boşsa, hiçbir şey yapma

        self.form_interviews.tableWidget.selectRow(item.row())

        context_menu = QMenu(self)
        show_appointments_action = context_menu.addAction("Assign Mentor")
        action = context_menu.exec(self.form_interviews.tableWidget.viewport().mapToGlobal(pos))

        if action == show_appointments_action:
            self.show_open_appointments()

    def show_open_appointments(self):
        cnf = Config()
        headers = ['Etkinlik ID', 'Mulakat Zamanı', 'Mentor Ad', 'Mentor Soyad', 'Mentor Mail', 'Gorev Adi', 'Aciklama',
                   'Lokasyon', 'Online Meeting Link']
        q1 = ("SELECT " + cnf.appointmentsTableFieldNames[0] + ", " + cnf.appointmentsTableFieldNames[2] +
              ", " + cnf.appointmentsTableFieldNames[3] + ", " + cnf.appointmentsTableFieldNames[4] +
              ", " + cnf.appointmentsTableFieldNames[5] + ", " + cnf.appointmentsTableFieldNames[6] +
              ", " + cnf.appointmentsTableFieldNames[7] + ", " + cnf.appointmentsTableFieldNames[8] +
              ", " + cnf.appointmentsTableFieldNames[9] + ", " + cnf.appointmentsTableFieldNames[10] + " " +
              "FROM " + cnf.appointmentsTable + " " +
              "WHERE " + cnf.appointmentsTableFieldNames[12] + " is null " +
              "ORDER BY " + cnf.appointmentsTableFieldNames[3] + " ASC")
        self.open_appointments = myf.execute_read_query(cnf.open_conn(), q1)
        self.open_appointments = myf.remake_it_with_types(self.open_appointments)
        self.event_ids = [row[1] for row in self.open_appointments]  # EventID'leri sakla

        dialog = QDialog(self)
        dialog.setWindowTitle("Açık Randevular")
        layout = QVBoxLayout(dialog)

        # Create a temporary QTableWidget to pass to write2table
        table_widget = QTableWidget()
        table_widget.setColumnCount(len(headers))
        table_widget.setHorizontalHeaderLabels(headers)
        table_widget.setRowCount(len(self.open_appointments))

        # Prepare the data for write2table
        appointments_list = [appointment[2:] for appointment in self.open_appointments]  # Exclude ID

        # Create a temporary object to hold the table widget
        class TempPage:
            def __init__(self, table_widget_example):
                self.tableWidget = table_widget_example

        temp_page = TempPage(table_widget)

        # Use write2table to populate the table
        myf.write2table(temp_page, headers, appointments_list)

        layout.addWidget(temp_page.tableWidget)

        close_button = QPushButton("Kapat")
        close_button.clicked.connect(dialog.close)
        layout.addWidget(close_button)

        dialog.setLayout(layout)

        # Randevu seçimi ve mentor atama işlemi
        temp_page.tableWidget.cellDoubleClicked.connect(self.on_appointment_selected)

        dialog.exec()

    def on_appointment_selected(self, row):
        appointment_id = self.open_appointments[row][0]
        event_id = self.open_appointments[row][1]
        self.assign_mentor(appointment_id, event_id)

    def assign_mentor(self, appointment_id, event_id):
        cnf = Config()
        reply = QMessageBox.question(self, 'Mentor Atama', 'Bu randevuya mentor atamak istiyor musunuz?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            # Seçili satırın BasvuranID'sini al
            current_row = self.form_interviews.tableWidget.currentRow()
            basvuran_id = self.basvuran_ids[current_row]  # BasvuranID'yi saklanan listeden al

            # Veritabanında güncelleme yap
            q1 = ("UPDATE " + cnf.appointmentsTable + " SET " + cnf.appointmentsTableFieldNames[12] + " = %s " +
                  "WHERE " + cnf.appointmentsTableFieldNames[0] + " = %s")
            myf.execute_query(cnf.open_conn(), q1, (basvuran_id, appointment_id))

            q2 = ("UPDATE " + cnf.applicationTable + " SET " + cnf.applicationTableFieldNames[18] + " = 1 WHERE "
                  + cnf.applicationTableFieldNames[3] + " = %s AND " + cnf.applicantTableFieldNames[0] + " = %s")
            myf.execute_query(cnf.open_conn(), q2, (myf.last_period(), basvuran_id))

            # Basvuranın adını, soyadını ve email'ini veritabanından çekip Google Sheet'e yazdırıyoruz.
            applicant_query = "SELECT Name, Surname, Email FROM form_applicant WHERE ID = %s"
            applicant_data = myf.execute_read_query(cnf.open_conn(), applicant_query, (basvuran_id,))
            attendee_name, attendee_surname, attendee_email = applicant_data[0]

            self.update_google_sheet(event_id, attendee_name, attendee_surname, attendee_email)

            QMessageBox.information(self, 'Başarılı', 'Mentor başarıyla atandı.')

            # Dialog'u kapat
            self.sender().parent().close()
            self.disable_assign_mentor_context_menu()
            # Tabloyu güncelle
            self.mentor_not_assigned_applicants()

    # Gspread kullanarak Google Sheets ile bağlantı kuran metot
    def update_google_sheet(self, event_id, attendee_name, attendee_surname, attendee_email):
        # Google Sheet dosyasını aç
        sheet = self.client.open(self.google_sheet_name).sheet1

        # Event ID sütunundaki tüm verileri al (Event ID'nin olduğu sütunun numarası 2)
        event_ids = sheet.col_values(2)

        # İlgili Event ID'nin olduğu satırı bul
        for idx, sheet_event_id in enumerate(event_ids):
            if sheet_event_id == event_id:
                # İlgili satırda, Attendee Name, Surname, ve Mail sütunlarını güncelle
                sheet.update_cell(idx + 1, 11, attendee_email)  # 11: Attendee Mail sütunu
                sheet.update_cell(idx + 1, 13, attendee_name)  # 13: Attendee Name sütunu
                sheet.update_cell(idx + 1, 14, attendee_surname)  # 14: Attendee Surname sütunu
                break
        else:
            print(f"Event ID {event_id} not found in the sheet.")

    def mentor_not_assigned_applicants(self):
        cnf = Config()
        self.disconnect_cell_entered_signal()
        self.normalise_combobox_assigned_applicants()

        self.headers = [
            "Zaman damgası", "Başvuru dönemi", "Adınız", "Soyadınız", "Mail adresiniz", "Telefon numaranız",
            "Posta kodunuz", "Yaşadığınız Eyalet", "Şu anki durumunuz",
            "Yakın zamanda başlayacak ITPH Cybersecurity veya Powerplatform Eğitimlerine katılmak ister misiniz",
            "Ekonomik durumunuz", "Şu anda bir dil kursuna devam ediyor musunuz?", "Yabancı dil seviyeniz [İngilizce]",
            "Yabancı dil seviyeniz [Hollandaca]", "Belediyenizden çalışma ile ilgili baskı görüyor musunuz?",
            "Başka bir IT kursu (Bootcamp) bitirdiniz mi?",
            "İnternetten herhangi bir IT kursu takip ettiniz mi (Coursera, Udemy gibi)",
            "Daha önce herhangi bir IT iş tecrübeniz var mı?",
            "Şu anda herhangi bir projeye dahil misiniz? (Öğretmenlik projesi veya Leerwerktraject v.s)",
            "IT sektöründe hangi bölüm veya bölümlerde çalışmak istiyorsunuz? (Birden fazla seçenek seçebilirsiniz)",
            "Neden VIT projesine katılmak istiyorsunuz? (Birden fazla seçenek seçebilirsiniz)",
            "Aşağıya bu projeye katılmak veya IT sektöründe kariyer yapmak için sizi harekete geçiren motivasyondan \n"
            "bahseder misiniz?"
        ]

        q1 = ("SELECT "
              "b." + cnf.applicationTableFieldNames[1] + ", b." + cnf.applicationTableFieldNames[2] +
              ", b." + cnf.applicationTableFieldNames[3] + ", a." + cnf.applicantTableFieldNames[2] +
              ", a." + cnf.applicantTableFieldNames[3] + ", a." + cnf.applicantTableFieldNames[4] +
              ", a." + cnf.applicantTableFieldNames[5] + ", a." + cnf.applicantTableFieldNames[6] +
              ", a." + cnf.applicantTableFieldNames[7] + ", b." + cnf.applicationTableFieldNames[4] +
              ", b." + cnf.applicationTableFieldNames[5] + ", b." + cnf.applicationTableFieldNames[6] +
              ", b." + cnf.applicationTableFieldNames[7] + ", b." + cnf.applicationTableFieldNames[8] +
              ", b." + cnf.applicationTableFieldNames[9] + ", b." + cnf.applicationTableFieldNames[10] +
              ", b." + cnf.applicationTableFieldNames[11] + ", b." + cnf.applicationTableFieldNames[12] +
              ", b." + cnf.applicationTableFieldNames[13] + ", b." + cnf.applicationTableFieldNames[14] +
              ", b." + cnf.applicationTableFieldNames[15] + ", b." + cnf.applicationTableFieldNames[16] +
              ", b." + cnf.applicationTableFieldNames[17] + " " +
              "FROM " + cnf.applicationTable + " b " +
              "INNER JOIN " + cnf.applicantTable + " a ON b." + cnf.applicationTableFieldNames[0] +
              " = a." + cnf.applicantTableFieldNames[0] + " " +
              "WHERE b." + cnf.applicationTableFieldNames[3] +
              " = %s AND b." + cnf.applicationTableFieldNames[18] + " = 0 " +
              "ORDER BY b." + cnf.applicationTableFieldNames[2] + " ASC")

        not_appointed = myf.execute_read_query(cnf.open_conn(), q1, (myf.last_period(),))

        # Rebuilds the list based on the data type of the cells.
        not_appointed = myf.remake_it_with_types(not_appointed)

        self.basvuran_ids = [row[0] for row in not_appointed]  # BasvuranID'leri sakla
        self.active_list = [row[1:] for row in not_appointed]  # BasvuranID hariç diğer verileri sakla

        # Applicants who have not been assigned a mentor
        myf.write2table(self.form_interviews, self.headers, self.active_list)

        # Context menu'yü sadece bu durumda aktifleştir
        self.enable_assign_mentor_context_menu()

    def mentor_assigned_applicants(self):
        cnf = Config()
        self.reenable_cell_entered_signal()
        self.headers = ['Mulakat Zamanı', 'Menti Ad', 'Menti Soyad', 'Menti Mail', 'Mentor Ad', 'Mentor Soyad',
                        'Mentor Mail', 'Gorev Adi', 'Aciklama', 'Lokasyon', 'Online Meeting Link', 'Response Status']
        q1 = ("SELECT "
              "b." + cnf.appointmentsTableFieldNames[3] + ", a." + cnf.applicantTableFieldNames[2] +
              ", a." + cnf.applicantTableFieldNames[3] + ", a." + cnf.applicantTableFieldNames[4] +
              ", b." + cnf.appointmentsTableFieldNames[4] + ", b." + cnf.appointmentsTableFieldNames[5] +
              ", b." + cnf.appointmentsTableFieldNames[6] + ", b." + cnf.appointmentsTableFieldNames[7] +
              ", b." + cnf.appointmentsTableFieldNames[8] + ", b." + cnf.appointmentsTableFieldNames[9] +
              ", b." + cnf.appointmentsTableFieldNames[10] + ", b." + cnf.appointmentsTableFieldNames[11] + " " +
              "FROM " + cnf.appointmentsTable + " b " +
              "INNER JOIN " + cnf.applicantTable + " a ON b." +
              cnf.appointmentsTableFieldNames[12] +
              " = a." + cnf.applicantTableFieldNames[0] + " " +
              "WHERE b." + cnf.applicantTableFieldNames[0] + " is not null " +
              "ORDER BY b." + cnf.appointmentsTableFieldNames[3] + " ASC")

        # burayi mulakat islemi olmus veya tarihi gecmis islemleri de sorgulamak icin oncekinin onune ekleyebiliriz.
        # boylece tum datayi gorebiliriz. aktif olan appointments uzerinde islem yapariz, gereksiz randevular gozukmez
        # ama ayni zamanda eski atamalari da gorebiliriz.
        q2 = ("SELECT "
              "b." + cnf.appointments_old_or_deletedTableFieldNames[5] + ", a." + cnf.applicantTableFieldNames[2] +
              ", a." + cnf.applicantTableFieldNames[3] + ", a." + cnf.applicantTableFieldNames[4] +
              ", b." + cnf.appointments_old_or_deletedTableFieldNames[6] +
              ", b." + cnf.appointments_old_or_deletedTableFieldNames[7] +
              ", b." + cnf.appointments_old_or_deletedTableFieldNames[8] +
              ", b." + cnf.appointments_old_or_deletedTableFieldNames[9] +
              ", b." + cnf.appointments_old_or_deletedTableFieldNames[10] +
              ", b." + cnf.appointments_old_or_deletedTableFieldNames[11] +
              ", b." + cnf.appointments_old_or_deletedTableFieldNames[12] +
              ", b." + cnf.appointments_old_or_deletedTableFieldNames[13] + " " +
              "FROM " + cnf.appointments_old_or_deletedTable + " b " +
              "INNER JOIN " + cnf.applicantTable + " a ON b." + cnf.appointments_old_or_deletedTableFieldNames[14] +
              " = a." + cnf.applicantTableFieldNames[0] + " " +
              "WHERE b." + cnf.appointments_old_or_deletedTableFieldNames[14] + " is not null " +
              "ORDER BY b." + cnf.appointments_old_or_deletedTableFieldNames[5] + " ASC")
        mentor_assigned_applicants = myf.execute_read_query(cnf.open_conn(), q1)

        # Tum basvuru donemlerinde -bir sekilde- mentor atanmis basvuranlari ve mentorlerini getir.
        if self.form_interviews.comboBoxAssignedApplicants.currentText() == 'All Periods':
            old_mentor_assigned_applicants = myf.execute_read_query(cnf.open_conn(), q2)
            mentor_assigned_applicants = old_mentor_assigned_applicants + mentor_assigned_applicants

        self.active_list = mentor_assigned_applicants
        # Applicants who have been assigned a mentor
        myf.write2table(self.form_interviews, self.headers, self.active_list)
        # Context menu'yü devre dışı bırak
        self.disable_assign_mentor_context_menu()

    def back_menu(self):
        if self.current_user[2] == "admin":
            from admin_menu import AdminMenuPage
            self.hide()
            self.menu_admin = AdminMenuPage(self.current_user)
            self.menu_admin.show()
        else:
            from menu import UserMenuPage
            self.hide()
            self.menu_user = UserMenuPage(self.current_user)
            self.menu_user.show()

    def app_exit(self):
        self.close()

    # .................................................................................................................#
    # .......................................... PRESENTATION CODES START .............................................#
    # .................................................................................................................#

    # This code is written to make the contents appear briefly when hovering over the cell.
    def on_cell_entered(self, row, column):
        # Get the text of the cell at the specified row and column
        item_text = self.form_interviews.tableWidget.item(row, column).text()

        # Show a tooltip with the cell text
        tooltip = self.form_interviews.tableWidget.viewport().mapToGlobal(
            self.form_interviews.tableWidget.visualItemRect(
                self.form_interviews.tableWidget.item(row, column)).topLeft())
        QToolTip.setFont(QFont("SansSerif", 10))
        QToolTip.showText(tooltip, item_text)

    # This code is for cell clicking
    # If you want to show a persistent tooltip with the cell text. You need to use this code.
    # I coded it for 'on_cell_clicked' method
    def on_cell_clicked(self, row, column):
        # Get the text of the clicked cell
        item_text = self.form_interviews.tableWidget.item(row, column).text()

        # Show a persistent tooltip with the cell text
        tooltip = self.form_interviews.tableWidget.viewport().mapToGlobal(
            self.form_interviews.tableWidget.visualItemRect(
                self.form_interviews.tableWidget.item(row, column)).topLeft())
        QToolTip.setFont(QFont("SansSerif", 10))
        QToolTip.showText(tooltip, item_text, self.form_interviews.tableWidget)

    # This code is for header clicking. This method sorts the data based on the column that was clicked
    def on_header_clicked(self, logical_index):
        # Get the current sort order for the clicked column
        current_order = self.sort_order.get(logical_index, None)

        # Toggle between ascending and descending order
        if current_order == Qt.SortOrder.AscendingOrder:
            new_order = Qt.SortOrder.DescendingOrder
        else:
            new_order = Qt.SortOrder.AscendingOrder

        # Update the sort order dictionary
        self.sort_order[logical_index] = new_order

        # Sort the table based on the clicked column and the new sort order
        self.form_interviews.tableWidget.sortItems(logical_index, order=new_order)

    def disconnect_cell_entered_signal(self):
        try:
            # Disconnect the cellEntered signal to disable on_cell_entered method
            self.form_interviews.tableWidget.cellEntered.disconnect(self.on_cell_entered)
        except TypeError:
            # Eğer sinyal zaten bağlantısı kesilmişse, hata oluşur; bu hatayı yok sayarız.
            pass

    def reenable_cell_entered_signal(self):
        try:
            # Connect the cellEntered signal to re-enable on_cell_entered method
            self.form_interviews.tableWidget.cellEntered.connect(self.on_cell_entered)
        except TypeError:
            # Eğer sinyal zaten bağlıysa, hata oluşur; bu hatayı yok sayarız.
            pass

    def enable_assign_mentor_context_menu(self):
        self.form_interviews.tableWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.form_interviews.tableWidget.customContextMenuRequested.connect(self.show_context_menu)

    def disable_assign_mentor_context_menu(self):
        self.form_interviews.tableWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        try:
            self.form_interviews.tableWidget.customContextMenuRequested.disconnect(self.show_context_menu)
        except TypeError:
            # Eğer bağlantı zaten kesilmişse, bu hatayı görmezden gel
            pass


# ........................................... Presentation Codes END ..................................................#


if __name__ == "__main__":
    app = QApplication([])
    main_window = InterviewsPage(('a', 'b', 'admin'))
    main_window.show()
    app.exec()
