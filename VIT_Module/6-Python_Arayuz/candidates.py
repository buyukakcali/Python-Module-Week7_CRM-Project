from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget, QApplication, QMenu, QMessageBox, QDialog, QVBoxLayout,
                             QTableWidget, QPushButton, QHBoxLayout, QComboBox)

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

        # For comparison when writing Attendee information to the sheet file during mentor appointment
        self.event_ids = None

        self.form_candidates = Ui_FormCandidates()
        self.form_candidates.setupUi(self)
        self.menu_user = None
        self.menu_admin = None

        # Persistent form settings activated at startup:
        self.form_candidates.labelInfo1.close()
        self.form_candidates.tableWidget.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft)
        myf.add_tooltip_to_any_form_object(self.form_candidates.comboBoxTrainees, 'Trainees')
        myf.add_tooltip_to_any_form_object(self.form_candidates.comboBoxProjectSubmitStatus, 'Project Submit Status')
        self.form_candidates.tableWidget.setStyleSheet("""
                QTableWidget { background-color: rgba(0, 0, 0,0%);}
                QToolTip { background-color: yellow; color: black; border: 1px solid black; }
                """)

        # Initial load view settings:
        self.filtering_column = 2
        self.headers = ['Zaman damgası', 'Basvuru Donemi', 'Mentor Ad', 'Mentor Soyad', 'Mentor Mail', 'Basvuran Ad',
                        'Basvuran Soyad', 'Basvuran Mail', 'Basvuran IT sektör bilgisi', 'Basvuran yoğunluk',
                        'Düşünceler', 'Yorumlar'
                        ]
        myf.write2table(self.form_candidates, self.headers, [])  # This code updates the tableWidget headers
        self.normalise_combobox_trainees()
        self.normalise_combobox_project_submit_status()


        # Connect signals to slots
        self.form_candidates.lineEditSearch.textEdited.connect(self.search_candidates)
        self.form_candidates.lineEditSearch.returnPressed.connect(self.search_candidates)
        self.form_candidates.pushButtonGetCandidates.clicked.connect(self.get_candidates)
        self.form_candidates.comboBoxProjectSubmitStatus.currentIndexChanged.connect(self.get_submitted_projects_list)
        self.form_candidates.pushButtonInterviewedCandidates.clicked.connect(self.get_interviewed_candidates)
        self.form_candidates.comboBoxTrainees.currentIndexChanged.connect(self.get_trainees)
        self.form_candidates.comboBoxFilterOptions.currentIndexChanged.connect(self.filter_table_candidates)
        self.form_candidates.pushButtonBackMenu.clicked.connect(self.back_menu)
        self.form_candidates.pushButtonExit.clicked.connect(self.app_exit)

        # EXTRA SLOTS:
        # ------------


        # Connect the cellClicked signal to the on_cell_clicked method
        self.form_candidates.tableWidget.cellClicked.connect(self.on_cell_clicked)

        # Connect the header's sectionClicked signal to the on_header_clicked method
        self.form_candidates.tableWidget.horizontalHeader().sectionClicked.connect(self.on_header_clicked)

        # Connect the header's sectionDoubleClicked signal to the on_header_double_clicked method
        self.form_candidates.tableWidget.horizontalHeader().sectionDoubleClicked.connect(self.on_header_double_clicked)

        # This code enables mouse tracking on tableWidget. It is needed for all mouse activity options above!
        self.form_candidates.tableWidget.setMouseTracking(True)

        # The display settings of the last clicked objects are determined.
        self.widgets = self.findChildren(QPushButton)  # Find all buttons of type QPushButton & assign them to the list
        self.widgets.extend(self.findChildren(QComboBox))   # Extend the list with QCombobox objects
        myf.handle_widget_styles(self, self.widgets)  # Manage button styles with central function

    # Lists candidates
    def get_candidates(self):
        try:
            myf.disable_context_menu(self.form_candidates, self.show_context_menu_add_remove_trainees)  # first disable
            myf.enable_context_menu(self.form_candidates, self.show_context_menu_assign_mentor)  # then enable
            self.normalise_combobox_trainees()
            self.normalise_combobox_project_submit_status()

            cnf = Config()
            self.headers = ['Zaman damgası', 'Basvuru Donemi', 'Aday Ad', 'Aday Soyad', 'Aday Mail',
                            'Mentor Ad', 'Mentor Soyad', 'Mentor Mail', 'ID', "Situation"]

            q1 = ("SELECT "
                  "fe." + cnf.evaluationTableFieldNames[1] + ", fe." + cnf.evaluationTableFieldNames[2] +
                   ", fa." + cnf.applicantTableFieldNames[2] + ", fa." + cnf.applicantTableFieldNames[3] +
                   ", fa." + cnf.applicantTableFieldNames[4] + ", ac." + cnf.appointmentsTableFieldNames[4] +
                   ", ac." + cnf.appointmentsTableFieldNames[5] + ", ac." + cnf.appointmentsTableFieldNames[6] +
                   ", fe." + cnf.evaluationTableFieldNames[0] + ", fe." + cnf.evaluationTableFieldNames[12] + " " +
                   "FROM " + cnf.evaluationTable + " fe " +
                   "LEFT JOIN " + cnf.appointmentsTable + " ac " +
                   "ON fe." + cnf.evaluationTableFieldNames[5] + " = ac." + cnf.appointmentsTableFieldNames[6] + " " +
                   "INNER JOIN " + cnf.applicantTable + " fa " +
                   "ON fe." + cnf.evaluationTableFieldNames[6] + " = fa." + cnf.applicantTableFieldNames[0] + " " +
                   "WHERE fe." + cnf.evaluationTableFieldNames[2] + " = %s " +
                   "AND fe." + cnf.evaluationTableFieldNames[12] + " > %s " +
                   "GROUP BY " +
                   "fe." + cnf.evaluationTableFieldNames[0] + ", fe." + cnf.evaluationTableFieldNames[1] +
                   ", fe." + cnf.evaluationTableFieldNames[2] + ", fa." + cnf.applicantTableFieldNames[2] +
                   ", fa." + cnf.applicantTableFieldNames[3] + ", fa." + cnf.applicantTableFieldNames[4] +
                   ", ac." + cnf.appointmentsTableFieldNames[4] + ", ac." + cnf.appointmentsTableFieldNames[5] +
                   ", ac." + cnf.appointmentsTableFieldNames[6] + ", fe." + cnf.evaluationTableFieldNames[0] +
                   ", fe." + cnf.evaluationTableFieldNames[12])
            # q1 = ("SELECT "
            #       "fe.crm_Timestamp, fe.crm_Period, fa.crm_Name, fa.crm_Surname, fa.crm_Email, "
            #       "ac.crm_MentorName, ac.crm_MentorSurname, ac.crm_MentorMail, fe.crm_ID, fe.crm_IsApplicantACandidate "
            #       "FROM "
            #       "form2_evaluations fe "
            #       "LEFT JOIN appointments_current ac ON fe.crm_MentorMail = ac.crm_MentorMail "
            #       "INNER JOIN form1_applicant fa ON fe.crm_ApplicantID = fa.crm_ID "
            #       "WHERE fe.crm_Period = %s AND fe.crm_IsApplicantACandidate > %s "
            #       "GROUP BY "
            #       "fe.crm_ID, fe.crm_Timestamp, fe.crm_Period, fa.crm_Name, fa.crm_Surname, fa.crm_Email, "
            #       "ac.crm_MentorName, ac.crm_MentorSurname, ac.crm_MentorMail, fe.crm_ID, fe.crm_IsApplicantACandidate")


            candidates = myf.execute_read_query(cnf.open_conn(), q1, (myf.last_period(), 0))

            # Rebuilds the list based on the data type of the cells.
            self.active_list = myf.remake_it_with_types(candidates)

            self.filtering_list = list(self.active_list)  # Assigned for filtering.
            myf.write2table(self.form_candidates, self.headers, self.active_list)

            # Fill the combobox for default filtering while loading
            self.filtering_column = 2
            self.form_candidates.comboBoxFilterOptions.setPlaceholderText("Filter Area")
            self.form_candidates.comboBoxFilterOptions.clear()
            items = myf.filter_active_options(self.filtering_list, self.filtering_column)
            self.form_candidates.comboBoxFilterOptions.addItems(items)

            # tableWidget line coloring process
            # The function called shows the records with colored background for displaying INTERVIEW DETERMINED
            myf.highlight_candidates(
                self.form_candidates, 9, 2, 'white', 'orange')
        except Exception as e:
            raise Exception(f"Error occurred in get_candidates method: {e}")

    # Adding context menu to right-click
    def show_context_menu_assign_mentor(self, pos):
        try:
            # Control to handle right click only
            if not self.form_candidates.tableWidget.viewport().underMouse():
                return

            item = self.form_candidates.tableWidget.itemAt(pos)
            if item is None or self.form_candidates.tableWidget.rowCount() == 0:
                return  # If there are no valid items or the table is empty, do nothing

            self.form_candidates.tableWidget.selectRow(item.row())

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
            action = context_menu.exec(self.form_candidates.tableWidget.viewport().mapToGlobal(pos))

            if action == show_assign_mentor_action:
                self.get_open_appointments()

        except Exception as e:
            raise Exception(f"Error occurred in show_context_menu_assign_mentor method: {e}")

    # Lists available appointments
    def get_open_appointments(self):
        try:
            current_row = self.form_candidates.tableWidget.currentRow()
            if int(self.form_candidates.tableWidget.item(current_row, 9).text()) == 2:
                header = "Warning:"
                message_text = "The candidate is already assigned for a project homework meeting!"
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
                      "WHERE " + cnf.appointmentsTableFieldNames[7] + " LIKE '2%' " +
                      "AND " + cnf.appointmentsTableFieldNames[12] + " is null " +
                      "ORDER BY " + cnf.appointmentsTableFieldNames[3] + " ASC")
                # q1 = ("SELECT crm_InterviewDatetime, crm_MentorName, crm_MentorSurname, crm_MentorMail, "
                #           "crm_Summary, crm_Description, crm_Location, crm_OnlineMeetingLink, crm_EventID "
                #           "FROM appointments_current "
                #           "WHERE crm_Summary LIKE '2%' AND crm_AttendeeID is null "
                #           "ORDER BY crm_InterviewDatetime ASC")

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

                # Appointment selection and mentor assigning process
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
            cnf = Config()
            reply = QMessageBox.question(self, 'Mentor Assignment',
                                         'Do you want to assign a mentor to this appointment?',
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                # Get the ID of the selected row
                current_row = self.form_candidates.tableWidget.currentRow()
                ID = int(self.form_candidates.tableWidget.item(current_row, 8).text())

                # Update the database
                q1 = ("UPDATE " + cnf.appointmentsTable + " SET " + cnf.appointmentsTableFieldNames[12] + " = %s " +
                      "WHERE " + cnf.appointmentsTableFieldNames[2] + " = %s")
                # q1 = "UPDATE appointments_current SET crm_AttendeeID = %s WHERE crm_EventID = %s"
                myf.execute_write_query(cnf.open_conn(), q1, (ID, event_id))

                q2 = ("UPDATE " + cnf.evaluationTable + " SET " + cnf.evaluationTableFieldNames[12] + " = 2 " +
                      "WHERE " + cnf.evaluationTableFieldNames[2] + " = %s AND " + cnf.evaluationTableFieldNames[0] + " = %s")
                # q2 = "UPDATE form2_evaluations SET crm_IsApplicantACandidate = 2 WHERE crm_Period = %s AND crm_ID = %s"
                myf.execute_write_query(cnf.open_conn(), q2, (myf.last_period(), ID))

                # We'll extract the applicant's name, surname and email from the database and send it to Google Sheet.
                get_candidates_query = (
                        "SELECT " + cnf.applicantTableFieldNames[2] + ", " + cnf.applicantTableFieldNames[3] +
                        ", " + cnf.applicantTableFieldNames[4] + " " +
                        "FROM " + cnf.applicantTable + " " +
                        "WHERE " + cnf.applicantTableFieldNames[0] + " = %s")
                # get_candidates_query = "SELECT crm_Name, crm_Surname, crm_Email FROM form1_applicant WHERE crm_ID = %s"

                candidates_data = myf.execute_read_query(cnf.open_conn(), get_candidates_query, (ID,))
                attendee_name, attendee_surname, attendee_email = candidates_data[0]

                myf.update_events_all_interviews_sheet(event_id, attendee_name, attendee_surname, attendee_email)

                QMessageBox.information(self, 'Successful', 'Mentor successfully assigned.')

                # close Dialog
                self.sender().parent().close()

                # Update tableWidget
                self.get_candidates()
        except Exception as e:
            raise Exception(f"Error occurred in assign_mentor method: {e}")

    def get_submitted_projects_list(self):
        myf.disable_context_menu(self.form_candidates, self.show_context_menu_assign_mentor)  # first disable
        myf.disable_context_menu(self.form_candidates, self.show_context_menu_add_remove_trainees)  # first disable
        # myf.normalise_combo_boxes([None, self.form_candidates.comboBoxFilterOptions])
        self.normalise_combobox_trainees()

        cnf = Config()
        try:
            self.headers = ['Basvuru Donemi', 'Aday Ad', 'Aday Soyad', 'Aday Mail', 'Proje Teslim Tarihi', 'ID', "Situation"]

            q1 = ("SELECT "
                  "fe." + cnf.evaluationTableFieldNames[2] + ", fa." + cnf.applicantTableFieldNames[2] +
                  ", fa." + cnf.applicantTableFieldNames[3] + ", fa." + cnf.applicantTableFieldNames[4] +
                  ", fe." + cnf.evaluationTableFieldNames[11] + ", fe." + cnf.evaluationTableFieldNames[0] +
                  ", fe." + cnf.evaluationTableFieldNames[12] + " " +
                  "FROM " + cnf.evaluationTable + " fe " +
                  "INNER JOIN " + cnf.applicantTable + " fa " +
                  "ON fe." + cnf.evaluationTableFieldNames[6] + " = fa." + cnf.applicantTableFieldNames[0] + " " +
                  "WHERE fe." + cnf.evaluationTableFieldNames[2] + " = %s " + # " = %s AND " +
                  # "fe." + cnf.evaluationTableFieldNames[11] + " != '0000-00-00 00:00:00' " +
                  "GROUP BY " +
                  "fe." + cnf.evaluationTableFieldNames[2] + ", fa." + cnf.applicantTableFieldNames[2] +
                   ", fa." + cnf.applicantTableFieldNames[3] + ", fa." + cnf.applicantTableFieldNames[4] +
                  ", fe." + cnf.evaluationTableFieldNames[11] + ", fe." + cnf.evaluationTableFieldNames[0] +
                  ", fe." + cnf.evaluationTableFieldNames[12])
            # q1 = ("SELECT "
            #       "fe.crm_Period, fa.crm_Name, fa.crm_Surname, fa.crm_Email, fe.crm_ProjectReturnDatetime "
            #       "fe.crm_ID, fe.crm_IsApplicantACandidate "
            #       "FROM "
            #       "form2_evaluations fe "
            #       "INNER JOIN form1_applicant fa ON fe.crm_ApplicantID = fa.crm_ID "
            #       "WHERE fe.crm_Period = %s "
            #       "GROUP BY "
            #       "fe.crm_Period, fa.crm_Name, fa.crm_Surname, fa.crm_Email, fe.crm_ProjectReturnDatetime != '0000-00-00 00:00:00'"
            #       "fe.crm_ID, fe.crm_IsApplicantACandidate")

            submitted_projects  = myf.execute_read_query(cnf.open_conn(), q1, (myf.last_period(),))

            # Rebuilds the list based on the data type of the cells.
            self.active_list = myf.remake_it_with_types(submitted_projects)
            submitted = []
            unsubmitted = []

            # Creating new lists based on submitting status
            for row in self.active_list:
                if row[4] is None:
                    unsubmitted.append(row)
                else:
                    submitted.append(row)

            if self.form_candidates.comboBoxProjectSubmitStatus.currentText().strip() == 'Submitted':
                self.filtering_list = list(submitted)  # Assigned for filtering.
                myf.write2table(self.form_candidates, self.headers, submitted)
            else:
                self.filtering_list = list(unsubmitted)  # Assigned for filtering.
                myf.write2table(self.form_candidates, self.headers, unsubmitted)

            # Fill the combobox for default filtering while loading
            self.filtering_column = 2
            self.form_candidates.comboBoxFilterOptions.setPlaceholderText("Filter Area")
            self.form_candidates.comboBoxFilterOptions.clear()
            items = myf.filter_active_options(self.filtering_list, self.filtering_column)
            self.form_candidates.comboBoxFilterOptions.addItems(items)

        except Exception as e:
            raise Exception(f"Error occurred in get_submitted_projects_list method: {e}")

    # Lists candidates who have had their second(with project homework) interview and shows their evaluation.
    def get_interviewed_candidates(self):
        try:
            myf.disable_context_menu(self.form_candidates, self.show_context_menu_assign_mentor)  # first disable
            myf.enable_context_menu(self.form_candidates, self.show_context_menu_add_remove_trainees)  # then enable
            # myf.normalise_combo_boxes([None, self.form_candidates.comboBoxFilterOptions])
            self.normalise_combobox_trainees()
            self.normalise_combobox_project_submit_status()

            cnf = Config()

            self.headers = ['Zaman damgası', 'Basvuru Donemi', 'Aday Ad', 'Aday Soyad', 'Aday Mail', 'Mentor Ad',
                            'Mentor Soyad', 'Mentor Mail', 'Kod Bilgisi', '1. Yardimci Degerlendirmesi',
                            '2. Yardimci Degerlendirmesi', '3. Yardimci Degerlendirmesi', 'Mentor Degerlendirmesi',
                            'ID', "Situation"
                            ]


            q1 = ("SELECT "
                  "ff." + cnf.finalEvaluationTableFieldNames[1] + ", ff." + cnf.finalEvaluationTableFieldNames[2] +
                  ", fa." + cnf.applicantTableFieldNames[2] + ", fa." + cnf.applicantTableFieldNames[3] +
                  ", fa." + cnf.applicantTableFieldNames[4] + ", ac." + cnf.appointmentsTableFieldNames[4] +
                  ", ac." + cnf.appointmentsTableFieldNames[5] + ", ac." + cnf.appointmentsTableFieldNames[6] +
                  ", ff." + cnf.finalEvaluationTableFieldNames[7] + ", ff." + cnf.finalEvaluationTableFieldNames[8] +
                  ", ff." + cnf.finalEvaluationTableFieldNames[9] + ", ff." + cnf.finalEvaluationTableFieldNames[10] +
                  ", ff." + cnf.finalEvaluationTableFieldNames[11] + ", ff." + cnf.finalEvaluationTableFieldNames[0] +
                  ", ff." + cnf.finalEvaluationTableFieldNames[12] + " " +
                  "FROM " + cnf.finalEvaluationTable + " ff " +
                  "LEFT JOIN " + cnf.appointmentsTable + " ac " +
                  "ON ff." + cnf.finalEvaluationTableFieldNames[5] + " = ac." + cnf.appointmentsTableFieldNames[6] +
                  " INNER JOIN " + cnf.applicantTable + " fa " +
                  "ON ff." + cnf.finalEvaluationTableFieldNames[6] + " = fa." + cnf.applicantTableFieldNames[0] + " " +
                  "WHERE ff." + cnf.finalEvaluationTableFieldNames[2] + " = %s " +
                  "GROUP BY " +
                  "ff." + cnf.finalEvaluationTableFieldNames[1] + ", ff." + cnf.finalEvaluationTableFieldNames[2] +
                  ", fa." + cnf.applicantTableFieldNames[2] + ", fa." + cnf.applicantTableFieldNames[3] +
                  ", fa." + cnf.applicantTableFieldNames[4] + ", ac." + cnf.appointmentsTableFieldNames[4] +
                  ", ac." + cnf.appointmentsTableFieldNames[5] + ", ac." + cnf.appointmentsTableFieldNames[6] +
                  ", ff." + cnf.finalEvaluationTableFieldNames[7] + ", ff." + cnf.finalEvaluationTableFieldNames[8] +
                  ", ff." + cnf.finalEvaluationTableFieldNames[9] + ", ff." + cnf.finalEvaluationTableFieldNames[10] +
                  ", ff." + cnf.finalEvaluationTableFieldNames[11] + ", ff." + cnf.finalEvaluationTableFieldNames[0] +
                  ", ff." + cnf.finalEvaluationTableFieldNames[12])
            # q1 = ("SELECT "
            #       "ff.crm_Timestamp, ff.crm_Period, fa.crm_Name, fa.crm_Surname, fa.crm_Email, "
            #       "ac.crm_MentorName, ac.crm_MentorSurname, ac.crm_MentorMail, ff.crm_CodingSkills, "
            #       "ff.crm_AssistantEvaluation1, ff.crm_AssistantEvaluation2, ff.crm_AssistantEvaluation3, "
            #       "ff.crm_MentorEvaluation, ff.crm_ID, ff.crm_IsCandidateATrainee "
            #       "FROM "
            #       "form3_final_evaluations ff "
            #       "LEFT JOIN appointments_current ac ON ff.crm_MentorMail = ac.crm_MentorMail "
            #       "INNER JOIN form1_applicant fa ON ff.crm_CandidateID = fa.crm_ID "
            #       "WHERE ff.crm_Period = %s "
            #       "GROUP BY "
            #       "ff.crm_Timestamp, ff.crm_Period, fa.crm_Name, fa.crm_Surname, fa.crm_Email, "
            #       "ac.crm_MentorName, ac.crm_MentorSurname, ac.crm_MentorMail, ff.crm_CodingSkills, "
            #       "ff.crm_AssistantEvaluation1, ff.crm_AssistantEvaluation2, ff.crm_AssistantEvaluation3, "
            #       "ff.crm_MentorEvaluation, ff.crm_ID, ff.crm_IsCandidateATrainee")

            candidates = myf.execute_read_query(cnf.open_conn(), q1, (myf.last_period(),))

            # Add data to table
            self.candidates = myf.remake_it_with_types(candidates)
            self.active_list = list(self.candidates)
            myf.write2table(self.form_candidates, self.headers, self.active_list)

            # Fill combobox for filtering
            self.filtering_column = 2
            self.form_candidates.comboBoxFilterOptions.setPlaceholderText("Filter Area")
            self.filtering_list = list(self.active_list)  # Assigned for filtering
            self.form_candidates.comboBoxFilterOptions.clear()
            items = myf.filter_active_options(self.filtering_list, self.filtering_column)
            self.form_candidates.comboBoxFilterOptions.addItems(items)

            # tableWidget line coloring process
            # The function called shows the records with colored background for displaying INTERVIEW DETERMINED
            myf.highlight_candidates(self.form_candidates, 14, 1, 'white', 'green')
        except Exception as e:
            raise Exception(f"Error occurred in get_interviewed_candidates method: {e}")

    # Adding context menu to right-click
    def show_context_menu_add_remove_trainees(self, pos):
        try:
            # Control to handle right click only
            if not self.form_candidates.tableWidget.viewport().underMouse():
                return

            item = self.form_candidates.tableWidget.itemAt(pos)
            if item is None or self.form_candidates.tableWidget.rowCount() == 0:
                return  # If there are no valid items or the table is empty, do nothing

            self.form_candidates.tableWidget.selectRow(item.row())

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
            add_trainee_action = context_menu.addAction("Add to Trainees")
            remove_trainee_action = context_menu.addAction("Remove from Trainees")
            action = context_menu.exec(self.form_candidates.tableWidget.viewport().mapToGlobal(pos))

            # The column containing the candidate's e-mail address (for example, column 4)
            value = self.form_candidates.tableWidget.item(item.row(), 4)
            candidate_mail = value.text()   # if value else None

            if value is not None:
                # Take action based on which action is selected
                if action == add_trainee_action:
                    self.add_remove_trainees(candidate_mail, 'add_trainee')
                elif action == remove_trainee_action:
                    self.add_remove_trainees(candidate_mail, 'remove_trainee')

        except Exception as e:
            raise Exception(f"Error occurred in show_context_menu_add_remove_trainees method: {e}")

    # Registers the candidate as a trainee or removes from trainee list
    def add_remove_trainees(self, candidate_mail: str, act):
        try:
            # myf.disable_context_menu(self.form_candidates, self.show_context_menu_assign_mentor)

            # Find the actual ID value of the selected row in the list
            crm_id = None
            isCandidateATrainee = None

            for element in self.active_list:
                if element[4] == candidate_mail:
                    crm_id = element[13]
                    isCandidateATrainee = element[14]

            # Warning messages for meaningless actions
            if act == 'add_trainee' and isCandidateATrainee > 0:
                header = "Warning:"
                message_text = "The record has already assigned as a Trainee!"
                myf.set_info_dialog(self, header, message_text)
                return
            elif act == 'remove_trainee' and isCandidateATrainee == 0:
                header = "Warning:"
                message_text = "The record is not a Trainee anyway!"
                myf.set_info_dialog(self, header, message_text)
                return

            # adding or removing actions
            cnf = Config()
            if act == 'add_trainee':
                reply = QMessageBox.question(self, 'Assigning / Registering Trainees:',
                                             'Do you want to assign this candidate as a trainee?',
                                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                             QMessageBox.StandardButton.No)

                if reply == QMessageBox.StandardButton.Yes and crm_id:
                    # Registers as a trainee
                    if isCandidateATrainee != 1:
                        q1 = ("UPDATE " + cnf.finalEvaluationTable + " " +
                              "SET " + cnf.finalEvaluationTableFieldNames[12] + " = 1 " +
                              "WHERE " + cnf.finalEvaluationTableFieldNames[2] + " = %s " +
                              "AND " + cnf.evaluationTableFieldNames[0] + " = %s")
                        # q1 = ("UPDATE form3_final_evaluations "
                        #       "SET crm_IsCandidateATrainee = 1 "
                        #       "WHERE crm_Period = %s AND crm_ID = %s")

                        last_period = myf.last_period()
                        myf.execute_write_query(cnf.open_conn(), q1, (last_period, crm_id))

                        QMessageBox.information(self, 'Info:', 'The selected record was assigned as Trainee.')
            else:
                reply = QMessageBox.question(self, 'Removing from the Trainee List:',
                                             'Do you want to remove this record from the trainee list?',
                                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                             QMessageBox.StandardButton.No)

                if reply == QMessageBox.StandardButton.Yes and crm_id:
                    # Removes the record from the trainee list
                    if isCandidateATrainee != 0:
                        q1 = ("UPDATE " + cnf.finalEvaluationTable + " " +
                              "SET " + cnf.finalEvaluationTableFieldNames[12] + " = 0 " +
                              "WHERE " + cnf.finalEvaluationTableFieldNames[2] + " = %s " +
                              "AND " + cnf.evaluationTableFieldNames[0] + " = %s")
                        # q1 = ("UPDATE form3_final_evaluations "
                        #       "SET crm_IsCandidateATrainee = 0 "
                        #       "WHERE crm_Period = %s AND crm_ID = %s")

                        last_period = myf.last_period()
                        myf.execute_write_query(cnf.open_conn(), q1, (last_period, crm_id))

                        QMessageBox.information(self, 'Info:', 'The selected record is removed from the trainee list!')
            # Update tableWidget
            self.get_interviewed_candidates()

        except Exception as e:
            raise Exception(f"Error occurred in add_remove_trainees method: {e}")

    # Lists trainees
    def get_trainees(self):
        try:
            myf.disable_context_menu(self.form_candidates, self.show_context_menu_assign_mentor)  # first disable
            myf.disable_context_menu(self.form_candidates, self.show_context_menu_add_remove_trainees)  # then enable
            # myf.normalise_combo_boxes([None, self.form_candidates.comboBoxFilterOptions])
            self.normalise_combobox_project_submit_status()

            cnf = Config()
            self.headers = ['Zaman damgası', 'Basvuru Donemi', 'Kursiyer Ad', 'Kursiyer Soyad', 'Kursiyer Mail',
                            'Mentor Ad', 'Mentor Soyad', 'Mentor Mail', 'Kodlama Becerisi',
                            '1. Yardimci Degerlendirmesi'	'2. Yardimci Degerlendirmesi',
                            '3. Yardimci Degerlendirmesi', 'Mentor Degerlendirmesi']

            # Fetches trainees from last period
            q1 = ("SELECT "
                  "b." + cnf.finalEvaluationTableFieldNames[1] + ", b." + cnf.finalEvaluationTableFieldNames[2] +
                  ", a." + cnf.applicantTableFieldNames[2] + ", a." + cnf.applicantTableFieldNames[3] +
                  ", a." + cnf.applicantTableFieldNames[4] + ", b." + cnf.finalEvaluationTableFieldNames[3] +
                  ", b." + cnf.finalEvaluationTableFieldNames[4] + ", b." + cnf.finalEvaluationTableFieldNames[5] +
                  ", b." + cnf.finalEvaluationTableFieldNames[7] + ", b." + cnf.finalEvaluationTableFieldNames[8] +
                  ", b." + cnf.finalEvaluationTableFieldNames[9] + ", b." + cnf.finalEvaluationTableFieldNames[10] +
                  ", b." + cnf.finalEvaluationTableFieldNames[11] +  " " +
                  "FROM " + cnf.finalEvaluationTable + " b " +
                  "INNER JOIN " + cnf.applicantTable + " a " +
                  "ON b." + cnf.finalEvaluationTableFieldNames[6] + " = a." + cnf.applicantTableFieldNames[0] + " " +
                  "WHERE b." + cnf.finalEvaluationTableFieldNames[12] + " = 1 " +
                  "ORDER BY b." + cnf.finalEvaluationTableFieldNames[1] + " ASC")
            # q1 = ("SELECT b.crm_Timestamp, b.crm_Period, a.crm_Name, a.crm_Surname, a.crm_Email, b.crm_MentorName, "
            #       "b.crm_MentorSurname, b.crm_MentorMail, b.crm_CodingSkills, b.crm_AssistantEvaluation1, "
            #       "b.crm_AssistantEvaluation2, b.crm_AssistantEvaluation3, b.crm_MentorEvaluation "
            #       "FROM form3_final_evaluations b "
            #       "WHERE crm_IsCandidateATrainee == 1 "
            #       "INNER JOIN form1_applicant a ON b.crm_CandidateID = a.crm_ID "
            #       "WHERE b.crm_IsCandidateATrainee = 1 "
            #       "ORDER BY b.crm_Timestamp ASC")

            # Fetches trainees from past periods
            q2 = ("SELECT "
                  "b." + cnf.finalEvaluationOldTableFieldNames[3] + ", b." + cnf.finalEvaluationOldTableFieldNames[4] +
                  ", a." + cnf.applicantTableFieldNames[2] + ", a." + cnf.applicantTableFieldNames[3] +
                  ", a." + cnf.applicantTableFieldNames[4] + ", b." + cnf.finalEvaluationOldTableFieldNames[5] +
                  ", b." + cnf.finalEvaluationOldTableFieldNames[6] +
                  ", b." + cnf.finalEvaluationOldTableFieldNames[7] +
                  ", b." + cnf.finalEvaluationOldTableFieldNames[9] +
                  ", b." + cnf.finalEvaluationOldTableFieldNames[10] +
                  ", b." + cnf.finalEvaluationOldTableFieldNames[11] +
                  ", b." + cnf.finalEvaluationOldTableFieldNames[12] +
                  ", b." + cnf.finalEvaluationOldTableFieldNames[13] + " " +
                  "FROM " + cnf.finalEvaluationOldTable + " b " +
                  "INNER JOIN " + cnf.applicantTable + " a ON b." + cnf.finalEvaluationOldTableFieldNames[8] +
                  " = a." + cnf.applicantTableFieldNames[0] + " " +
                  "WHERE b." + cnf.finalEvaluationOldTableFieldNames[14] + " = 1 " +
                  "ORDER BY b." + cnf.finalEvaluationOldTableFieldNames[2] + " DESC")
            # DESC was made for sequential view according to the period

            # q2 = ("SELECT b.crm_Timestamp, b.crm_Period, a.crm_Name, a.crm_Surname, a.crm_Email, b.crm_MentorName, "
            #       "b.crm_MentorSurname, b.crm_MentorMail, b.crm_CodingSkills, b.crm_AssistantEvaluation1, "
            #       "b.crm_AssistantEvaluation2, b.crm_AssistantEvaluation3, b.crm_MentorEvaluation "
            #       "FROM form3_final_evaluations_old b "
            #       "INNER JOIN form1_applicant a ON b.crm_CandidateID = a.crm_ID "
            #       "WHERE b.crm_IsCandidateATrainee = 1 "
            #       "ORDER BY b.crm_ID_in_form3_evaluations DESC")

            trainees = myf.execute_read_query(cnf.open_conn(), q1)

            # Bring mentor-assigned applicants and their mentors in all application periods.
            if self.form_candidates.comboBoxTrainees.currentText() == 'All Periods':
                old_trainees = myf.execute_read_query(cnf.open_conn(), q2)
                # Old_trainees DESC was made for sequential view according to the period, but it was not tested.
                # *** normal order in interview module - after control, delete here
                trainees = trainees + old_trainees

            self.active_list = list(trainees)

            # Applicants who have been assigned a mentor
            myf.write2table(self.form_candidates, self.headers, self.active_list)

            # Fill the combobox for filtering while loading
            self.filtering_list = list(self.active_list)
            self.filtering_column = 2
            self.form_candidates.comboBoxFilterOptions.clear()
            items = myf.filter_active_options(self.filtering_list, self.filtering_column)
            self.form_candidates.comboBoxFilterOptions.addItems(items)
        except Exception as e:
            raise Exception(f"Error occurred in get_trainees method: {e}")

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


    # Search settings for CandidatesPage
    def search_candidates(self):
        try:
            myf.normalise_combo_boxes([None, self.form_candidates.comboBoxFilterOptions])

            # If there is active_list, update filtering_list
            if self.active_list:
                self.filtering_list = list(self.active_list)  # Assign the list for filtering.

            searched_text = self.form_candidates.lineEditSearch.text()    # Get text in search field

            # Get results
            self.filtering_list = myf.search(self.filtering_list, self.headers, self.filtering_column, searched_text)

            myf.write2table(self.form_candidates, self.headers, self.filtering_list) # Write the results to the tableWidget

            # Fill the combobox for filtering after every single search
            if self.active_list:
                self.filtering_list = list(self.active_list)
                items = myf.filter_active_options(self.filtering_list, self.filtering_column)
                self.form_candidates.comboBoxFilterOptions.addItems(items)
        except Exception as e:
            raise Exception(f"Error occurred in search_candidates method: {e}")

    # Filter settings for InterviewsPage
    def filter_table_candidates(self):
        try:
            self.form_candidates.lineEditSearch.clear()  # clear the search box
            myf.filter_table(self.form_candidates, self.headers, self.filtering_list, self.filtering_column)
        except Exception as e:
            raise Exception(f"Error occurred in filter_table_candidates method: {e}")


    # .................................................................................................................#
    # .......................................... PRESENTATION CODES START .............................................#
    # .................................................................................................................#

    # Method to automatically adjust the display settings of the comboBoxTrainees object
    def normalise_combobox_trainees(self):
        try:
            myf.normalise_combo_boxes(
                [self.form_candidates.comboBoxTrainees, self.form_candidates.comboBoxFilterOptions],
                ['             Trainess', '          Last Period', '          All Periods'])
        except Exception as e:
            raise Exception(f"Error occurred in normalise_combo_box_trainees method: {e}")

    # Method to automatically adjust the display settings of the comboBoxTrainees object
    def normalise_combobox_project_submit_status(self):
        try:
            myf.normalise_combo_boxes(
                [self.form_candidates.comboBoxProjectSubmitStatus, self.form_candidates.comboBoxFilterOptions],
                ['  Project Submit Status', '          Submitted', '          Unsubmitted'])
        except Exception as e:
            raise Exception(f"Error occurred in normalise_combobox_project_submit_status method: {e}")

    # This code is written to make the contents appear briefly when hovering over the cell.
    def on_cell_entered(self, row: int, column: int):
        try:
            myf.on_cell_entered_f(self.form_candidates, row, column)
        except Exception as e:
            raise Exception(f"Error occurred in on_cell_entered method: {e}")

    # This code is for cell clicking
    # If you want to show a persistent tooltip with the cell text. You need to use this code and its function.
    def on_cell_clicked(self, row: int, column: int):
        try:
            myf.on_cell_clicked_f(self.form_candidates, row, column)
        except Exception as e:
            raise Exception(f"Error occurred in on_cell_clicked method: {e}")

    # This code is for header clicking. This method sorts the data based on the column that was clicked
    def on_header_clicked(self, logical_index: int):
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

            self.form_candidates.comboBoxFilterOptions.clear()
            self.filtering_column = logical_index
            self.form_candidates.comboBoxFilterOptions.setPlaceholderText("Filter Area")
            items = myf.filter_active_options(self.filtering_list, logical_index)
            # print('Filtered items: ', items)
            self.form_candidates.comboBoxFilterOptions.addItems(items)
            myf.write2table(self.form_candidates, self.headers, self.active_list)
            self.form_candidates.comboBoxFilterOptions.currentIndexChanged.connect(self.filter_table_candidates)

        except Exception as e:
            raise Exception(f"Error occurred in on_header_double_clicked method: {e}")

    # ......................................... Presentation Codes END ................................................#


if __name__ == "__main__":
    app = QApplication([])
    main_window = CandidatesPage(['a', '$2b$12$U67LNgs5U7xNND9PYczCZeVtQl/Hhn6vxACCOxNpmSRjyD2AvKsS2', 'admin', 'Fatih', 'BUYUKAKCALI'])
    main_window.show()
    app.exec()
