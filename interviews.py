from PyQt6.QtCore import Qt, QObject, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (QWidget, QApplication, QToolTip, QMenu, QDialog, QVBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QMessageBox, QComboBox)

import main
from UI_Files.interviews_ui import Ui_FormInterviews


class InterviewsPage(QWidget):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user  # Variable name is absolutely perfect for why it is here
        self.sort_order = {}  # Dictionary to keep track of sort order for each column
        self.open_appointments = None
        self.basvuran_ids = None
        self.active_list = None
        self.filtering_column = 2
        self.headers = []
        self.filtering_list = []
        self.form_interviews = Ui_FormInterviews()
        self.form_interviews.setupUi(self)

        main.write2table(self.form_interviews, self.headers, [])  # This code updates the tableWidget headers
        self.menu_admin = None
        self.menu_user = None

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

        # These codes are required to assign a mentor by right-clicking.
        self.form_interviews.tableWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.form_interviews.tableWidget.customContextMenuRequested.connect(self.show_context_menu)

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
            return main.write2table(self.form_interviews, self.headers, self.filtering_list)

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
            return main.write2table(self.form_interviews, self.headers, self.filtering_list)

    def show_context_menu(self, pos):
        # Tıklanan hücreyi bulun
        item = self.form_interviews.tableWidget.itemAt(pos)
        if item:
            # Tıklanan hücrenin satırını seçin
            self.form_interviews.tableWidget.selectRow(item.row())

        context_menu = QMenu(self)
        show_appointments_action = context_menu.addAction("Assign Mentor")
        action = context_menu.exec(self.form_interviews.tableWidget.mapToGlobal(pos))

        if action == show_appointments_action:
            self.show_open_appointments()

    def show_open_appointments(self):
        headers = ['Mulakat Zamanı', 'Mentor Ad', 'Mentor Soyad', 'Mentor Mail', 'Gorev Adi', 'Aciklama',
                   'Lokasyon', 'Online Meeting Link']
        q1 = ("SELECT "
              "ID, MulakatZamani, MentorAdi, MentorSoyadi, MentorMail, "
              "Summary, Description, Location, OnlineMeetingLink "
              "FROM appointments "
              "WHERE MentiID IS NULL")
        self.open_appointments = main.execute_read_query(main.open_conn(), q1)

        dialog = QDialog(self)
        dialog.setWindowTitle("Açık Randevular")
        layout = QVBoxLayout(dialog)

        table = QTableWidget()
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setRowCount(len(self.open_appointments))

        for row, appointment in enumerate(self.open_appointments):
            for col, value in enumerate(appointment[1:]):  # ID'yi atlayarak başlıyoruz
                item = QTableWidgetItem(str(value))
                table.setItem(row, col, item)

        layout.addWidget(table)

        close_button = QPushButton("Kapat")
        close_button.clicked.connect(dialog.close)
        layout.addWidget(close_button)

        dialog.setLayout(layout)

        # Randevu seçimi ve mentor atama işlemi
        table.cellDoubleClicked.connect(self.on_appointment_selected)

        dialog.exec()

    def on_appointment_selected(self, row, col):
        appointment_id = self.open_appointments[row][0]
        self.assign_mentor(appointment_id)

    def assign_mentor(self, appointment_id):
        reply = QMessageBox.question(self, 'Mentor Atama', 'Bu randevuya mentor atamak istiyor musunuz?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            # Seçili satırın BasvuranID'sini al
            current_row = self.form_interviews.tableWidget.currentRow()
            basvuran_id = self.basvuran_ids[current_row]  # BasvuranID'yi saklanan listeden al

            # Veritabanında güncelleme yap
            q1 = "UPDATE appointments SET MentiID = %s WHERE ID = %s"
            main.execute_query(main.open_conn(), q1, (basvuran_id, appointment_id))
            q2 = ("UPDATE "
                  "form_basvuru "
                  "SET "
                  "IlkMulakat = 1 "
                  "WHERE BasvuruDonemi = %s AND BasvuranID = %s")
            main.execute_query(main.open_conn(), q2, (main.last_period, basvuran_id))

            QMessageBox.information(self, 'Başarılı', 'Mentor başarıyla atandı.')

            # Dialog'u kapat
            self.sender().parent().close()
            # Tabloyu güncelle
            self.mentor_not_assigned_applicants()

    def mentor_not_assigned_applicants(self):
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
              "b.BasvuranID, b.ZamanDamgasi, b.BasvuruDonemi, a.Ad, a.Soyad, a.Email, a.Telefon, a.PostaKodu, "
              "a.YasadiginizEyalet, b.SuAnkiDurum, b.ITPHEgitimKatilmak, b.EkonomikDurum, b.DilKursunaDevam, "
              "b.IngilizceSeviye, b.HollandacaSeviye, b.BaskiGoruyor, b.BootcampBitirdi, b.OnlineITKursu, "
              "b.ITTecrube, b.ProjeDahil, b.CalismakIstedigi, b.NedenKatilmakIstiyor, b.MotivasyonunNedir "
              "FROM form_basvuru b "
              "INNER JOIN form_basvuran a ON b.BasvuranID = a.ID "
              "WHERE b.BasvuruDonemi = %s AND b.IlkMulakat = 0 "
              "ORDER BY b.ZamanDamgasi ASC")

        not_appointed = main.execute_read_query(main.open_conn(), q1, (main.last_period,))

        # Rebuilds the list based on the data type of the cells.
        self.active_list = main.remake_it_with_types(not_appointed)

        self.basvuran_ids = [row[0] for row in not_appointed]  # BasvuranID'leri sakla
        self.active_list = [row[1:] for row in not_appointed]  # BasvuranID hariç diğer verileri sakla

        # Applicants who have not been assigned a mentor
        main.write2table(self.form_interviews, self.headers, self.active_list)
        self.form_interviews.tableWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

    def mentor_assigned_applicants(self):
        self.headers = ['Mulakat Zamanı', 'Menti Ad', 'Menti Soyad', 'Menti Mail', 'Mentor Ad', 'Mentor Soyad',
                        'Mentor Mail', 'Gorev Adi', 'Aciklama', 'Lokasyon', 'Online Meeting Link', 'Response Status']
        q1 = ("SELECT "
              "b.MulakatZamani, a.Ad, a.Soyad, a.Email, b.MentorAdi, b.MentorSoyadi, b.MentorMail, b.Summary, "
              "b.Description, b.Location, b.OnlineMeetingLink, b.ResponseStatus "
              "FROM appointments b "
              "INNER JOIN form_basvuran a ON b.MentiID = a.ID "
              "WHERE b.MentiID is not null "
              "ORDER BY b.MulakatZamani ASC")

        # burayi mulakat islemi olmus veya tarihi gecmis islemleri de sorgulamak icin oncekinin onune ekleyebiliriz.
        # boylece tum datayi gorebiliriz. aktif olan appointments uzerinde islem yapariz, gereksiz randevular gozukmez
        # ama ayni zamanda eski atamalari da gorebiliriz.
        q2 = ("SELECT "
              "b.MulakatZamani, a.Ad, a.Soyad, a.Email, b.MentorAdi, b.MentorSoyadi, b.MentorMail, b.Summary, "
              "b.Description, b.Location, b.OnlineMeetingLink, b.ResponseStatus "
              "FROM appointments_old_or_deleted b "
              "INNER JOIN form_basvuran a ON b.MentiID = a.ID "
              "WHERE b.MentiID is not null "
              "ORDER BY b.MulakatZamani ASC")
        mentor_assigned_applicants = main.execute_read_query(main.open_conn(), q1)

        # Tum basvuru donemlerinde -bir sekilde- mentor atanmis basvuranlari ve mentorlerini getir.
        if self.form_interviews.comboBoxAssignedApplicants.currentText() == 'All Periods':
            old_mentor_assigned_applicants = main.execute_read_query(main.open_conn(), q2)
            mentor_assigned_applicants = old_mentor_assigned_applicants + mentor_assigned_applicants

        self.active_list = mentor_assigned_applicants
        # Applicants who have been assigned a mentor
        main.write2table(self.form_interviews, self.headers, self.active_list)

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
    # def on_cell_entered(self, row, column):
    #     # Get the text of the cell at the specified row and column
    #     item_text = self.form_interviews.tableWidget.item(row, column).text()
    #
    #     # Show a tooltip with the cell text
    #     tooltip = self.form_interviews.tableWidget.viewport().mapToGlobal(
    #         self.form_interviews.tableWidget.visualItemRect(
    #             self.form_interviews.tableWidget.item(row, column)).topLeft())
    #     QToolTip.setFont(QFont("SansSerif", 10))
    #     QToolTip.showText(tooltip, item_text)

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


# ........................................... Presentation Codes END ..................................................#


if __name__ == "__main__":
    app = QApplication([])
    main_window = InterviewsPage(('a', 'b', 'admin'))
    main_window.show()
    app.exec()
