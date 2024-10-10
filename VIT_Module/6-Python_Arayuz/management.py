from PyQt6.QtCore import QDateTime, QTime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QDialog, QLineEdit, QMenu, QInputDialog)

from UI_Files.management_ui import Ui_FormManagement
from UI_Files.add_new_user_ui import Ui_DialogAddNewUser
from UI_Files.reset_users_pass_ui import Ui_DialogResetUsersPasswords
from UI_Files.update_deadline_ui import Ui_DialogSetDeadline
from UI_Files.about_coder_ui import Ui_DialogAboutCoder

import my_functions as myf
from my_classes import Config


class ManagementPage(QMainWindow):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user
        self.form_management = Ui_FormManagement()
        self.form_management.setupUi(self)

        self.menu_user = None
        self.menu_admin = None
        self.users = None
        self.dialog_add_user = None
        self.dialog_reset_users_password = None
        self.dialog_update_deadline = None
        self.dialog_about_coder = None

        # Persistent form settings activated at startup:
        # Bind informative tooltips to buttons
        myf.add_tooltip_to_any_form_object(self.form_management.pushButtonAddNewUser, 'Add New User')
        myf.add_tooltip_to_any_form_object(self.form_management.pushButtonResetUserPassword, 'Reset Users Passwords')
        myf.add_tooltip_to_any_form_object(self.form_management.pushButtonUpdateDriveFolder, 'Update Homework Projects Folder')
        myf.add_tooltip_to_any_form_object(self.form_management.pushButtonUpdateDeadline, 'Update Homework Projects Deadline')

        self.add_user_window = None
        self.reset_users_pass_window = None
        self.update_deadline_window = None
        self.about_coder_window = None

        # Initial load view settings:
        self.menuBar().setStyleSheet("""            
            QMenuBar {
                /* Menu bar background color */
                /* Text color in the menu bar */
            }
            QMenuBar::item {
                /* Sides of menu name */
            }
            QMenuBar:item:hover {
                /* Sides of menu name */
            }
            QMenu {
                background-color: #ffffff; /* Menu background color */
                color: #000000; /* Text color in the menu */
                border: 1px solid #cfcfcf; /* menu borders */
                border-radius: 5px; /* Rounding the corners */
            }
            QMenu::item {
                background-color: #f5f5f5; /* Background color of non-selected items */
            }
            QMenu::item:selected {
                background-color: #0078d7; /* Background color of the selected item */
                color: #ffffff; /* Text color of the selected item */
            }
        """)

        # Connect signals to slots:
        self.form_management.pushButtonAddNewUser.clicked.connect(self.add_new_user)
        self.form_management.pushButtonResetUserPassword.clicked.connect(self.reset_users_password)
        self.form_management.pushButtonUpdateDriveFolder.clicked.connect(self.update_driver_folder_name)
        self.form_management.pushButtonUpdateDeadline.clicked.connect(self.update_project_hw_deadline)
        self.form_management.pushButtonBackMenu.clicked.connect(self.back_menu)

        # Bind actions to methods
        self.form_management.actionAdd_New_User.triggered.connect(self.add_new_user)
        self.form_management.actionReset_Users_Passwords.triggered.connect(self.reset_users_password)
        self.form_management.actionUpdate_Google_Drive_Folder.triggered.connect(self.update_driver_folder_name)
        self.form_management.actionUpdate_Project_Deadline.triggered.connect(self.update_project_hw_deadline)
        self.form_management.actionBack_Menu.triggered.connect(self.back_menu)
        self.form_management.actionLogs.triggered.connect(self.show_info)
        self.form_management.actionAbout_Coder.triggered.connect(self.about_coder)



    # Temporary method will be moved from here if the relevant feature is used!!!
    def show_info(self):
        myf.set_info_dialog(self, 'Bilgi:',
                            'Bu ozellik istenirse eklenebilir ancak db tarafinda loglama ile ilgili '
                            'calismak gerekiyor.\nCok zor olmaz ama ne tur seylerin loglanmasi ve buradan kontrol '
                            'edilmesi faydali olacak, once o tartisilmali...')



    # It was written so that a user with admin authority can create new accounts.
    def add_new_user(self):
        try:
            self.add_user_window = QDialog(self)  # We create a modal window
            self.add_user_window.setModal(True)  # make a modal

            self.dialog_add_user = Ui_DialogAddNewUser()  # Use the new interface file here
            self.dialog_add_user.setupUi(self.add_user_window)

            # show the window
            self.add_user_window.show()
            self.empty_add_new_user_dialog()

            self.dialog_add_user.lineEditUsername.textChanged.connect(self.dialog_add_new_user_turn_back_orj_style)
            self.dialog_add_user.lineEditPassword.textChanged.connect(self.dialog_add_new_user_turn_back_orj_style)
            self.dialog_add_user.comboBoxAuthority.currentIndexChanged.connect(self.dialog_add_new_user_turn_back_orj_style)
            self.dialog_add_user.lineEditName.textChanged.connect(self.dialog_add_new_user_turn_back_orj_style)
            self.dialog_add_user.lineEditSurname.textChanged.connect(self.dialog_add_new_user_turn_back_orj_style)

            # Connect confirmation and cancel buttons
            self.dialog_add_user.pushButtonNUAApprove.clicked.connect(self.submit_user_info)
            self.dialog_add_user.pushButtonNUACancel.clicked.connect(self.add_user_window.close)
        except Exception as e:
            raise Exception(f"Error occurred in add_new_user method: {e}")

    # Restores the original style based on the object's type.
    def dialog_add_new_user_turn_back_orj_style(self):
        try:
            cnf = Config()
            self.dialog_add_user.lineEditUsername.setStyleSheet(cnf.orj_style)
            self.dialog_add_user.lineEditPassword.setStyleSheet(cnf.orj_style)
            self.dialog_add_user.lineEditName.setStyleSheet(cnf.orj_style)
            self.dialog_add_user.lineEditSurname.setStyleSheet(cnf.orj_style)
            self.dialog_add_user.comboBoxAuthority.setStyleSheet(cnf.orj_style)
            self.dialog_add_user.pushButtonNUAApprove.setStyleSheet(cnf.orj_style)
            self.dialog_add_user.pushButtonNUACancel.setStyleSheet(cnf.orj_style)
        except Exception as e:
            raise Exception(f"Error occurred in dialog_add_new_user_turn_back_orj_style method: {e}")

    # Returns the objects in add_user_ui to their initial state of use.
    def empty_add_new_user_dialog(self):
        try:
            self.dialog_add_new_user_turn_back_orj_style()
            self.dialog_add_user.lineEditUsername.setText('')
            self.dialog_add_user.lineEditPassword.setEchoMode(QLineEdit.EchoMode.Password)
            self.dialog_add_user.lineEditPassword.setText('')
            self.dialog_add_user.comboBoxAuthority.clear()
            self.dialog_add_user.comboBoxAuthority.setPlaceholderText('Authority')
            self.dialog_add_user.comboBoxAuthority.addItems(['admin', 'user'])
            self.dialog_add_user.lineEditName.setText('')
            self.dialog_add_user.lineEditSurname.setText('')
        except Exception as e:
            raise Exception(f"Error occurred in empty_add_new_user_dialog method: {e}")

    # It is the method that does the most important job, creating a new user in the db by taking new data from the form.
    def submit_user_info(self):
        try:
            # Receive and process user information
            username = self.dialog_add_user.lineEditUsername.text().strip()
            password = self.dialog_add_user.lineEditPassword.text().strip()
            authority = self.dialog_add_user.comboBoxAuthority.currentText().strip()
            name = self.dialog_add_user.lineEditName.text().strip()
            surname = self.dialog_add_user.lineEditSurname.text().strip()

            warning_style_sheet = """
                    QLineEdit { 
                        background-color: red;
                        border: 2px solid rgb(255, 80, 0);
                    }
                    QComboBox { 
                        background-color: red;
                        border: 2px solid rgb(255, 80, 0);
                    }
                """

            if not username:
                self.dialog_add_user.lineEditUsername.setStyleSheet(warning_style_sheet)
            if not password:
                self.dialog_add_user.lineEditPassword.setStyleSheet(warning_style_sheet)
            if not authority:
                self.dialog_add_user.comboBoxAuthority.setStyleSheet(warning_style_sheet)
            if not name:
                self.dialog_add_user.lineEditName.setStyleSheet(warning_style_sheet)
            if not surname:
                self.dialog_add_user.lineEditSurname.setStyleSheet(warning_style_sheet)
            if not username or not password or not authority or not name or not surname:
                return

            cnf = Config()
            values = [username, myf.hash_password(password), authority, name, surname]
            q1 =  "INSERT INTO users (Username, Password, Authority, UName, USurname) VALUES (%s, %s, %s, %s, %s)"
            result = myf.execute_write_query(cnf.open_conn(), q1, tuple(values))

            if result == 1:
                self.empty_add_new_user_dialog()
                header = 'Bilgi:'
                message_text = (f'New user account: \n\nUsername : {username} \nAuthority  : {authority} \n'
                                f'Name           : {name} \nSurname     : {surname} \n\nis successfully added!')
            else:
                header = 'Warning:'
                message_text = 'There is an error while creating new user!!!'

            myf.set_info_dialog(self, header, message_text)
        except Exception as e:
            raise Exception(f"Error occurred in submit_user_info method: {e}")


    # It was written so that a user with admin authority can reset other users' passwords.
    def reset_users_password(self):
        try:
            self.reset_users_pass_window = QDialog(self)
            self.reset_users_pass_window.setModal(True)

            self.dialog_reset_users_password = Ui_DialogResetUsersPasswords()
            self.dialog_reset_users_password.setupUi(self.reset_users_pass_window)

            self.reset_users_pass_window.show()

            myf.enable_context_menu(self.dialog_reset_users_password, self.show_context_menu_reset_password)

            cnf = Config()
            headers = ["Username", "Name", "Surname", "Authority"]
            q1 = "SELECT Username, UName, USurname, Authority FROM users"

            self.users = myf.execute_read_query(cnf.open_conn(), q1)
            myf.write2table(self.dialog_reset_users_password, headers, self.users)

            self.dialog_reset_users_password.pushButtonRUPExit.clicked.connect(self.reset_users_pass_window.close)
        except Exception as e:
            raise Exception(f"Error occurred in reset_users_password method: {e}")

    # It was written to bring up the 'Reset Password' context menu by right-clicking on the listed records.
    def show_context_menu_reset_password(self, pos):
        try:
            item = self.dialog_reset_users_password.tableWidget.itemAt(pos)
            if item is None or self.dialog_reset_users_password.tableWidget.rowCount() == 0:
                return  # If there are no valid items or the table is empty, do nothing

            self.dialog_reset_users_password.tableWidget.setStyleSheet("""
                QTableWidget::item:selected {
                    background-color: darkCyan;
                }
            """)
            self.dialog_reset_users_password.tableWidget.selectRow(item.row())

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
            show_reset_password_action = context_menu.addAction("Reset Password")
            action = context_menu.exec(self.dialog_reset_users_password.tableWidget.viewport().mapToGlobal(pos))

            if action == show_reset_password_action:
                self.submit_new_password(self.users[item.row()][0])
        except Exception as e:
            raise Exception(f"Error occurred in show_context_menu_reset_password method: {e}")

    # It is the method that does the most important job, resetting the password in the database.
    def submit_new_password(self, username_):
        try:
            cnf = Config()

            # Create a password input dialog
            dialog = QInputDialog(self)
            dialog.setWindowTitle("New Password")
            dialog.setLabelText("Enter the new password:")
            dialog.setTextEchoMode(QLineEdit.EchoMode.Password)

            # Get the QLineEdit used inside the QInputDialog
            line_edit = dialog.findChild(QLineEdit)

            # Apply custom styles to QLineEdit (background color, text color, font, etc.)
            if line_edit:
                line_edit.setStyleSheet("""
                    QLineEdit {
                        background-color: lightBlue;  /* Background color */
                        color: darkBlue;              /* Text color */
                        font-weight: bold;            /* Bold font */
                        font-size: 14px;              /* Font size */
                    }
                """)

            # Execute the dialog and retrieve the new password
            if dialog.exec() == QDialog.DialogCode.Accepted:
                new_password = dialog.textValue()
                if new_password:
                    q1 = "UPDATE users SET Password = %s WHERE Username = %s"
                    vals = [myf.hash_password(new_password), username_]
                    result = myf.execute_write_query(cnf.open_conn(), q1, tuple(vals))

                    if result == 1:
                        header = "Successful:"
                        message_text = "Password updated successfully!"
                    else:
                        header = "Fault:"
                        message_text = "Could not update password!"
                    myf.set_info_dialog(self, header, message_text)
        except Exception as e:
            raise Exception(f"Error occurred in submit_new_password method: {e}")


    # A method written to introduce to the application the name of the folder created in Google Drive to store homework
    # projects.
    def update_driver_folder_name(self):
        try:
            cnf = Config()

            # Create a normal text input dialog
            dialog = QInputDialog(self)
            dialog.setWindowTitle("Project Homework Folder")
            dialog.setLabelText("Enter the new folder name:")
            dialog.setTextEchoMode(QLineEdit.EchoMode.Normal)

            # Get the QLineEdit used inside the QInputDialog
            line_edit = dialog.findChild(QLineEdit)

            # Apply custom styles to QLineEdit (background color, text color, font, etc.)
            if line_edit:
                line_edit.setStyleSheet("""
                            QLineEdit {
                                background-color: lightBlue;  /* Background color */
                                color: darkBlue;              /* Text color */
                                font-weight: bold;            /* Bold font */
                                font-size: 14px;              /* Font size */
                            }
                        """)

            # Execute the dialog and retrieve the new password
            if dialog.exec() == QDialog.DialogCode.Accepted:
                new_folder_name = dialog.textValue().strip()

                if new_folder_name:
                    configuration_sheet_name = cnf.configuration_sheet_file_name  # configuration sheet name
                    sheet = myf.connect_to_google_sheets(configuration_sheet_name)    # Open Google Sheet file
                    sheet_data = sheet.get_all_values()

                    result = None
                    for i, header in enumerate(sheet_data[0]):
                        if header == cnf.header_of_parent_folder_column_name:
                            result = sheet.update_cell(2, i + 1, new_folder_name)
                    if result:
                        header = "Successful:"
                        message_text = (f"Project Homework Folder Name in Google Drive is successfully updated as "
                                        f"'{new_folder_name}'.")
                    else:
                        header = "Fault:"
                        message_text = "Could not update Project Homework Folder!"
                    myf.set_info_dialog(self, header, message_text)
        except Exception as e:
            raise  Exception(f"Error occurred in update_driver_folder_name method: {e}")


    # A method written to introduce deadlines for homework projects into practice.
    def update_project_hw_deadline(self):
        try:
            self.update_deadline_window = QDialog(self)
            self.update_deadline_window.setModal(True)

            self.dialog_update_deadline = Ui_DialogSetDeadline()
            self.dialog_update_deadline.setupUi(self.update_deadline_window)

            # Set the dateTimeEdit to the current date + 15 days, at 23:59:59
            current_datetime = QDateTime.currentDateTime()
            future_datetime = current_datetime.addDays(15)

            # Set time to 23:59:59
            future_time = QTime(23, 59, 59)
            future_datetime.setTime(future_time)

            self.dialog_update_deadline.dateTimeEdit.setDateTime(future_datetime)

            myf.add_tooltip_to_any_form_object(self.dialog_update_deadline.dateTimeEdit,
                                               'Attention!!! The time here defaults to 15 days from the '
                                               'current time...')

            self.dialog_update_deadline.pushButtonSetDeadline.clicked.connect(self.submit_new_deadline)

            self.update_deadline_window.exec()
        except Exception as e:
            raise Exception(f"Error occurred in update_project_hw_deadline method: {e}")

    # It is the method that does the real job, setting the deadline in the configuration sheet under Google Drive.
    def submit_new_deadline(self):
        try:
            cnf = Config()
            new_deadline = self.dialog_update_deadline.dateTimeEdit.dateTime().toString("yyyy-MM-dd HH:mm:ss")

            # Link using Google Sheets API
            configuration_sheet_name = cnf.configuration_sheet_file_name  # configuration sheet name
            sheet = myf.connect_to_google_sheets(configuration_sheet_name)  # Open Google Sheet file
            sheet_data = sheet.get_all_values()

            result = None
            # We find the right column by scrolling through the headings
            for i, header in enumerate(sheet_data[0]):
                if header == cnf.header_of_deadline_column_name:
                    # The new date will be updated to the 2nd row and the relevant column
                    result = sheet.update_cell(2, i + 1, new_deadline)  # (here the cell uses a 1-based index)

            if result:
                header = "Successful:"
                message_text = f"Project Homework Deadline is successfully updated as '{new_deadline}'."
            else:
                header = "Fault:"
                message_text = "Could not update Project Homework Deadline!"
            myf.set_info_dialog(self, header, message_text)

            self.update_deadline_window.accept()    # closing the window

        except Exception as e:
            raise Exception(f"Error occurred in submit_new_deadline method: {e}")


    # Information page about the coder
    def about_coder(self):
        try:
            self.about_coder_window = QDialog(self)
            self.about_coder_window.setModal(True)

            self.dialog_about_coder = Ui_DialogAboutCoder()
            self.dialog_about_coder.setupUi(self.about_coder_window)

            self.about_coder_window.show()
        except Exception as e:
            raise Exception(f"Error occurred in about_coder method: {e}")


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


if __name__ == "__main__":
    app = QApplication([])
    main_window = ManagementPage(['a', '$2b$12$U67LNgs5U7xNND9PYczCZeVtQl/Hhn6vxACCOxNpmSRjyD2AvKsS2', 'admin', 'Fatih', 'BUYUKAKCALI'])
    main_window.show()
    app.exec()
