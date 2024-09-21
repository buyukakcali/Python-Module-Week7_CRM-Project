import gspread
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget, QApplication, QMenu, QMessageBox, QDialog, QVBoxLayout,
                             QTableWidget, QPushButton, QHBoxLayout, QLabel)

from oauth2client.service_account import ServiceAccountCredentials

from UI_Files.candidates_ui import Ui_FormCandidates
import my_functions as myf
from my_classes import Config


class CandidatesPage(QWidget):
    def __init__(self, current_user) -> None:
        super().__init__()
        self.current_user = current_user  # Variable name is absolutely perfect for why it is here
        self.sort_order = {}  # Dictionary to keep track of sort order for each column

        self.candidates = None
        self.active_list = None
        self.filtering_list = []
        self.open_appointments = None
        self.event_ids = None  # Mentor atamasinda Attendee bilgilerinin sheet dosyasina yazilirken karsilastirma icin

        self.form_candidates = Ui_FormCandidates()
        self.form_candidates.setupUi(self)
        self.menu_user = None
        self.menu_admin = None

        # Persistent form settings activated at startup:
        self.form_candidates.tableWidget.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft)
        myf.add_tooltip_to_any_form_object(self.form_candidates.comboBoxTrainees, 'Trainees')

        # Initial load view settings
        self.filtering_column = 10
        self.headers = ['Zaman damgası', 'Basvuru Donemi', 'Mentor Ad', 'Mentor Soyad', 'Mentor Mail', 'Basvuran Ad',
                        'Basvuran Soyad', 'Basvuran Mail', 'Basvuran IT sektör bilgisi', 'Basvuran yoğunluk',
                        'Düşünceler', 'Yorumlar'
                        ]
        myf.write2table(self.form_candidates, self.headers, [])  # This code updates the tableWidget headers
        self.form_candidates.comboBoxFilterOptions.setPlaceholderText(
            "Katılımcı Hakkındaki Tavsiyelere Göre Filtreleyin")

        # Google Drivedaki sheet dosyasına bağlanma
        self.google_first_interview_sheet_name = 'IlkMulakat'  # Firs interview sheet
        self.google_applicant_evaluations_sheet_name = 'AdayDegerlendirmesi'  # Applicant evaluation sheet
        self.google_credentials_file = 'credentials/key.json'  # Your credentials file

        # Google Sheets API bağlantısını ayarla
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://spreadsheets.google.com/feeds",
                 "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(self.google_credentials_file, scope)
        self.client = gspread.authorize(creds)


        # Connect signals to slots
        self.form_candidates.lineEditSearch.textEdited.connect(self.search_candidates)
        self.form_candidates.lineEditSearch.returnPressed.connect(self.search_candidates)
        self.form_candidates.pushButtonGetCandidatess.clicked.connect(self.get_candidates)
        #
        self.normalise_comboBoxTrainees()
        self.form_candidates.comboBoxTrainees.currentIndexChanged.connect(self.get_interviewed_candidates)
        #
        self.form_candidates.comboBoxFilterOptions.currentIndexChanged.connect(self.filter_table)
        self.form_candidates.pushButtonBackMenu.clicked.connect(self.back_menu)
        self.form_candidates.pushButtonExit.clicked.connect(self.app_exit)

        # Connect the cellEntered signal to the on_cell_entered method
        self.form_candidates.tableWidget.cellEntered.connect(self.on_cell_entered)

        # Connect the cellClicked signal to the on_cell_clicked method
        self.form_candidates.tableWidget.cellClicked.connect(self.on_cell_clicked)

        # Connect the header's sectionClicked signal to the on_header_clicked method
        self.form_candidates.tableWidget.horizontalHeader().sectionClicked.connect(self.on_header_clicked)

        # Connect the header's sectionDoubleClicked signal to the on_header_double_clicked method
        self.form_candidates.tableWidget.horizontalHeader().sectionDoubleClicked.connect(self.on_header_double_clicked)

        # This code enables mouse tracking on tableWidget. It is needed for all mouse activity options above!
        self.form_candidates.tableWidget.setMouseTracking(True)

        # The display settings of the last clicked button are determined.
        self.widgets = self.findChildren(QPushButton)  # Find all buttons of type QPushButton & assign them to the list
        self.widgets.append(self.form_candidates.comboBoxTrainees)  # adding the QComboBox object extra
        myf.handle_widget_styles(self, self.widgets)  # Manage button styles with central function

    def get_candidates(self):
        try:
            cnf = Config()
            self.headers = ['Zaman damgası', 'Basvuru Donemi', 'Basvuran Ad', 'Basvuran Soyad', 'Basvuran Mail',
                            'Mentor Ad', 'Mentor Soyad', 'Mentor Mail', 'ID', "Situation"
                            ]
            # q1 = ("SELECT "
            #       "fe.crm_ID, fe.crm_Timestamp, fe.crm_Period, fa.crm_Name, fa.crm_Surname, fa.crm_Email, fe.crm_ITSkills, fe.crm_Availability, fe.crm_Recommendation, "
            #       "fe.crm_Comment, ac.crm_MentorName, ac.crm_MentorSurname, ac.crm_MentorMail, fe.crm_IsApplicantACandidate "
            #       "FROM "
            #       "form2_evaluations fe "
            #       "LEFT JOIN appointments_current ac ON fe.crm_MentorMail = ac.crm_MentorMail "
            #       "INNER JOIN form1_applicant fa ON fe.crm_ApplicantID = fa.crm_ID "
            #       "WHERE fe.crm_Period = %s AND fe.crm_IsApplicantACandidate = %s "
            #       "GROUP BY "
            #       "fe.crm_ID, fe.crm_Timestamp, fe.crm_Period, "
            #       "fa.crm_Name, fa.crm_Surname, fa.crm_Email, fe.crm_ITSkills, fe.crm_Availability, fe.crm_Recommendation, "
            #       "fe.crm_Comment, ac.crm_MentorName, ac.crm_MentorSurname, ac.crm_MentorMail, fe.crm_IsApplicantACandidate"
            #       )
            q1 = ("SELECT "
                  "fe.crm_Timestamp, fe.crm_Period, fa.crm_Name, fa.crm_Surname, fa.crm_Email, "
                  "ac.crm_MentorName, ac.crm_MentorSurname, ac.crm_MentorMail, fe.crm_ID, fe.crm_IsApplicantACandidate "
                  "FROM "
                  "form2_evaluations fe "
                  "LEFT JOIN appointments_current ac ON fe.crm_MentorMail = ac.crm_MentorMail "
                  "INNER JOIN form1_applicant fa ON fe.crm_ApplicantID = fa.crm_ID "
                  "WHERE fe.crm_Period = %s AND fe.crm_IsApplicantACandidate > %s "
                  "GROUP BY "
                  "fe.crm_ID, fe.crm_Timestamp, fe.crm_Period, fa.crm_Name, fa.crm_Surname, fa.crm_Email, "
                  "ac.crm_MentorName, ac.crm_MentorSurname, ac.crm_MentorMail, fe.crm_ID, fe.crm_IsApplicantACandidate"
                  )


            candidates = myf.execute_read_query(cnf.open_conn(), q1, (myf.last_period(), 0))

            # Rebuilds the list based on the data type of the cells.
            candidates = myf.remake_it_with_types(candidates)
            # self.active_list = [row[1:] for row in applicants]  # ID hariç diğer verileri ata
            self.active_list = list(candidates)

            self.filtering_list = list(self.active_list)  # Assigned for filtering.
            myf.write2table(self.form_candidates, self.headers, self.active_list)
            myf.resize_columns(self.form_candidates.tableWidget)

            # Fill the combobox for default filtering while loading
            self.filtering_column = 2
            self.form_candidates.comboBoxFilterOptions.setPlaceholderText("Filtre Alanı")
            self.form_candidates.comboBoxFilterOptions.clear()
            items = myf.filter_active_options(self.filtering_list, self.filtering_column)
            self.form_candidates.comboBoxFilterOptions.addItems(items)

            # tableWidget line coloring process
            # The function called shows the records with colored background for displaying INTERVIEW DETERMINED
            myf.highlight_candidates(self.form_candidates, 9, 2, 'orange')
        except Exception as e:
            raise Exception(f"Error occurred in get_interviewed_applicants method: {e}")

    def show_context_menu_assign_mentor(self, pos):
        try:
            item = self.form_candidates.tableWidget.itemAt(pos)
            if item is None or self.form_candidates.tableWidget.rowCount() == 0:
                return  # Eğer geçerli bir öğe yoksa veya tablo boşsa, hiçbir şey yapma

            self.form_candidates.tableWidget.selectRow(item.row())

            context_menu = QMenu(self)
            show_assign_mentor_action = context_menu.addAction("Assign Mentor")
            action = context_menu.exec(self.form_candidates.tableWidget.viewport().mapToGlobal(pos))

            if action == show_assign_mentor_action:
                self.show_open_appointments()
        except Exception as e:
            raise Exception(f"Error occurred in show_context_menu_assign_mentor method: {e}")

    def show_open_appointments(self):
        try:
            current_row = self.form_candidates.tableWidget.currentRow()
            if int(self.form_candidates.tableWidget.item(current_row, 9).text()) == 2:
                dialog = QDialog(self)
                dialog.setWindowTitle("Bilgi:")
                layout = QVBoxLayout(dialog)

                # Bilgi mesajını ekle
                info_label = QLabel("The candidate is already assigned for a project homework meeting!")
                layout.addWidget(info_label)

                # Kapat butonunun genişliğini sınırlamak için maksimum genişliği ayarlayın
                close_button = QPushButton("Kapat")
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
            else:
                cnf = Config()
                headers = ['Mulakat Zamanı', 'Mentor Ad', 'Mentor Soyad', 'Mentor Mail', 'Gorev Adi', 'Aciklama',
                           'Lokasyon', 'Online Meeting Link']

                q1 = ("SELECT " + cnf.appointmentsTableFieldNames[3] + ", " + cnf.appointmentsTableFieldNames[4] +
                      ", " + cnf.appointmentsTableFieldNames[5] + ", " + cnf.appointmentsTableFieldNames[6] +
                      ", " + cnf.appointmentsTableFieldNames[7] + ", " + cnf.appointmentsTableFieldNames[8] +
                      ", " + cnf.appointmentsTableFieldNames[9] + ", " + cnf.appointmentsTableFieldNames[10] +
                      ", " + cnf.appointmentsTableFieldNames[2] + " " +
                      "FROM " + cnf.appointmentsTable + " " +
                      "WHERE " + cnf.appointmentsTableFieldNames[7] + " LIKE '2%' " +
                      "AND " + cnf.appointmentsTableFieldNames[12] + " is null " +
                      "ORDER BY " + cnf.appointmentsTableFieldNames[3] + " ASC")

                open_appointments = myf.execute_read_query(cnf.open_conn(), q1)
                self.open_appointments = myf.remake_it_with_types(open_appointments)

                dialog = QDialog(self)
                dialog.setWindowTitle("Açık Randevular")
                layout = QVBoxLayout(dialog)

                # Create a temporary QTableWidget to pass to write2table
                table_widget = QTableWidget()
                table_widget.setColumnCount(len(headers))
                table_widget.setHorizontalHeaderLabels(headers)
                table_widget.setRowCount(len(self.open_appointments))

                # Create a temporary object to hold the table widget
                class TempPage:
                    def __init__(self, table_widget_example):
                        self.tableWidget = table_widget_example

                temp_page = TempPage(table_widget)

                # Use write2table to populate the table
                myf.write2table(temp_page, headers, self.open_appointments)

                layout.addWidget(temp_page.tableWidget)

                # Kapat butonunun genişliğini sınırlamak için maksimum genişliği ayarlayabilirsiniz
                close_button = QPushButton("Kapat")
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

                # Code that makes the opened tableWidget appear properly
                myf.auto_resize_window_for_table(dialog, table_widget)

                # Randevu seçimi ve mentor atama işlemi
                temp_page.tableWidget.cellDoubleClicked.connect(self.on_appointment_selected)
                dialog.exec()
        except Exception as e:
            raise Exception(f"Error occurred in show_open_appointments method: {e}")

    def on_appointment_selected(self, row):
        try:
            event_id = self.open_appointments[row][8]
            self.assign_mentor(event_id)
        except Exception as e:
            raise Exception(f"Error occurred in on_appointment_selected method: {e}")

    def assign_mentor(self, event_id):
        try:
            cnf = Config()
            reply = QMessageBox.question(self, 'Mentor Atama', 'Bu randevuya mentor atamak istiyor musunuz?',
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                # Seçili satırın ID'sini al
                current_row = self.form_candidates.tableWidget.currentRow()
                ID = self.form_candidates.tableWidget.item(current_row, 12).text()

                # Veritabanında güncelleme yap
                q1 = "UPDATE appointments_current SET crm_AttendeeID = %s WHERE crm_EventID = %s"
                # q1 = ("UPDATE " + cnf.appointmentsTable + " SET " + cnf.appointmentsTableFieldNames[12] + " = %s " +
                #       "WHERE " + cnf.appointmentsTableFieldNames[2] + " = %s")
                myf.execute_query(cnf.open_conn(), q1, (ID, event_id))

                q2 = "UPDATE form2_evaluations SET crm_IsApplicantACandidate = 2 WHERE crm_Period = %s AND crm_ID = %s"
                # q2 = ("UPDATE " + cnf.applicationTable + " SET " + cnf.applicationTableFieldNames[18] + " = 1 WHERE "
                #       + cnf.applicationTableFieldNames[3] + " = %s AND " + cnf.applicantTableFieldNames[0] + " = %s")
                myf.execute_query(cnf.open_conn(), q2, (myf.last_period(), ID))

                # Basvuranın adını, soyadını ve email'ini veritabanından çekip Google Sheet'e yazdıracagiz.
                get_candidates_query = "SELECT crm_Name, crm_Surname, crm_Email FROM form1_applicant WHERE crm_ID = %s"
                # applicant_query = (
                #         "SELECT " + cnf.applicantTableFieldNames[2] + ", " + cnf.applicantTableFieldNames[3] +
                #         ", " + cnf.applicantTableFieldNames[4] + " " +
                #         "FROM " + cnf.applicantTable + " WHERE " + cnf.applicantTableFieldNames[0] + " = %s")
                candidates_data = myf.execute_read_query(cnf.open_conn(), get_candidates_query, (ID,))
                attendee_name, attendee_surname, attendee_email = candidates_data[0]
                print(candidates_data[0], ' : bunu sheete yollayacagiz!')

                # self.update_first_interview_sheet(event_id, attendee_name, attendee_surname, attendee_email)

                QMessageBox.information(self, 'Başarılı', 'Mentor başarıyla atandı.')

                # Dialog'u kapat
                self.sender().parent().close()

                # Tabloyu güncelle
                self.get_candidates()
        except Exception as e:
            raise Exception(f"Error occurred in assign_mentor method: {e}")

        # Gspread kullanarak FirstInterview sheetine bağlantı kuran metot

    # def update_first_interview_sheet(self, event_id, attendee_name, attendee_surname, attendee_email):
    #     try:
    #         # Google Sheet dosyasını aç
    #         sheet = self.client.open(self.google_first_interview_sheet_name).sheet1
    #
    #         # Event ID sütunundaki tüm verileri al (Event ID'nin olduğu sütunun numarası 2)
    #         event_ids = sheet.col_values(2)
    #
    #         # İlgili Event ID'nin olduğu satırı bul
    #         for idx, sheet_event_id in enumerate(event_ids):
    #             if sheet_event_id == event_id:
    #                 # İlgili satırda, Attendee Name, Surname, ve Mail sütunlarını güncelle
    #                 sheet.update_cell(idx + 1, 11, attendee_email)  # 11: Attendee Mail sütunu
    #                 sheet.update_cell(idx + 1, 13, attendee_name)  # 13: Attendee Name sütunu
    #                 sheet.update_cell(idx + 1, 14, attendee_surname)  # 14: Attendee Surname sütunu
    #                 break
    #         else:
    #             print(f"Event ID {event_id} not found in the sheet.")
    #     except Exception as e:
    #         raise Exception(f"Error occurred in update_first_interview_sheet method: {e}")

    def get_interviewed_candidates(self):
        try:

            # burasi bastan yazilacak. db den veri cekecek, formla gelen verileri!!! asagidaki kod get_canditadets in kodu!..
            self.form_candidates.comboBoxFilterOptions.currentIndexChanged.connect(self.filter_table)

            cnf = Config()

            self.headers = ['Zaman damgası', 'Basvuru Donemi', 'Basvuran Ad', 'Basvuran Soyad', 'Basvuran Mail',
                            'Mentor Ad', 'Mentor Soyad', 'Mentor Mail', 'ID', "Situation"
                            ]

            q1 = ("SELECT "
                  "fe.crm_Timestamp, fe.crm_Period, fa.crm_Name, fa.crm_Surname, fa.crm_Email, "
                  "ac.crm_MentorName, ac.crm_MentorSurname, ac.crm_MentorMail, fe.crm_ID, fe.crm_IsApplicantACandidate "
                  "FROM "
                  "form2_evaluations fe "
                  "LEFT JOIN appointments_current ac ON fe.crm_MentorMail = ac.crm_MentorMail "
                  "INNER JOIN form1_applicant fa ON fe.crm_ApplicantID = fa.crm_ID "
                  "WHERE fe.crm_Period = %s AND fe.crm_IsApplicantACandidate > %s "
                  "GROUP BY "
                  "fe.crm_ID, fe.crm_Timestamp, fe.crm_Period, fa.crm_Name, fa.crm_Surname, fa.crm_Email, "
                  "ac.crm_MentorName, ac.crm_MentorSurname, ac.crm_MentorMail, fe.crm_ID, fe.crm_IsApplicantACandidate"
                  )

            candidates = myf.execute_read_query(cnf.open_conn(), q1, (myf.last_period(), 0))

            # Veriyi tabloya ekle
            self.candidates = myf.remake_it_with_types(candidates)
            self.active_list = list(candidates)

            myf.write2table(self.form_candidates, self.headers, self.active_list)

            # Filtreleme için combobox'u doldur
            self.filtering_column = 2
            self.form_candidates.comboBoxFilterOptions.setPlaceholderText("Filtre Alanı")
            self.filtering_list = list(self.active_list)  # Filtreleme için atandı
            self.form_candidates.comboBoxFilterOptions.clear()
            items = myf.filter_active_options(self.filtering_list, self.filtering_column)
            self.form_candidates.comboBoxFilterOptions.addItems(items)

        except Exception as e:
            raise Exception(f"Error occurred in get_interviewed_applicants method: {e}")

    def back_menu(self):
        try:
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
        except Exception as e:
            raise Exception(f"Error occurred in back_menu method: {e}")

    def app_exit(self):
        self.close()


    # Search settings for CandidatesPage
    def search_candidates(self):
        self.normalise_combobox_filter_options()

        # Eğer aktif liste varsa, filtering_list'i güncelle
        if self.active_list:
            self.filtering_list = list(self.active_list)  # Filtreleme için listeyi ata.

        searched_text = self.form_candidates.lineEditSearch.text()    # Arama alanındaki metni al

        # Sonuçları al
        self.filtering_list = myf.search(self.filtering_list, self.headers, self.filtering_column, searched_text)

        myf.write2table(self.form_candidates, self.headers, self.filtering_list)    # Sonuçları tabloya yaz

        # Fill the combobox for filtering after every single search
        if self.active_list:
            self.filtering_list = list(self.active_list)
            items = myf.filter_active_options(self.filtering_list, self.filtering_column)
            self.form_candidates.comboBoxFilterOptions.addItems(items)

    # Filter settings for InterviewsPage
    def filter_table(self):
        try:
            self.form_candidates.lineEditSearch.clear()  # clear the search box
            myf.filter_table_f(self.form_candidates, self.headers, self.filtering_list, self.filtering_column)
        except Exception as e:
            raise Exception(f"Error occurred in filter_table method: {e}")
    # .................................................................................................................#
    # .......................................... PRESENTATION CODES START .............................................#
    # .................................................................................................................#

    # Method to automatically adjust the display settings of the comboBoxFilterOptions object
    def normalise_combobox_filter_options(self):
        try:
            self.form_candidates.comboBoxFilterOptions.clear()
            self.form_candidates.comboBoxFilterOptions.setPlaceholderText("Filtre Alani")
        except Exception as e:
            raise Exception(f"Error occurred in normalise_combobox_filter_options method: {e}")

    # Method to automatically adjust the display settings of the comboBoxTrainees object
    def normalise_comboBoxTrainees(self):
        try:
            myf.normalise_comboBoxes(
                [self.form_candidates.comboBoxTrainees, self.form_candidates.comboBoxFilterOptions],
                ['             Trainess', '          Last Period', '          All Periods'])
        except Exception as e:
            raise Exception(f"Error occurred in normalise_comboBoxTrainees method: {e}")

    # This code is written to make the contents appear briefly when hovering over the cell.
    def on_cell_entered(self, row, column):
        try:
            myf.on_cell_entered_f(self.form_candidates, row, column)
        except Exception as e:
            raise Exception(f"Error occurred in on_cell_entered method: {e}")

    def on_cell_clicked(self, row, column):
        try:
            myf.on_cell_clicked_f(self.form_candidates, row, column)
        except Exception as e:
            raise Exception(f"Error occurred in on_cell_clicked method: {e}")

    # This code is for header clicking. This method sorts the data based on the column that was clicked
    def on_header_clicked(self, logical_index):
        try:
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
            self.form_candidates.tableWidget.sortItems(logical_index, order=new_order)
        except Exception as e:
            raise Exception(f"Error occurred in on_header_clicked method: {e}")

    # This method is for header double-clicking.
    # Activity code to offer new filtering options when you click on the titles
    def on_header_double_clicked(self, logical_index):
        try:
            # Check that filtering list is not empty and is of list type
            if not self.filtering_list or not isinstance(self.filtering_list, list):
                print("Filtering list is empty or not initialized")
                return

            # Check if logical_index is within the bounds of the list
            if logical_index >= len(self.filtering_list[0]):
                print(f"Invalid logical_index: {logical_index}")
                return

            # Get the value at the specified logical_index
            value = self.filtering_list[0][logical_index]
            # print(f"Value at index {logical_index}: {value}, Type: {type(value)}")

            # Check if value is None and not string
            if value is None:
                print(f"Value at index {logical_index} is None")
                return

            self.form_candidates.comboBoxFilterOptions.clear()
            self.filtering_column = logical_index
            self.form_candidates.comboBoxFilterOptions.setPlaceholderText("Filtre Alani")
            items = myf.filter_active_options(self.filtering_list, logical_index)
            # print('Filtered items: ', items)
            self.form_candidates.comboBoxFilterOptions.addItems(items)
            myf.write2table(self.form_candidates, self.headers, self.active_list)
            self.form_candidates.comboBoxFilterOptions.currentIndexChanged.connect(self.filter_table)

        except Exception as e:
            raise Exception(f"Error occurred in on_header_double_clicked method: {e}")

    # ......................................... Presentation Codes END ................................................#


if __name__ == "__main__":
    app = QApplication([])
    main_window = CandidatesPage(('a', 'b', 'admin'))
    main_window.show()
    app.exec()
