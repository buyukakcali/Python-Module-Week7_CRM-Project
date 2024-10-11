import gspread
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (QWidget, QApplication, QMenu, QDialog, QVBoxLayout, QPushButton, QTableWidget, QHBoxLayout,
                             QMessageBox, QComboBox)

from UI_Files.interviews_ui import Ui_FormInterviews
import my_functions as myf
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
        self.filtering_column = 2
        self.form_interviews.comboBoxFilterOptions.setPlaceholderText("Filter Area")
        self.headers = [
            "Zaman damgası", "Başvuru dönemi", "Ad", "Soyad", "E-Mail", "Telefon", "Posta kodu", "Eyalet", "Durumu",
            "ITPH Talebi", "Ekonomik durumu", "Dil kursu?", "İngilizce", "Hollandaca", "Belediye baskısı?",
            "IT kursu / Bootcamp?", "İnternet IT kursu?", "IT iş tecrübesi?", "Başka bir proje?", "IT sektör hayali?",
            "Neden VIT projesi", "Motivasyonu?", "Id", "Situation"
        ]
        myf.write2table(self.form_interviews, self.headers, [])  # This code updates the tableWidget headers


        # Connect signals to slots
        self.form_interviews.lineEditSearch.textEdited.connect(self.search_interviews)
        self.form_interviews.lineEditSearch.returnPressed.connect(self.search_interviews)
        self.form_interviews.pushButtonUnassignedApplicants.clicked.connect(self.mentor_not_assigned_applicants)
        self.form_interviews.pushButtonAssignedApplicants.clicked.connect(self.mentor_assigned_applicants)
        self.form_interviews.pushButtonInterviewedApplicants.clicked.connect(self.get_interviewed_applicants)
        self.form_interviews.comboBoxFilterOptions.currentIndexChanged.connect(self.filter_table_interviews)
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

        # The display settings of the last clicked objects are determined.
        self.widgets = self.findChildren(QPushButton)  # Find all buttons of type QPushButton & assign them to the list
        self.widgets.extend(self.findChildren(QComboBox))   # Extend the list with QCombobox objects
        myf.handle_widget_styles(self, self.widgets)  # Manage button styles with central function

    # Shows applications that have not yet been assigned a first interview appointment.
    def mentor_not_assigned_applicants(self):
        try:
            myf.disable_cell_entered_signal_f(self.form_interviews, self.on_cell_entered)
            myf.disable_context_menu(self.form_interviews, self.show_context_menu_add_to_candidates)  # first disable
            myf.enable_context_menu(self.form_interviews, self.show_context_menu_assign_mentor)  # then enable
            myf.normalise_combo_boxes([None, self.form_interviews.comboBoxFilterOptions])

            cnf = Config()

            self.headers = [
                "Zaman damgası", "Başvuru dönemi",
                "Ad", "Soyad", "E-Mail", "Telefon", "Posta kodu", "Eyalet",
                "Durumu", "ITPH Talebi", "Ekonomik durumu", "Dil kursu?", "İngilizce", "Hollandaca",
                "Belediye baskısı?", "IT kursu / Bootcamp?", "İnternet IT kursu?", "IT iş tecrübesi?",
                "Başka bir proje?", "IT sektör hayali?", "Neden VIT projesi", "Motivasyonu?", "Id", "Situation"]

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
                  ", " + "b." + cnf.applicationTableFieldNames[18] + " " +
                  "FROM " + cnf.applicationTable + " b " +
                  "INNER JOIN " + cnf.applicantTable + " a ON b." + cnf.applicationTableFieldNames[0] +
                  " = a." + cnf.applicantTableFieldNames[0] + " " +
                  "WHERE b." + cnf.applicationTableFieldNames[3] +
                  " = %s AND b." + cnf.applicationTableFieldNames[18] + " <= 1 " +
                  "ORDER BY b." + cnf.applicationTableFieldNames[2] + " ASC")
            # q1 = ("SELECT b.crm_Timestamp, b.crm_Period, a.crm_Name, a.crm_Surname, a.crm_Email, a.crm_Phone, "
            #       "a.crm_PostCode, a.crm_Province, b.crm_SuAnkiDurum, b.crm_ITPHEgitimKatilmak, b.crm_EkonomikDurum, "
            #       "b.crm_DilKursunaDevam, b.crm_IngilizceSeviye, b.crm_HollandacaSeviye, b.crm_BaskiGoruyor, "
            #       "b.crm_BootcampBitirdi, b.crm_OnlineITKursu, b.crm_ITTecrube, b.crm_ProjeDahil, "
            #       "b.crm_CalismakIstedigi, b.crm_NedenKatilmakIstiyor, b.crm_MotivasyonunNedir, b.crm_ApplicantID, "
            #       "b.crm_FirstInterview "
            #       "FROM form1_application b "
            #       "INNER JOIN form1_applicant a ON b.crm_ID = a.crm_ID "
            #       "WHERE b.crm_Period = %s AND b.crm_FirstInterview <= 1 "
            #       "ORDER BY b.crm_Timestamp ASC")

            not_appointed = myf.execute_read_query(cnf.open_conn(), q1, (myf.last_period(),))

            # Rebuilds the list based on the data type of the cells.
            self.active_list = myf.remake_it_with_types(not_appointed)

            # Write to tableWidget: applicants who have not been assigned a mentor
            myf.write2table(self.form_interviews, self.headers, self.active_list)

            # Fill the combobox for filtering while loading
            self.form_interviews.comboBoxFilterOptions.clear()
            self.filtering_list = list(self.active_list)  # Assigned for filtering.
            self.filtering_column = 2
            items = myf.filter_active_options(self.filtering_list, self.filtering_column)
            self.form_interviews.comboBoxFilterOptions.addItems(items)

            # tableWidget line coloring process
            # The called function paints the background of the records with the specified color.
            myf.highlight_candidates(self.form_interviews, 23, 1, 'white', QColor("#FF5733"))

        except Exception as e:
            raise Exception(f"Error occurred in mentor_not_assigned_applicants method: {e}")

    # Adding context menu to right-click
    def show_context_menu_assign_mentor(self, pos):
        try:
            # Control to handle right click only
            if not self.form_interviews.tableWidget.viewport().underMouse():
                return

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
                self.get_open_appointments()
        except Exception as e:
            raise Exception(f"Error occurred in show_context_menu_assign_mentor method: {e}")

    # Lists available appointments
    def get_open_appointments(self):
        try:
            current_row = self.form_interviews.tableWidget.currentRow()
            if int(self.form_interviews.tableWidget.item(current_row, 23).text()) > 0:
                header = "Warning:"
                message_text = "The applicant has already been assigned a mentor!"
                myf.set_info_dialog(self, header, message_text)
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
                      "WHERE " + cnf.appointmentsTableFieldNames[7] + " LIKE '1%' " +
                      "AND " + cnf.appointmentsTableFieldNames[12] + " is null " +
                      "ORDER BY " + cnf.appointmentsTableFieldNames[3] + " ASC")
                # q1 = ("SELECT crm_InterviewDatetime, crm_MentorName, crm_MentorSurname, crm_MentorMail, crm_Summary, "
                #       "crm_Description, crm_Location, crm_OnlineMeetingLink, crm_EventID "
                #       "FROM appointments_current "
                #       "WHERE crm_Summary LIKE '1%' AND crm_AttendeeID is null "
                #       "ORDER BY crm_InterviewDatetime ASC")

                open_appointments = myf.execute_read_query(cnf.open_conn(), q1)
                self.open_appointments = myf.remake_it_with_types(open_appointments)

                dialog = QDialog(self)
                dialog.setWindowTitle("Available Appointments")
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
                close_button = QPushButton("Close")
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
            raise Exception(f"Error occurred in get_open_appointments method: {e}")

    # It is used in get_open_appointments(function above). It was actually separated to reduce code complexity
    def on_appointment_selected(self, row: int):
        try:
            event_id = self.open_appointments[row][8]
            self.assign_mentor(event_id)
        except Exception as e:
            raise Exception(f"Error occurred in on_appointment_selected method: {e}")

    # Assigns the appropriate selected appointment to the selected row (or vice versa)
    def assign_mentor(self, event_id: str):
        try:
            # # Disable context menu for blocking the unwanted context menu showing after assigning
            # myf.disable_context_menu(self.form_interviews, self.show_context_menu_assign_mentor)

            cnf = Config()
            reply = QMessageBox.question(self, 'Mentor Assignment',
                                         'Do you want to assign a mentor to this appointment?',
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                # Get the ApplicantID of the selected row
                current_row = self.form_interviews.tableWidget.currentRow()
                applicant_id = self.form_interviews.tableWidget.item(current_row, 22).text()

                # Update the database
                q1 = ("UPDATE " + cnf.appointmentsTable + " SET " + cnf.appointmentsTableFieldNames[12] + " = %s " +
                      "WHERE " + cnf.appointmentsTableFieldNames[2] + " = %s")
                # q1 = "UPDATE appointments_current SET crm_AttendeeID = %s WHERE crm_EventID = %s"
                myf.execute_write_query(cnf.open_conn(), q1, (applicant_id, event_id))

                q2 = ("UPDATE " + cnf.applicationTable + " SET " + cnf.applicationTableFieldNames[18] + " = 1 WHERE "
                      + cnf.applicationTableFieldNames[3] + " = %s AND " + cnf.applicantTableFieldNames[0] + " = %s")
                # q2 = "UPDATE form1_application SET crm_FirstInterview = 1 WHERE crm_Period = %s AND crm_ID = %s"
                myf.execute_write_query(cnf.open_conn(), q2, (myf.last_period(), applicant_id))

                # We extract the applicant's name, surname and email from the database and print it on Google Sheet.
                applicant_query = (
                        "SELECT " + cnf.applicantTableFieldNames[2] + ", " + cnf.applicantTableFieldNames[3] +
                        ", " + cnf.applicantTableFieldNames[4] + " " +
                        "FROM " + cnf.applicantTable + " WHERE " + cnf.applicantTableFieldNames[0] + " = %s")
                applicant_data = myf.execute_read_query(cnf.open_conn(), applicant_query, (applicant_id,))
                attendee_name, attendee_surname, attendee_email = applicant_data[0]
                # applicant_query = "SELECT crm_Name, crm_Surname, crm_Email FROM form1_applicant WHERE crm_ID = %s"

                myf.update_events_all_interviews_sheet(event_id, attendee_name, attendee_surname, attendee_email)

                QMessageBox.information(self, 'Successful', 'Mentor successfully assigned.')

                # Close dialog
                self.sender().parent().close()

                # Update tableWidget
                self.mentor_not_assigned_applicants()
        except Exception as e:
            raise Exception(f"Error occurred in assign_mentor method: {e}")

    # Lists applications for which a mentor has been assigned,
    # or -in other words- an interview appointment has been given.
    def mentor_assigned_applicants(self):
        try:
            myf.re_enable_cell_entered_signal_f(self.form_interviews, self.on_cell_entered)
            myf.disable_context_menu(self.form_interviews, self.show_context_menu_add_to_candidates)  # always disable
            myf.disable_context_menu(self.form_interviews, self.show_context_menu_assign_mentor)  # always disable
            myf.normalise_combo_boxes([None, self.form_interviews.comboBoxFilterOptions])

            cnf = Config()
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
            # q1 = ("SELECT b.crm_InterviewDatetime, a.crm_Name, a.crm_Surname, a.crm_Email, b.crm_MentorName, "
            #       "b.crm_MentorSurname, b.crm_MentorMail, b.crm_Summary, b.crm_Description, b.crm_Location, "
            #       "b.crm_OnlineMeetingLink, b.crm_ResponseStatus "
            #       "FROM appointments_current b "
            #       "INNER JOIN form1_applicant a ON b.crm_AttendeeID = a.crm_ID "
            #       "WHERE b.crm_ID is not null AND b.crm_Summary LIKE '1%' "
            #       "ORDER BY b.crm_InterviewDatetime ASC")

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
            myf.disable_cell_entered_signal_f(self.form_interviews, self.on_cell_entered)
            myf.disable_context_menu(self.form_interviews, self.show_context_menu_assign_mentor)  # first disable
            myf.enable_context_menu(self.form_interviews, self.show_context_menu_add_to_candidates)  # then enable
            myf.normalise_combo_boxes([None, self.form_interviews.comboBoxFilterOptions])

            cnf = Config()

            self.headers = ['Zaman damgası', 'Başvuru Dönemi', 'Başvuran Ad', 'Başvuran Soyad', 'Başvuran Mail',
                            'Mentor Ad', 'Mentor Soyad', 'Mentor Mail','Başvuran IT sektör bilgisi',
                            'Başvuran Yoğunluk', 'Düşünceler', 'Yorumlar', "Situation"]

            q1 = ("SELECT "
                  "fe." + cnf.evaluationTableFieldNames[0] + ", fe." + cnf.evaluationTableFieldNames[1] +
                  ", fe." + cnf.evaluationTableFieldNames[2] + ", fa." + cnf.applicantTableFieldNames[2] +
                  ", fa." + cnf.applicantTableFieldNames[3] + ", fa." + cnf.applicantTableFieldNames[4] +
                  ", ac." + cnf.appointmentsTableFieldNames[4] + ", ac." + cnf.appointmentsTableFieldNames[5] +
                  ", ac." + cnf.appointmentsTableFieldNames[6] + ", fe." + cnf.evaluationTableFieldNames[7] +
                  ", fe." + cnf.evaluationTableFieldNames[8] + ", fe." + cnf.evaluationTableFieldNames[9] +
                  ", fe." + cnf.evaluationTableFieldNames[10] + ", fe." + cnf.evaluationTableFieldNames[12] + " " +
                  "FROM " + cnf.evaluationTable + " fe " +
                  "LEFT JOIN " + cnf.appointmentsTable + " ac " +
                  "ON fe." + cnf.evaluationTableFieldNames[5] + " = ac." + cnf.appointmentsTableFieldNames[6] + " "
                  "INNER JOIN " + cnf.applicantTable + " fa " +
                  "ON fe." + cnf.evaluationTableFieldNames[6] + " = fa." + cnf.applicantTableFieldNames[0] + " " +
                  "WHERE fe." + cnf.evaluationTableFieldNames[2] + " = %s " +
                  "GROUP BY "
                  "fe." + cnf.evaluationTableFieldNames[0] + ", fe." + cnf.evaluationTableFieldNames[1] +
                  ", fe." + cnf.evaluationTableFieldNames[2] + ", fa." + cnf.applicantTableFieldNames[2] +
                  ", fa." + cnf.applicantTableFieldNames[3] + ", fa." + cnf.applicantTableFieldNames[4] +
                  ", ac." + cnf.appointmentsTableFieldNames[4] + ", ac." + cnf.appointmentsTableFieldNames[5] +
                  ", ac." + cnf.appointmentsTableFieldNames[6] + ", fe." + cnf.evaluationTableFieldNames[7] +
                  ", fe." + cnf.evaluationTableFieldNames[8] + ", fe." + cnf.evaluationTableFieldNames[9] +
                  ", fe." + cnf.evaluationTableFieldNames[10] + ", fe." + cnf.evaluationTableFieldNames[12])
            # q1 = ("SELECT "
            #       "fe.crm_ID, fe.crm_Timestamp, fe.crm_Period, fa.crm_Name, fa.crm_Surname, fa.crm_Email, "
            #       "ac.crm_MentorName, ac.crm_MentorSurname, ac.crm_MentorMail, fe.crm_ITSkills, fe.crm_Availability, "
            #       "fe.crm_Recommendation, fe.crm_Comment, crm_IsApplicantACandidate "
            #       "FROM form2_evaluations fe "
            #       "LEFT JOIN appointments_current ac ON fe.crm_MentorMail = ac.crm_MentorMail "
            #       "INNER JOIN form1_applicant fa ON fe.crm_ApplicantID = fa.crm_ID "
            #       "WHERE fe.crm_Period = %s "
            #       "GROUP BY "
            #       "fe.crm_ID, fe.crm_Timestamp, fe.crm_Period, fa.crm_Name, fa.crm_Surname, fa.crm_Email, "
            #       "ac.crm_MentorName, ac.crm_MentorSurname, ac.crm_MentorMail, fe.crm_ITSkills, fe.crm_Availability, "
            #       "fe.crm_Recommendation, fe.crm_Comment, crm_IsApplicantACandidate")

            applicants = myf.execute_read_query(cnf.open_conn(), q1, (myf.last_period(),))

            # Fill the tableWidget
            self.applicants = myf.remake_it_with_types(applicants)
            self.active_list = list([row[1:] for row in self.applicants])  # Assign other data except ID

            myf.write2table(self.form_interviews, self.headers, self.active_list)

            # Fill combobox for filtering
            self.filtering_list = list(self.active_list)  # Assigned for filtering
            self.filtering_column = 10
            self.form_interviews.comboBoxFilterOptions.clear()
            items = myf.filter_active_options(self.filtering_list, self.filtering_column)
            self.form_interviews.comboBoxFilterOptions.addItems(items)
            self.form_interviews.comboBoxFilterOptions.setPlaceholderText(
                "Filter by Recommendations About Participant")

            # tableWidget line coloring process
            # The function called shows the records determined as candidates with colored lines
            myf.highlight_candidates(
                self.form_interviews, 12, 1, 'white', QColor(123, 104, 238))

            myf.highlight_candidates(
                self.form_interviews, 12, 2, 'white', QColor(123, 104, 238))
        except Exception as e:
            raise Exception(f"Error occurred in get_interviewed_applicants method: {e}")

    # Adding context menu to right-click
    def show_context_menu_add_to_candidates(self, pos):
        try:
            # Control to handle right click only
            if not self.form_interviews.tableWidget.viewport().underMouse():
                return

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
            add_candidate_action = context_menu.addAction("Add to Candidates")
            action = context_menu.exec(self.form_interviews.tableWidget.viewport().mapToGlobal(pos))

            if action == add_candidate_action:
                # Column containing the applicant's e-mail address = 4
                value = self.form_interviews.tableWidget.item(item.row(), 4)
                applicant_mail = value.text()
                if value is not None:
                    self.add_to_candidates(applicant_mail)
        except Exception as e:
            raise Exception(f"Error occurred in show_context_menu_add_to_candidates method: {e}")

    # Registers the applicant as a candidate
    def add_to_candidates(self, applicant_email: str):
        try:
            # Find the actual ID value of the selected row in the list
            crm_id = None
            mentor_mail = None
            isApplicantACandidate = None

            for element in self.applicants:
                if element[5] == applicant_email:
                    crm_id = element[0]
                    mentor_mail = element[8]
                    isApplicantACandidate = element[13]

            if isApplicantACandidate > 0:
                header = "Warning:"
                message_text = "The applicant has already assigned as a Candidate!"
                myf.set_info_dialog(self, header, message_text)
                return

            cnf = Config()
            reply = QMessageBox.question(self, 'Assigning / Registering Candidates:',
                                             'Do you want to register this applicant as a candidate?',
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes and crm_id:
                # If the applicant has not already been assigned as a candidate, update the database
                if isApplicantACandidate != 1:
                    q1 = ("UPDATE " + cnf.evaluationTable + " SET " + cnf.evaluationTableFieldNames[12] + " = 1 " +
                          "WHERE " + cnf.evaluationTableFieldNames[2] + " = %s " +
                          "AND " + cnf.evaluationTableFieldNames[0] + " = %s")
                    # q1 = ("UPDATE form2_evaluations SET crm_IsApplicantACandidate = 1 " +
                    #       "WHERE crm_Period = %s AND crm_ID = %s")

                    last_period = myf.last_period()
                    myf.execute_write_query(cnf.open_conn(), q1, (last_period, crm_id))

                    self.update_applicant_evaluations_sheet(last_period, mentor_mail, applicant_email)

                    QMessageBox.information(self, 'Info:', 'The selected record was assigned as Candidate.')

                    # Update tableWidget
                    self.get_interviewed_applicants()
                else:
                    QMessageBox.information(self, 'Info:',
                                            'The selected record has already been assigned as a Candidate before!')

        except Exception as e:
            raise Exception(f"Error occurred in add_to_candidates method: {e}")

    # Method to connect to 3-Application_Evaluations_Form_Answers sheet using gspread
    @staticmethod
    def update_applicant_evaluations_sheet(last_period: str, mentor_mail: str, applicant_mail: str):
        try:
            cnf = Config()
            # Open Google Sheet file
            # 3-Application_Evaluations_Form_Answers sheet
            google_applicant_evaluations_sheet_name = cnf.google_applicant_evaluations_sheet_name
            sheet = myf.connect_to_google_sheets(google_applicant_evaluations_sheet_name)

            # Get data in columns 1, 2 and 3 only
            column_data = sheet.get('B:D')  # Gets columns B through D

            for row_index, element in enumerate(column_data, start=1):
                if element[0] == last_period and element[1] == mentor_mail and element[2] == applicant_mail:
                    # Write the value 1 in column 10(column J)
                    sheet.update_cell(row_index, 10, 1)
                    # # row_index updates the row, 10th column, J disabled the code below.
                    # # So repeating lines will also be updated
                    # break # Exit the loop when the relevant row is found
        except gspread.SpreadsheetNotFound:
            print("Spreadsheet not found. Please make sure the file name is correct.")
        except gspread.WorksheetNotFound:
            print("Worksheet not found. Please make sure the page name is correct.")
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
        try:
            myf.normalise_combo_boxes([None, self.form_interviews.comboBoxFilterOptions])

            # If there is active_list, update filtering_list
            if self.active_list:
                self.filtering_list = list(self.active_list)  # Assign the list for filtering.

            searched_text = self.form_interviews.lineEditSearch.text()  # Get text in search field

            # Get results
            self.filtering_list = myf.search(self.filtering_list, self.headers, self.filtering_column, searched_text)

            # Write the results to the tableWidget
            myf.write2table(self.form_interviews, self.headers, self.filtering_list)

            # Fill the combobox for filtering after every single search
            if self.active_list:
                self.filtering_list = list(self.active_list)
                items = myf.filter_active_options(self.filtering_list, self.filtering_column)
                self.form_interviews.comboBoxFilterOptions.addItems(items)
        except Exception as e:
            raise Exception(f"Error occurred in search_interviews method: {e}")

    # Filter settings for InterviewsPage
    def filter_table_interviews(self):
        try:
            self.form_interviews.lineEditSearch.clear()  # clear the search box
            myf.filter_table(self.form_interviews, self.headers, self.filtering_list, self.filtering_column)
        except Exception as e:
            raise Exception(f"Error occurred in filter_table_interviews method: {e}")

    # .................................................................................................................#
    # .......................................... PRESENTATION CODES START .............................................#
    # .................................................................................................................#

    # This code is written to make the contents appear briefly when hovering over the cell.
    def on_cell_entered(self, row: int, column: int):
        try:
            myf.on_cell_entered_f(self.form_interviews, row, column)
        except Exception as e:
            raise Exception(f"Error occurred in on_cell_entered method: {e}")

    # This code is for cell clicking
    # If you want to show a persistent tooltip with the cell text. You need to use this code and its function.
    def on_cell_clicked(self, row: int, column: int):
        try:
            myf.on_cell_clicked_f(self.form_interviews, row, column)
        except Exception as e:
            raise Exception(f"Error occurred in on_cell_clicked method: {e}")

    # This code is for header clicking. This method sorts the data based on the column that was clicked
    def on_header_clicked(self, logical_index: int):
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
    def on_header_double_clicked(self, logical_index: int):
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
            self.form_interviews.comboBoxFilterOptions.currentIndexChanged.connect(self.filter_table_interviews)

        except Exception as e:
            raise Exception(f"Error occurred in on_header_double_clicked method: {e}")

# ........................................... Presentation Codes END ..................................................#


if __name__ == "__main__":
    app = QApplication([])
    main_window = InterviewsPage(['a', '$2b$12$U67LNgs5U7xNND9PYczCZeVtQl/Hhn6vxACCOxNpmSRjyD2AvKsS2', 'admin', 'Fatih', 'BUYUKAKCALI'])
    main_window.show()
    app.exec()
