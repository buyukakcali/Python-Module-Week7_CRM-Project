from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtWidgets import QWidget

import main
from UI_Files.settings_ui import Ui_FormSettings


class SettingsPage(QWidget):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user
        self.decision = None
        self.worksheet = None
        self.form_settings = Ui_FormSettings()
        self.form_settings.setupUi(self)  # At the beginning, we are writing labels etc..
        self.user_info_page_start()
        self.form_settings.pushButtonApprove.hide()  # We make the APPROVE button invisible in the startup

        self.form_settings.lineEditUserName.setText(current_user[0])
        # self.form_settings.lineEditName.setText(current_user[3])
        # self.form_settings.lineEditSurname.setText(current_user[4])
        self.form_settings.lineEditAccountType.setText(current_user[2])
        self.form_settings.pushButtonChangePassword.clicked.connect(self.change_password_page_start)
        self.form_settings.pushButtonChangeAccountDetails.clicked.connect(self.edit_account_details_start)
        self.form_settings.pushButtonApprove.clicked.connect(self.click_approve_button)
        self.form_settings.pushButtonCancel.clicked.connect(self.click_cancel_button)

    def click_approve_button(self):
        if self.decision == '1':
            try:
                msg_box = QMessageBox()
                msg_box.setWindowTitle("Information MessageBox")
                if self.current_user[1] == self.form_settings.lineEditUserName.text():
                    if self.form_settings.lineEditName.text() == self.form_settings.lineEditSurname.text():
                        changed_user = self.current_user
                        changed_user[1] = self.form_settings.lineEditSurname.text()

                        # Process of changing the password
                        result = self.update_user(changed_user)

                        if result:
                            msg_box.setIcon(QMessageBox.Icon.Information)
                            msg_box.setText("The password has been successfully changed.")
                            self.close()
                        else:
                            msg_box.setIcon(QMessageBox.Icon.Critical)
                            msg_box.setText("WARNING! There is a problem while changing the password...\n"
                                            "The password couldn't be changed!!!")
                    else:
                        msg_box.setIcon(QMessageBox.Icon.Warning)
                        msg_box.setText("You didn't enter new passwords as same!")
                else:
                    msg_box.setIcon(QMessageBox.Icon.Warning)
                    msg_box.setText('Current password is not right!')
                msg_box.exec()
                self.change_password_page_start()
            except Exception as e:
                raise e
        elif self.decision == '2':
            try:
                msg_box = QMessageBox()
                msg_box.setWindowTitle("Information MessageBox")
                if self.current_user[1] == self.form_settings.lineEditUserName.text():
                    changed_user = self.current_user
                    changed_user[3] = self.form_settings.lineEditName.text()
                    changed_user[4] = self.form_settings.lineEditSurname.text()

                    # Process of changing the password
                    result = self.update_user(changed_user)

                    if result:
                        msg_box.setIcon(QMessageBox.Icon.Information)
                        msg_box.setText("The user details has been successfully updated.")
                        self.close()
                    else:
                        msg_box.setIcon(QMessageBox.Icon.Critical)
                        msg_box.setText("WARNING! There is a problem while updating the user details...\n"
                                        "Nothing changed!!!")
                else:
                    msg_box.setIcon(QMessageBox.Icon.Warning)
                    msg_box.setText('Hey developer! You have a very big and critical security problem!')
                msg_box.exec()
                self.user_info_page_start()

            except Exception as e:
                raise e

    def click_cancel_button(self):
        try:
            self.user_info_page_start()
        except Exception as e:
            raise e

    def update_user(self, current_u):
        self.worksheet = main.connection_hub('credentials/key.json', 'Kullanicilar', 'Form Yanıtları 1')
        users = self.worksheet.get_all_values()
        if self.decision == '1':
            for i, u in enumerate(users):
                if u[0] == self.current_user[0]:
                    u[1] = current_u[1]
                    self.worksheet.update_cell(i + 1, 1 + 1, u[1])  # Writing data to Google Sheets file
                    return True
            else:
                return False
        elif self.decision == '2':
            for i, u in enumerate(users):
                if u[0] == self.current_user[0]:
                    u[3] = current_u[3]
                    u[4] = current_u[4]
                    self.worksheet.update_cell(i + 1, 3 + 1, u[3])  # Writing data to Google Sheets file
                    self.worksheet.update_cell(i + 1, 4 + 1, u[4])
                    return True
            else:
                return False
        else:
            print('There is no user')

    def change_password_page_start(self):
        self.decision = '1'
        # font = QtGui.QFont()      # This is an example for changing font properties from here
        # font.setFamily("Gabriola")
        # font.setPointSize(20)
        # self.form_settings.labelWellcome.setFont(font)
        self.form_settings.labelWellcome.setText(f'Change Password for    "{self.current_user[0]}"')

        self.form_settings.frameButtons.close()
        self.form_settings.lineEditAccountType.close()

        self.form_settings.lineEditUserName.setEnabled(True)
        self.form_settings.lineEditName.setEnabled(True)
        self.form_settings.lineEditSurname.setEnabled(True)

        self.form_settings.lineEditUserName.setText('')
        self.form_settings.lineEditName.setText('')
        self.form_settings.lineEditSurname.setText('')
        self.form_settings.lineEditUserName.setPlaceholderText('Current Password')
        self.form_settings.lineEditName.setPlaceholderText('New Password')
        self.form_settings.lineEditSurname.setPlaceholderText('New Password (Again)')

        self.form_settings.lineEditUserName.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.form_settings.lineEditName.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.form_settings.lineEditSurname.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.form_settings.pushButtonChangePassword.hide()
        self.form_settings.pushButtonChangeAccountDetails.hide()
        self.form_settings.pushButtonApprove.show()

    def edit_account_details_start(self):
        self.decision = '2'

        self.form_settings.frameButtons.close()
        self.form_settings.lineEditAccountType.show()

        self.form_settings.lineEditUserName.setEnabled(True)
        self.form_settings.lineEditName.setEnabled(True)
        self.form_settings.lineEditSurname.setEnabled(True)

        self.form_settings.lineEditName.setText('')
        self.form_settings.lineEditSurname.setText('')

        self.form_settings.pushButtonChangePassword.hide()
        self.form_settings.pushButtonChangeAccountDetails.hide()
        self.form_settings.pushButtonApprove.show()

    def user_info_page_start(self):
        self.decision = None
        self.form_settings.labelWellcome.setText(f'Wellcome,    {self.current_user[0]}')
        self.form_settings.lineEditUserName.setPlaceholderText('UserName')
        # self.form_settings.lineEditName.setPlaceholderText('Name')
        # self.form_settings.lineEditSurname.setPlaceholderText('Surname')
        self.form_settings.frameButtons.show()
        self.form_settings.lineEditAccountType.show()

        self.form_settings.lineEditUserName.setEnabled(False)
        self.form_settings.lineEditName.setEnabled(False)
        self.form_settings.lineEditSurname.setEnabled(False)

        self.form_settings.lineEditUserName.setText(self.current_user[0])
        self.form_settings.lineEditName.setText('')
        self.form_settings.lineEditSurname.setText('')
        self.form_settings.lineEditName.setPlaceholderText('John')
        self.form_settings.lineEditSurname.setPlaceholderText('DOE')

        self.form_settings.lineEditUserName.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.form_settings.lineEditName.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.form_settings.lineEditSurname.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)

        self.form_settings.pushButtonChangePassword.show()
        self.form_settings.pushButtonChangeAccountDetails.show()
        self.form_settings.pushButtonApprove.hide()


if __name__ == "__main__":
    app = QApplication([])
    main_window = SettingsPage(['a', 'b', 'admin'])
    main_window.show()
    app.exec()
