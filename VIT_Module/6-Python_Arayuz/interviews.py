import gspread
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (QWidget, QApplication, QMenu, QDialog, QVBoxLayout, QPushButton, QTableWidget, QHBoxLayout)

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
        self.event_ids = None  # Mentor atamasinda Attendee bilgilerinin sheet dosyasina yazilirken karsilastirma icin

        self.form_interviews = Ui_FormInterviews()
        self.form_interviews.setupUi(self)
        self.menu_user = None
        self.menu_admin = None

        # Baslangic ve kalici gorunum ayarlari:
        self.form_interviews.labelInfo1.close()
        self.form_interviews.tableWidget.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft)

        # Initial load view and first filtering column settings
        self.filtering_column = 2
        self.form_interviews.comboBoxFilterOptions.setPlaceholderText("Filtre Alanı")
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
        myf.write2table(self.form_interviews, self.headers, [])  # This code updates the tableWidget headers

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
        self.form_interviews.lineEditSearch.textEdited.connect(self.search_interviews)
        self.form_interviews.lineEditSearch.returnPressed.connect(self.search_interviews)

        # Get unassigned applicants list
        self.form_interviews.pushButtonUnassignedApplicants.clicked.connect(self.mentor_not_assigned_applicants)
        # Connect the combobox signal
        self.normalise_combobox_assigned_applicants_buttons()
        self.form_interviews.comboBoxAssignedApplicants.currentIndexChanged.connect(self.mentor_assigned_applicants)

        self.form_interviews.pushButtonInterviewedApplicants.clicked.connect(self.get_interviewed_applicants)
        self.form_interviews.pushButtonBackMenu.clicked.connect(self.back_menu)
        self.form_interviews.pushButtonExit.clicked.connect(self.app_exit)

        # EXTRA SLOTS:

        # Connect the cellEntered signal to the on_cell_entered method
        self.form_interviews.tableWidget.cellEntered.connect(self.on_cell_entered)
        # myf.disable_cell_entered_signal_f(self.form_interviews, self.on_cell_entered)

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
        self.widgets.append(self.form_interviews.comboBoxAssignedApplicants)  # adding the QComboBox object extra
        myf.handle_widget_styles(self.widgets, self)  # Manage button styles with central function

    def mentor_not_assigned_applicants(self):
        try:
            self.form_interviews.comboBoxFilterOptions.currentIndexChanged.connect(self.filter_table)
            self.normalise_combobox_assigned_applicants_buttons()
            cnf = Config()

            self.headers = [
                "Zaman damgası", "Başvuru dönemi",
                "Ad", "Soyad", "E-Mail", "Telefon", "Posta kodu", "Eyalet",
                "Durumu", "ITPH Talebi", "Ekonomik durumu", "Dil kursu?", "İngilizce", "Hollandaca",
                "Belediye baskısı?", "IT kursu / Bootcamp?", "İnternet IT kursu?", "IT iş tecrübesi?",
                "Başka bir proje?", "IT sektör hayali?", "Neden VIT projesi", "Motivasyonu?", "Basvuran Id"
            ]

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
                  ", " + "b." + cnf.applicationTableFieldNames[1] + " " +
                  "FROM " + cnf.applicationTable + " b " +
                  "INNER JOIN " + cnf.applicantTable + " a ON b." + cnf.applicationTableFieldNames[0] +
                  " = a." + cnf.applicantTableFieldNames[0] + " " +
                  "WHERE b." + cnf.applicationTableFieldNames[3] +
                  " = %s AND b." + cnf.applicationTableFieldNames[18] + " = 0 " +
                  "ORDER BY b." + cnf.applicationTableFieldNames[2] + " ASC")

            not_appointed = myf.execute_read_query(cnf.open_conn(), q1, (myf.last_period(),))

            # Rebuilds the list based on the data type of the cells.
            self.active_list = myf.remake_it_with_types(not_appointed)

            # Write to tableWidget: applicants who have not been assigned a mentor
            myf.write2table(self.form_interviews, self.headers, self.active_list)
            myf.resize_columns(self.form_interviews.tableWidget)

            # Activate the Assign Mentor context menu only in this case
            # myf.enable_context_menu(self.form_interviews, self.show_context_menu_assign_mentor)

            # Fill the combobox for filtering while loading
            self.filtering_list = list(self.active_list)  # Assigned for filtering.
            self.filtering_column = 2
            self.form_interviews.comboBoxFilterOptions.clear()
            items = myf.filter_active_options(self.filtering_list, self.filtering_column)
            self.form_interviews.comboBoxFilterOptions.addItems(items)
        except Exception as e:
            raise Exception(f"Error occurred in mentor_not_assigned_applicants method: {e}")

    def show_context_menu_assign_mentor(self, pos):
        try:
            item = self.form_interviews.tableWidget.itemAt(pos)
            if item is None or self.form_interviews.tableWidget.rowCount() == 0:
                return  # Eğer geçerli bir öğe yoksa veya tablo boşsa, hiçbir şey yapma

            self.form_interviews.tableWidget.selectRow(item.row())

            context_menu = QMenu(self)
            show_assign_mentor_action = context_menu.addAction("Assign Mentor")
            action = context_menu.exec(self.form_interviews.tableWidget.viewport().mapToGlobal(pos))

            if action == show_assign_mentor_action:
                self.show_open_appointments()
        except Exception as e:
            raise Exception(f"Error occurred in show_context_menu_assign_mentor method: {e}")

    def show_open_appointments(self):
        try:
            # Disable Assign Mentor context menu
            # myf.disable_context_menu(self.form_interviews, self.show_context_menu_assign_mentor)

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

            # Kapat butonunun genişliğini sınırlamak için maksimum genişliği ayarlayabilirsiniz
            close_button = QPushButton("Kapat")
            close_button.setMaximumWidth(150)  # Maksimum genişliği 150 piksel ile sınırlıyoruz
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

            # myf.enable_context_menu(self.form_interviews, self.show_context_menu_assign_mentor)
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
            # Disable Assign Mentor context menu
            # myf.disable_context_menu(self.form_interviews, self.show_context_menu_assign_mentor)

            cnf = Config()
            reply = QMessageBox.question(self, 'Mentor Atama', 'Bu randevuya mentor atamak istiyor musunuz?',
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                # Seçili satırın BasvuranID'sini al
                current_row = self.form_interviews.tableWidget.currentRow()
                basvuran_id = self.form_interviews.tableWidget.item(current_row, 22).text()

                # Veritabanında güncelleme yap
                q1 = ("UPDATE " + cnf.appointmentsTable + " SET " + cnf.appointmentsTableFieldNames[12] + " = %s " +
                      "WHERE " + cnf.appointmentsTableFieldNames[2] + " = %s")
                myf.execute_query(cnf.open_conn(), q1, (basvuran_id, event_id))

                q2 = ("UPDATE " + cnf.applicationTable + " SET " + cnf.applicationTableFieldNames[18] + " = 1 WHERE "
                      + cnf.applicationTableFieldNames[3] + " = %s AND " + cnf.applicantTableFieldNames[0] + " = %s")
                myf.execute_query(cnf.open_conn(), q2, (myf.last_period(), basvuran_id))

                # Basvuranın adını, soyadını ve email'ini veritabanından çekip Google Sheet'e yazdırıyoruz.
                applicant_query = (
                        "SELECT " + cnf.applicantTableFieldNames[2] + ", " + cnf.applicantTableFieldNames[3] +
                        ", " + cnf.applicantTableFieldNames[4] + " " +
                        "FROM " + cnf.applicantTable + " WHERE " + cnf.applicantTableFieldNames[0] + " = %s")
                applicant_data = myf.execute_read_query(cnf.open_conn(), applicant_query, (basvuran_id,))
                attendee_name, attendee_surname, attendee_email = applicant_data[0]

                self.update_first_interview_sheet(event_id, attendee_name, attendee_surname, attendee_email)

                QMessageBox.information(self, 'Başarılı', 'Mentor başarıyla atandı.')

                # Dialog'u kapat
                self.sender().parent().close()

                # Tabloyu güncelle
                self.mentor_not_assigned_applicants()
        except Exception as e:
            raise Exception(f"Error occurred in assign_mentor method: {e}")

    # Gspread kullanarak FirstInterview sheetine bağlantı kuran metot
    def update_first_interview_sheet(self, event_id, attendee_name, attendee_surname, attendee_email):
        try:
            # Google Sheet dosyasını aç
            sheet = self.client.open(self.google_first_interview_sheet_name).sheet1

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
            raise Exception(f"Error occurred in update_first_interview_sheet method: {e}")

    def mentor_assigned_applicants(self):
        try:
            self.form_interviews.comboBoxFilterOptions.currentIndexChanged.connect(self.filter_table)
            cnf = Config()
            self.normalise_combobox_filter_options()
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

            # Disable Assign Mentor context menu
            # myf.disable_context_menu(self.form_interviews, self.show_context_menu_assign_mentor)  # assign mentor yazisini gidermek icin koydugum son kod. basarisiz ise silebilirsin

            # Applicants who have been assigned a mentor
            myf.write2table(self.form_interviews, self.headers, self.active_list)

            # Fill the combobox for filtering while loading
            self.filtering_list = list(self.active_list)
            self.filtering_column = 1
            self.form_interviews.comboBoxFilterOptions.clear()
            items = myf.filter_active_options(self.filtering_list, self.filtering_column)
            self.form_interviews.comboBoxFilterOptions.addItems(items)

            # Disable Assign Mentor context menu
            # myf.disable_context_menu(self.form_interviews, self.show_context_menu_assign_mentor)
        except Exception as e:
            raise Exception(f"Error occurred in mentor_assigned_applicants method: {e}")

    # Ilk mulakati yapilmis basvuranlarin listelenmesi
    def get_interviewed_applicants(self):
        try:
            self.form_interviews.comboBoxFilterOptions.currentIndexChanged.connect(self.filter_table)
            cnf = Config()
            self.normalise_combobox_assigned_applicants_buttons()

            self.headers = ['Zaman damgası', 'Başvuru Dönemi', 'Mentor Ad', 'Mentor Soyad', 'Mentor Mail',
                            'Başvuran Ad', 'Başvuran Soyad', 'Başvuran Mail', 'Başvuran IT sektör bilgisi',
                            'Başvuran Yoğunluk', 'Düşünceler', 'Yorumlar']

            q1 = ("SELECT "
                  "fe.crm_ID, fe.crm_Timestamp, fe.crm_Period, ac.crm_MentorName, ac.crm_MentorSurname, ac.crm_MentorMail, "
                  "fa.crm_Name, fa.crm_Surname, fa.crm_Email, fe.crm_ITSkills, fe.crm_Availability, fe.crm_Recommendation, "
                  "fe.crm_Comment, crm_IsApplicantACandidate "
                  "FROM form2_evaluations fe "
                  "LEFT JOIN appointments_current ac ON fe.crm_MentorMail = ac.crm_MentorMail "
                  "INNER JOIN form1_applicant fa ON fe.crm_ApplicantID = fa.crm_ID "
                  "WHERE fe.crm_Period = %s "
                  "GROUP BY "
                  "fe.crm_ID, fe.crm_Timestamp, fe.crm_Period, ac.crm_MentorName, ac.crm_MentorSurname, ac.crm_MentorMail, "
                  "fa.crm_Name, fa.crm_Surname, fa.crm_Email, fe.crm_ITSkills, fe.crm_Availability, fe.crm_Recommendation, "
                  "fe.crm_Comment, crm_IsApplicantACandidate")

            applicants = myf.execute_read_query(cnf.open_conn(), q1, (myf.last_period(),))

            # Veriyi tabloya ekle
            self.applicants = myf.remake_it_with_types(applicants)
            self.active_list = list([row[1:] for row in self.applicants])  # ID ve en son sutun hariç diğer verileri ata

            myf.write2table(self.form_interviews, self.headers, self.active_list)

            # Enable Add to Candidates context menu
            # myf.enable_context_menu(self.form_interviews, self.show_context_menu_add_to_candidates)  # Sağ tıklayınca 'Add to Candidates' menüsü aktif edildi

            # Filtreleme için combobox'u doldur
            self.filtering_list = list(self.active_list)  # Filtreleme için atandı
            self.filtering_column = 10
            self.form_interviews.comboBoxFilterOptions.clear()
            items = myf.filter_active_options(self.filtering_list, self.filtering_column)
            self.form_interviews.comboBoxFilterOptions.addItems(items)
            self.form_interviews.comboBoxFilterOptions.setPlaceholderText(
                "Katılımcı Hakkındaki Tavsiyelere Göre Filtrele")

            # Yeşil renklendirme işlemi
            self.highlight_candidates()

        except Exception as e:
            raise Exception(f"Error occurred in get_interviewed_applicants method: {e}")

    def show_context_menu_add_to_candidates(self, pos):
        try:
            item = self.form_interviews.tableWidget.itemAt(pos)
            if item is None or self.form_interviews.tableWidget.rowCount() == 0:
                return  # Eğer geçerli bir öğe yoksa veya tablo boşsa, hiçbir şey yapma

            self.form_interviews.tableWidget.selectRow(item.row())

            context_menu = QMenu(self)
            add_candidate_action = context_menu.addAction("Add to Candidates")
            action = context_menu.exec(self.form_interviews.tableWidget.viewport().mapToGlobal(pos))

            if action == add_candidate_action:
                value = self.form_interviews.tableWidget.item(item.row(),
                                                              7)  # Basvuranin mail adresinin bulundugu sutun = 7
                applicant_mail = value.text()
                if value is not None:
                    self.add_to_candidates(applicant_mail)
        except Exception as e:
            raise Exception(f"Error occurred in show_context_menu_add_to_candidates method: {e}")

    def add_to_candidates(self, applicant_email):
        try:
            # Disable Add to Candidates context menu
            # myf.disable_context_menu(self.form_interviews, self.show_context_menu_add_to_candidates)

            # Secilen satirin listedeki gercek ID degerini bul
            crm_id = None
            mentor_mail = None
            isApplicant = None
            for element in self.applicants:
                if element[8] == applicant_email:
                    crm_id = element[0]
                    mentor_mail = element[5]
                    isApplicant = element[13]

            cnf = Config()
            reply = QMessageBox.question(self, 'Aday Belirleme/Ekleme',
                                         'Bu basvurani aday olarak belirlemek istiyor musunuz?',
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes and crm_id:
                if isApplicant != 1:
                    # Veritabanında güncelleme yap
                    q1 = ("UPDATE " + cnf.evaluationTable + " SET " + cnf.evaluationTableFieldNames[13] + " = 1 WHERE "
                          + cnf.evaluationTableFieldNames[2] + " = %s AND " + cnf.evaluationTableFieldNames[
                              0] + " = %s")

                    last_period = myf.last_period()
                    myf.execute_query(cnf.open_conn(), q1, (last_period, crm_id))

                    self.update_applicant_evaluations_sheet(last_period, mentor_mail, applicant_email)

                    QMessageBox.information(self, 'Bilgi:', 'Secilen kayit, Aday olarak belirlendi.')

                    # Tabloyu güncelle
                    self.get_interviewed_applicants()
                else:
                    QMessageBox.information(self, 'Bilgi:', 'Secilen kayit zaten daha onceden aday olarak belirlendi.')

        except Exception as e:
            raise Exception(f"Error occurred in add_to_candidates method: {e}")

    # Gspread kullanarak ApplicantEvaluations sheetine bağlantı kuran metot
    def update_applicant_evaluations_sheet(self, last_period, mentor_mail, applicant_mail):
        try:
            # Google Sheet dosyasını aç
            sheet = self.client.open(self.google_applicant_evaluations_sheet_name).sheet1

            # Sadece 1, 2 ve 3. sütunlardaki verileri al
            column_data = sheet.get('B:D')  # B'dan D'ye kadar olan sütunları alır

            for row_index, element in enumerate(column_data, start=1):
                if element[0] == last_period and element[1] == mentor_mail and element[2] == applicant_mail:
                    # 9. sütuna (I sütunu) 1 değerini yaz
                    sheet.update_cell(row_index, 9, 1)  # row_index satırı, 9. sütunu günceller
                    # alttaki kodu devredisi biraktim. boylece tekrar eden satirlar da guncellenecek
                    # break  # İlgili satır bulunduğunda döngüden çık

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
        self.normalise_combobox_filter_options()

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

    # Method to automatically adjust the display settings of the comboBoxAssignedApplicants object
    def normalise_combobox_assigned_applicants_buttons(self):
        try:
            self.form_interviews.comboBoxAssignedApplicants.clear()
            self.form_interviews.comboBoxAssignedApplicants.setPlaceholderText('Assigned Applicants')
            self.form_interviews.comboBoxAssignedApplicants.addItems(['Last Period', 'All Periods'])

            self.form_interviews.comboBoxFilterOptions.clear()
            self.form_interviews.comboBoxFilterOptions.setPlaceholderText("Filtre Alani")
        except Exception as e:
            raise Exception(f"Error occurred in normalise_combobox_assigned_applicants_buttons method: {e}")

    # Method to automatically adjust the display settings of the comboBoxFilterOptions object
    def normalise_combobox_filter_options(self):
        try:
            self.form_interviews.comboBoxFilterOptions.clear()
            self.form_interviews.comboBoxFilterOptions.setPlaceholderText("Filtre Alani")
        except Exception as e:
            raise Exception(f"Error occurred in normalise_combobox_filter_options method: {e}")

    # Aday olarak belirlenmis kayitlarin renkli satirlarla gosterilmesi icin kod
    def highlight_candidates(self):
        try:
            for i, row_data in enumerate(self.applicants):
                # row_data[-1] değeri crm_IsApplicantACandidate verisi
                if row_data[-1] >= 1:  # Eğer crm_IsApplicantACandidate 1 veya 1 den buyukse
                    for col in range(self.form_interviews.tableWidget.columnCount()):
                        item = self.form_interviews.tableWidget.item(i, col)
                        if item:  # Eğer item mevcutsa
                            item.setBackground(QColor('green'))  # Arka plan rengini yeşil yap
        except Exception as e:
            raise Exception(f"Error occurred in highlight_candidates method: {e}")

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
            self.form_interviews.comboBoxFilterOptions.setPlaceholderText("Filtre Alani")
            items = myf.filter_active_options(self.filtering_list, logical_index)
            # print('Filtered items: ', items)
            self.form_interviews.comboBoxFilterOptions.addItems(items)
            myf.write2table(self.form_interviews, self.headers, self.active_list)
            self.form_interviews.comboBoxFilterOptions.currentIndexChanged.connect(self.filter_table)

        except Exception as e:
            raise Exception(f"Error occurred in on_header_double_clicked method: {e}")


from PyQt6.QtCore import QObject, QEvent
from PyQt6.QtWidgets import QComboBox, QMessageBox


class HoverEventFilter(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.hover_style = None  # Hover stili burada saklanacak

    def eventFilter(self, watched, event):
        if isinstance(watched, QComboBox):
            if event.type() == QEvent.Type.HoverEnter:
                # Hover stili al ve sakla
                self.hover_style = watched.styleSheet()
                print(f"Hovering over: {watched.objectName()}")
                print(f"Current Style Sheet:\n{self.hover_style}")

            elif event.type() == QEvent.Type.HoverLeave:
                # Hover stili kaybolur, ancak burada stil bilgisi saklanır
                print(f"Leaving: {watched.objectName()}")

        return super().eventFilter(watched, event)

    def apply_hover_style(self, combo_box):
        if self.hover_style:
            # Hover stilini combo_box'a uygula
            combo_box.setStyleSheet(self.hover_style)


# ........................................... Presentation Codes END ..................................................#


if __name__ == "__main__":
    app = QApplication([])
    main_window = InterviewsPage(('a', 'b', 'admin'))
    main_window.show()
    app.exec()
