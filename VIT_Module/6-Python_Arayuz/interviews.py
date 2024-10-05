import gspread
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget, QApplication, QMenu, QDialog, QVBoxLayout, QPushButton, QTableWidget, QHBoxLayout,
                             QMessageBox)
from oauth2client.service_account import ServiceAccountCredentials

import my_functions as myf
from UI_Files.interviews_ui import Ui_FormInterviews
from my_classes import Config


class InterviewsPage(QWidget):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user  # Variable name is absolutely perfect for why it is here
        self.sort_order = {}  # Dictionary to keep track of sort order for each column

        self.applicants = None
        self.active_list = None
        self.filtering_list = []
        self.open_appointments = None
        # self.event_ids is for comparison when writing Attendee information to the sheet file during mentor appointment
        self.event_ids = None

        self.form_interviews = Ui_FormInterviews()
        self.form_interviews.setupUi(self)
        self.menu_user = None
        self.menu_admin = None

        # Persistent form settings activated at startup:
        self.form_interviews.labelInfo1.close()
        self.form_interviews.tableWidget.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft)
        self.form_interviews.tableWidget.setStyleSheet("""
                        QTableWidget { background-color: rgba(0, 0, 0,0%);}
                        QToolTip { background-color: yellow; color: black; border: 1px solid black; }
                        """)

        # Initial load view and first filtering column settings:
        cnf = Config()
        self.filtering_column = 2
        self.form_interviews.comboBoxFilterOptions.setPlaceholderText("Filter Area")
        self.headers = [
            "Zaman damgası", "Başvuru dönemi", "Ad", "Soyad", "E-Mail", "Telefon", "Posta kodu", "Eyalet", "Durumu",
            "ITPH Talebi", "Ekonomik durumu", "Dil kursu?", "İngilizce", "Hollandaca", "Belediye baskısı?",
            "IT kursu / Bootcamp?", "İnternet IT kursu?", "IT iş tecrübesi?", "Başka bir proje?", "IT sektör hayali?",
            "Neden VIT projesi", "Motivasyonu?", "Id", "Situation"
        ]
        myf.write2table(self.form_interviews, self.headers, [])  # This code updates the tableWidget headers

        # Connecting to sheet file in Google Drive:
        # 2-Events_All_Interviews sheet
        self.google_events_all_interviews_sheet_name = cnf.google_events_all_interviews_sheet_name
        # 3-Application_Evaluations_Form_Answers sheet
        self.google_applicant_evaluations_sheet_name = cnf.google_applicant_evaluations_sheet_name
        self.google_credentials_file = cnf.google_credentials_file  # Your credentials file

        # Set Google Sheets API connection
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://spreadsheets.google.com/feeds",
                 "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(self.google_credentials_file, scope)
        self.client = gspread.authorize(creds)

        # Connect signals to slots
        self.form_interviews.lineEditSearch.textEdited.connect(self.search_interviews)
        self.form_interviews.lineEditSearch.returnPressed.connect(self.search_interviews)
        self.form_interviews.pushButtonUnassignedApplicants.clicked.connect(self.mentor_not_assigned_applicants)
        self.form_interviews.pushButtonAssignedApplicants.clicked.connect(self.mentor_assigned_applicants)
        self.form_interviews.pushButtonInterviewedApplicants.clicked.connect(self.get_interviewed_applicants)
        self.form_interviews.pushButtonBackMenu.clicked.connect(self.back_menu)
        self.form_interviews.pushButtonExit.clicked.connect(self.app_exit)

        # EXTRA SLOTS:
        # ------------

        # Connect the cellEntered signal to the on_cell_entered method
        # self.form_interviews.tableWidget.cellEntered.connect(self.on_cell_entered)

        # Connect the cellEntered signal to the on_cell_entered method
        self.form_interviews.tableWidget.cellClicked.connect(self.on_cell_clicked)

        # Connect the header's sectionClicked signal to the on_header_clicked method
        self.form_interviews.tableWidget.horizontalHeader().sectionClicked.connect(self.on_header_clicked)

        # Connect the header's sectionDoubleClicked signal to the on_header_double_clicked method
        self.form_interviews.tableWidget.horizontalHeader().sectionDoubleClicked.connect(self.on_header_double_clicked)

        # This code enables mouse tracking on tableWidget. It is needed for all mouse activity options above!
        self.form_interviews.tableWidget.setMouseTracking(True)

        # The display settings of the last clicked button are determined.
        self.widgets = self.findChildren(QPushButton)  # Find all buttons of type QPushButton & assign them to the list
        myf.handle_widget_styles(self, self.widgets)  # Manage button styles with central function

    # Shows applications that have not yet been assigned a first interview appointment.
    def mentor_not_assigned_applicants(self):
        try:
            self.form_interviews.comboBoxFilterOptions.currentIndexChanged.connect(self.filter_table)
            cnf = Config()

            self.headers = [
                "Zaman damgası", "Başvuru dönemi",
                "Ad", "Soyad", "E-Mail", "Telefon", "Posta kodu", "Eyalet",
                "Durumu", "ITPH Talebi", "Ekonomik durumu", "Dil kursu?", "İngilizce", "Hollandaca",
                "Belediye baskısı?", "IT kursu / Bootcamp?", "İnternet IT kursu?", "IT iş tecrübesi?",
                "Başka bir proje?", "IT sektör hayali?", "Neden VIT projesi", "Motivasyonu?", "Id", "Situation"
            ]
            print(type(self.headers))

            q1 = ("SELECT "
                  "b." + cnf.applicationTableFieldNames[2] + ", b." + cnf.applicationTableFieldNames[3] +
                  ", a." + cnf.applicantTableFieldNames[2] + ", a." + cnf.applicantTableFieldNames[3] +
                  ", a." + cnf.applicantTableFieldNames[4] + ", a." + cnf.applicantTableFieldNames[5] +
                  ", a." + cnf.applicantTableFieldNames[6] + ", a." + cnf.applicantTableFieldNames[7] +
                  ", b." + cnf.applicationTableFieldNames[4] + ", b." + cnf.applicationTableFieldNames[5] +
                  ", b." + cnf.applicationTableFieldNames[6] + ", b." + cnf.applicationTableFieldNames[7] +
                  ", b." + cnf.applicationTableFieldNames[8] + ", b." + cnf.applicationTableFieldNames[9] +
                  ", b." + cnf.applicationTableFieldNames[10] + ", b." + cnf.applicationTableFieldNames[11] +
                  ", b." + cnf.applicationTableFieldNames[12] + ", b." + cnf.applicationTableFieldNames[13] +
                  ", b." + cnf.applicationTableFieldNames[14] + ", b." + cnf.applicationTableFieldNames[15] +
                  ", b." + cnf.applicationTableFieldNames[16] + ", b." + cnf.applicationTableFieldNames[17] +
                  ", " + "b." + cnf.applicationTableFieldNames[1] +
                  ", " + "b." + cnf.applicationTableFieldNames[18] + " "
                  "FROM " + cnf.applicationTable + " b " +
                  "INNER JOIN " + cnf.applicantTable + " a ON b." + cnf.applicationTableFieldNames[0] +
                  " = a." + cnf.applicantTableFieldNames[0] + " " +
                  "WHERE b." + cnf.applicationTableFieldNames[3] +
                  " = %s AND b." + cnf.applicationTableFieldNames[18] + " <= 1 "
                  +
                  "ORDER BY b." + cnf.applicationTableFieldNames[2] + " ASC")

            not_appointed = myf.execute_read_query(cnf.open_conn(), q1, (myf.last_period(),))

            # Rebuilds the list based on the data type of the cells.
            self.active_list = myf.remake_it_with_types(not_appointed)

            # Write to tableWidget: applicants who have not been assigned a mentor
            myf.write2table(self.form_interviews, self.headers, self.active_list)

            # Fill the combobox for filtering while loading
            self.filtering_list = list(self.active_list)  # Assigned for filtering.
            self.filtering_column = 2
            self.form_interviews.comboBoxFilterOptions.clear()
            items = myf.filter_active_options(self.filtering_list, self.filtering_column)
            self.form_interviews.comboBoxFilterOptions.addItems(items)
        except Exception as e:
            raise Exception(f"Error occurred in mentor_not_assigned_applicants method: {e}")

    # Adding context menu to right-click
    def show_context_menu_assign_mentor(self, pos):
        try:
            item = self.form_interviews.tableWidget.itemAt(pos)
            if item is None or self.form_interviews.tableWidget.rowCount() == 0:
                return  # If there are no valid items or the table is empty, do nothing

            self.form_interviews.tableWidget.selectRow(item.row())

            context_menu = QMenu(self)
            # Center text in menu and remove border with style settings
            context_menu.setStyleSheet("""
                                    QMenu {
                                        border: 1px solid #cccccc;  /* Thin border (optional) */
                                        border-radius: 10px;  /* Round the edges */
                                    }
                                    QMenu::item {
                                        padding: 8px 20px;
                                        color: white;
                                        background-color: darkCyan;
                                        text-align: center;  /* Center text */
                                        font-weight: bold;
                                        border-radius: 10px;  /* Round the edges */
                                    }
                                    QMenu::item:selected {
                                        color: red;
                                        background-color: #a8dadc;  /* Selected item color */
                                        border-radius: 10px;  /* Round the edges */
                                    }
                                """)
            show_assign_mentor_action = context_menu.addAction("Assign Mentor")
            action = context_menu.exec(self.form_interviews.tableWidget.viewport().mapToGlobal(pos))

            if action == show_assign_mentor_action:
                self.show_open_appointments()
        except Exception as e:
            raise Exception(f"Error occurred in show_context_menu_assign_mentor method: {e}")

    # Lists available appointments
    def show_open_appointments(self):
        try:
            cnf = Config()
            headers = ['Mulakat Zamanı', 'Mentor Ad', 'Mentor Soyad', 'Mentor Mail', 'Gorev Adi', 'Aciklama',
                       'Lokasyon', 'Online Meeting Link']

            q1 = ("SELECT " + cnf.appointmentsTableFieldNames[3] + ", " + cnf.appointmentsTableFieldNames[4] +
                  ", " + cnf.appointmentsTableFieldNames[5] + ", " + cnf.appointmentsTableFieldNames[6] +
                  ", " + cnf.appointmentsTableFieldNames[7] + ", " + cnf.appointmentsTableFieldNames[8] +
                  ", " + cnf.appointmentsTableFieldNames[9] + ", " + cnf.appointmentsTableFieldNames[10] +
                  ", " + cnf.appointmentsTableFieldNames[2] + " " +
                  "FROM " + cnf.appointmentsTable + " " +
                  "WHERE " + cnf.appointmentsTableFieldNames[7] + " LIKE '1%' " +
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

            # To limit the width of the close button, you can set the maximum width
            close_button = QPushButton("Kapat")
            close_button.setMaximumWidth(150)  # We limit the maximum width to 150 pixels
            close_button.clicked.connect(dialog.close)

            # Create a QHBoxLayout to center the button
            button_layout = QHBoxLayout()
            button_layout.addStretch()  # Adds space to the left
            button_layout.addWidget(close_button)  # Centers the button
            button_layout.addStretch()  # Adds space to the right
            layout.addLayout(button_layout)  # Add button layout to main layout

            dialog.setLayout(layout)

            # Code that makes the opened tableWidget appear properly
            myf.auto_resize_dialog_window_for_table(dialog, table_widget)

            # Appointment selection and mentor appointment process
            temp_page.tableWidget.cellDoubleClicked.connect(self.on_appointment_selected)
            dialog.exec()
        except Exception as e:
            raise Exception(f"Error occurred in show_open_appointments method: {e}")

    # It is used in show_open_appointments(function above). It was actually separated to reduce code complexity
    def on_appointment_selected(self, row):
        try:
            event_id = self.open_appointments[row][8]
            self.assign_mentor(event_id)
        except Exception as e:
            raise Exception(f"Error occurred in on_appointment_selected method: {e}")

    # Assigns the appropriate selected appointment to the selected row (or vice versa)
    def assign_mentor(self, event_id):
        try:
            # # Disable context menu for blocking the unwanted context menu showing after assigning
            # myf.disable_context_menu(self.form_interviews, self.show_context_menu_assign_mentor)

            cnf = Config()
            reply = QMessageBox.question(self, 'Mentor Atama', 'Bu randevuya mentor atamak istiyor musunuz?',
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                # Get the ApplicantID of the selected row
                current_row = self.form_interviews.tableWidget.currentRow()
                applicant_id = self.form_interviews.tableWidget.item(current_row, 22).text()

                # Update the database
                q1 = ("UPDATE " + cnf.appointmentsTable + " SET " + cnf.appointmentsTableFieldNames[12] + " = %s " +
                      "WHERE " + cnf.appointmentsTableFieldNames[2] + " = %s")
                myf.execute_write_query(cnf.open_conn(), q1, (applicant_id, event_id))

                q2 = ("UPDATE " + cnf.applicationTable + " SET " + cnf.applicationTableFieldNames[18] + " = 1 WHERE "
                      + cnf.applicationTableFieldNames[3] + " = %s AND " + cnf.applicantTableFieldNames[0] + " = %s")
                myf.execute_write_query(cnf.open_conn(), q2, (myf.last_period(), applicant_id))

                # We extract the applicant's name, surname and email from the database and print it on Google Sheet.
                applicant_query = (
                        "SELECT " + cnf.applicantTableFieldNames[2] + ", " + cnf.applicantTableFieldNames[3] +
                        ", " + cnf.applicantTableFieldNames[4] + " " +
                        "FROM " + cnf.applicantTable + " WHERE " + cnf.applicantTableFieldNames[0] + " = %s")
                applicant_data = myf.execute_read_query(cnf.open_conn(), applicant_query, (applicant_id,))
                attendee_name, attendee_surname, attendee_email = applicant_data[0]

                self.update_events_all_interviews_sheet(event_id, attendee_name, attendee_surname, attendee_email)

                QMessageBox.information(self, 'Başarılı', 'Mentor başarıyla atandı.')

                # Close dialog
                self.sender().parent().close()

                # Update table
                self.mentor_not_assigned_applicants()
        except Exception as e:
            raise Exception(f"Error occurred in assign_mentor method: {e}")

    # Method to connect to 2-Events_All_Interviews sheet using gspread
    def update_events_all_interviews_sheet(self, event_id, attendee_name, attendee_surname, attendee_email):
        try:
            # Google Sheet dosyasını aç
            sheet = self.client.open(self.google_events_all_interviews_sheet_name).sheet1

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
        except Exception as e:
            raise Exception(f"Error occurred in update_events_all_interviews_sheet method: {e}")

    # Lists applications for which a mentor has been assigned,
    # or -in other words- an interview appointment has been given.
    def mentor_assigned_applicants(self):
        try:
            self.form_interviews.comboBoxFilterOptions.currentIndexChanged.connect(self.filter_table)
            cnf = Config()
            myf.normalise_combo_boxes([None, self.form_interviews.comboBoxFilterOptions])
            self.headers = ['Mulakat Zamanı', 'Menti Ad', 'Menti Soyad', 'Menti Mail', 'Mentor Ad', 'Mentor Soyad',
                            'Mentor Mail', 'Gorev Adi', 'Aciklama', 'Lokasyon', 'Online Meeting Link',
                            'Response Status']
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
                  "AND " + "b." + cnf.appointmentsTableFieldNames[7] + " LIKE '1%' " +
                  "ORDER BY b." + cnf.appointmentsTableFieldNames[3] + " ASC")

            mentor_assigned_applicants = myf.execute_read_query(cnf.open_conn(), q1)
            self.active_list = list(mentor_assigned_applicants)

            # Applicants who have been assigned a mentor
            myf.write2table(self.form_interviews, self.headers, self.active_list)

            # Fill the combobox for filtering while loading
            self.filtering_list = list(self.active_list)
            self.filtering_column = 1
            self.form_interviews.comboBoxFilterOptions.clear()
            items = myf.filter_active_options(self.filtering_list, self.filtering_column)
            self.form_interviews.comboBoxFilterOptions.addItems(items)
        except Exception as e:
            raise Exception(f"Error occurred in mentor_assigned_applicants method: {e}")

    # Lists applicants who have had their first interview and shows their evaluation.
    def get_interviewed_applicants(self):
        try:
            self.form_interviews.comboBoxFilterOptions.currentIndexChanged.connect(self.filter_table)
            cnf = Config()

            self.headers = ['Zaman damgası', 'Başvuru Dönemi', 'Başvuran Ad', 'Başvuran Soyad', 'Başvuran Mail',
                            'Mentor Ad', 'Mentor Soyad', 'Mentor Mail','Başvuran IT sektör bilgisi',
                            'Başvuran Yoğunluk', 'Düşünceler', 'Yorumlar', "Situation"]

            q1 = ("SELECT "
                  "fe.crm_ID, fe.crm_Timestamp, fe.crm_Period, fa.crm_Name, fa.crm_Surname, fa.crm_Email, "
                  "ac.crm_MentorName, ac.crm_MentorSurname, ac.crm_MentorMail, fe.crm_ITSkills, fe.crm_Availability, "
                  "fe.crm_Recommendation, fe.crm_Comment, crm_IsApplicantACandidate "
                  "FROM form2_evaluations fe "
                  "LEFT JOIN appointments_current ac ON fe.crm_MentorMail = ac.crm_MentorMail "
                  "INNER JOIN form1_applicant fa ON fe.crm_ApplicantID = fa.crm_ID "
                  "WHERE fe.crm_Period = %s "
                  "GROUP BY "
                  "fe.crm_ID, fe.crm_Timestamp, fe.crm_Period, fa.crm_Name, fa.crm_Surname, fa.crm_Email, "
                  "ac.crm_MentorName, ac.crm_MentorSurname, ac.crm_MentorMail, fe.crm_ITSkills, fe.crm_Availability, "
                  "fe.crm_Recommendation, fe.crm_Comment, crm_IsApplicantACandidate")

            applicants = myf.execute_read_query(cnf.open_conn(), q1, (myf.last_period(),))

            # Veriyi tabloya ekle
            self.applicants = myf.remake_it_with_types(applicants)
            self.active_list = list([row[1:] for row in self.applicants])  # ID hariç diğer verileri ata

            myf.write2table(self.form_interviews, self.headers, self.active_list)

            # Filtreleme için combobox'u doldur
            self.filtering_list = list(self.active_list)  # Filtreleme için atandı
            self.filtering_column = 10
            self.form_interviews.comboBoxFilterOptions.clear()
            items = myf.filter_active_options(self.filtering_list, self.filtering_column)
            self.form_interviews.comboBoxFilterOptions.addItems(items)
            self.form_interviews.comboBoxFilterOptions.setPlaceholderText(
                "Filter by Recommendations About Participant")

            # Add tooltip for "Situation" column
            tooltip_text = "This column's mean:\n0: interviewed applicant\n1: determined as a candidate\n2: candidate invited to project interview"
            myf.add_tooltip_to_header(self.form_interviews.tableWidget, 12, tooltip_text)

            # # Fare "Situation" başlığına geldiğinde animasyonu başlatmak için
            # # Header üzerinde event filter kullanarak fare hareketlerini dinle
            # header = self.form_interviews.tableWidget.horizontalHeader()
            # header.installEventFilter(self)
            #
            # # # Animasyon için gerekli değişkenler
            # # self.blinking_columns = [9, 12]
            # # self.blink_active = False  # Animasyonun aktif olup olmadığını kontrol et


        except Exception as e:
            raise Exception(f"Error occurred in get_interviewed_applicants method: {e}")

    # Adding context menu to right-click
    def show_context_menu_add_to_candidates(self, pos):
        try:
            item = self.form_interviews.tableWidget.itemAt(pos)
            if item is None or self.form_interviews.tableWidget.rowCount() == 0:
                return  # Eğer geçerli bir öğe yoksa veya tablo boşsa, hiçbir şey yapma

            self.form_interviews.tableWidget.selectRow(item.row())

            context_menu = QMenu(self)
            # Stil ayarlarıyla menüdeki metinleri ortala ve kenarlığı kaldır
            context_menu.setStyleSheet("""
                                    QMenu {
                                        border: 1px solid #cccccc;  /* Thin border (optional) */
                                        border-radius: 10px;  /* Round the edges */
                                    }
                                    QMenu::item {
                                        padding: 8px 20px;
                                        color: white;
                                        background-color: darkCyan;
                                        text-align: center;  /* Center text */
                                        font-weight: bold;
                                        border-radius: 10px;  /* Round the edges */
                                    }
                                    QMenu::item:selected {
                                        color: red;
                                        background-color: #a8dadc;  /* Selected item color */
                                        border-radius: 10px;  /* Round the edges */
                                    }
                                """)
            add_candidate_action = context_menu.addAction("Add to Candidates")
            action = context_menu.exec(self.form_interviews.tableWidget.viewport().mapToGlobal(pos))

            if action == add_candidate_action:
                # Basvuranin mail adresinin bulundugu sutun = 7
                value = self.form_interviews.tableWidget.item(item.row(), 7)
                applicant_mail = value.text()
                if value is not None:
                    self.add_to_candidates(applicant_mail)
        except Exception as e:
            raise Exception(f"Error occurred in show_context_menu_add_to_candidates method: {e}")

    # Designates the applicant as a candidate
    def add_to_candidates(self, applicant_email):
        try:
            # Secilen satirin listedeki gercek ID degerini bul
            crm_id = None
            mentor_mail = None
            isApplicantACandidate = None
            for element in self.applicants:
                if element[8] == applicant_email:
                    crm_id = element[0]
                    mentor_mail = element[5]
                    isApplicantACandidate = element[13]

            cnf = Config()
            reply = QMessageBox.question(self, 'Aday Belirleme/Ekleme',
                                         'Bu basvurani aday olarak belirlemek istiyor musunuz?',
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes and crm_id:
                # Eger basvurucu, daha once zaten aday olarak belirlenmemisse veritabanında güncelleme yap
                if isApplicantACandidate != 1:
                    q1 = ("UPDATE " + cnf.evaluationTable + " SET " + cnf.evaluationTableFieldNames[13] + " = 1 " +
                          "WHERE " + cnf.evaluationTableFieldNames[2] + " = %s " +
                          "AND " + cnf.evaluationTableFieldNames[0] + " = %s")

                    last_period = myf.last_period()
                    myf.execute_write_query(cnf.open_conn(), q1, (last_period, crm_id))

                    self.update_applicant_evaluations_sheet(last_period, mentor_mail, applicant_email)

                    QMessageBox.information(self, 'Bilgi:', 'Secilen kayit, Aday olarak belirlendi.')

                    # Tabloyu güncelle
                    self.get_interviewed_applicants()
                else:
                    QMessageBox.information(self, 'Bilgi:', 'Secilen kayit zaten daha onceden aday olarak belirlendi.')

        except Exception as e:
            raise Exception(f"Error occurred in add_to_candidates method: {e}")

    # Method to connect to 3-Application_Evaluations_Form_Answers sheet using gspread
    def update_applicant_evaluations_sheet(self, last_period, mentor_mail, applicant_mail):
        try:
            # Google Sheet dosyasını aç
            sheet = self.client.open(self.google_applicant_evaluations_sheet_name).sheet1

            # Sadece 1, 2 ve 3. sütunlardaki verileri al
            column_data = sheet.get('B:D')  # B'dan D'ye kadar olan sütunları alır

            for row_index, element in enumerate(column_data, start=1):
                if element[0] == last_period and element[1] == mentor_mail and element[2] == applicant_mail:
                    # 9. sütuna (I sütunu) 1 değerini yaz
                    sheet.update_cell(row_index, 9, 1)

                    # row_index satırı, 9. sütunu günceller alttaki kodu devredisi biraktim. boylece tekrar eden
                    # satirlar da guncellenecek

                    # break # İlgili satır bulunduğunda döngüden çık
        except gspread.SpreadsheetNotFound:
            print("Spreadsheet bulunamadı. Lütfen dosya adının doğru yazıldığından emin olun.")
        except gspread.WorksheetNotFound:
            print("Çalışma sayfası bulunamadı. Lütfen sayfa adının doğru yazıldığından emin olun.")
        except Exception as e:
            raise Exception(f"Error occurred in update_applicant_evaluations_sheet method: {e}")

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
        try:
            self.close()
        except Exception as e:
            raise Exception(f"Error occurred in app_exit method: {e}")

    # Search settings for InterviewsPage
    def search_interviews(self):
        myf.normalise_combo_boxes([None, self.form_interviews.comboBoxFilterOptions])

        # Eğer aktif liste varsa, filtering_list'i güncelle
        if self.active_list:
            self.filtering_list = list(self.active_list)  # Filtreleme için listeyi ata.

        # Arama alanındaki metni al
        searched_text = self.form_interviews.lineEditSearch.text()

        # Sonuçları al
        self.filtering_list = myf.search(self.filtering_list, self.headers, self.filtering_column, searched_text)

        myf.write2table(self.form_interviews, self.headers, self.filtering_list)  # Sonuçları tabloya yaz

        # Fill the combobox for filtering after every single search
        if self.active_list:
            self.filtering_list = list(self.active_list)
            items = myf.filter_active_options(self.filtering_list, self.filtering_column)
            self.form_interviews.comboBoxFilterOptions.addItems(items)

    # Filter settings for InterviewsPage
    def filter_table(self):
        try:
            self.form_interviews.lineEditSearch.clear()  # clear the search box
            myf.filter_table_f(self.form_interviews, self.headers, self.filtering_list, self.filtering_column)
        except Exception as e:
            raise Exception(f"Error occurred in filter_table method: {e}")

    # .................................................................................................................#
    # .......................................... PRESENTATION CODES START .............................................#
    # .................................................................................................................#

    # This code is written to make the contents appear briefly when hovering over the cell.
    def on_cell_entered(self, row, column):
        try:
            myf.on_cell_entered_f(self.form_interviews, row, column)
        except Exception as e:
            raise Exception(f"Error occurred in on_cell_entered method: {e}")

    # This code is for cell clicking
    # If you want to show a persistent tooltip with the cell text. You need to use this code and its function.
    def on_cell_clicked(self, row, column):
        try:
            myf.on_cell_clicked_f(self.form_interviews, row, column)
        except Exception as e:
            raise Exception(f"Error occurred in on_cell_clicked method: {e}")

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

            self.form_interviews.comboBoxFilterOptions.clear()
            self.filtering_column = logical_index
            self.form_interviews.comboBoxFilterOptions.setPlaceholderText("Filter Area")
            items = myf.filter_active_options(self.filtering_list, logical_index)
            # print('Filtered items: ', items)
            self.form_interviews.comboBoxFilterOptions.addItems(items)
            myf.write2table(self.form_interviews, self.headers, self.active_list)
            self.form_interviews.comboBoxFilterOptions.currentIndexChanged.connect(self.filter_table)

        except Exception as e:
            raise Exception(f"Error occurred in on_header_double_clicked method: {e}")

# ........................................... Presentation Codes END ..................................................#


if __name__ == "__main__":
    app = QApplication([])
    main_window = InterviewsPage(['a', '$2b$12$U67LNgs5U7xNND9PYczCZeVtQl/Hhn6vxACCOxNpmSRjyD2AvKsS2', 'admin', 'Fatih', 'BUYUKAKCALI'])
    main_window.show()
    app.exec()
