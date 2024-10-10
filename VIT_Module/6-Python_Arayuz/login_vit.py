from PyQt6 import QtCore
from PyQt6.QtWidgets import QMainWindow, QLineEdit

import my_functions as myf
from UI_Files.login_vit_ui import Ui_MainWindow
from admin_menu import AdminMenuPage
from menu import UserMenuPage
from my_classes import Config


class LoginPageVIT(QMainWindow):
    def __init__(self):
        super().__init__()
        self.form_login = Ui_MainWindow()
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.form_login.setupUi(self)
        self.menu_admin = None
        self.menu_user = None
        self.main_window = None

        # Codes to check authorization when you press the Enter key in the password field
        self.form_login.lineEditPassword.returnPressed.connect(self.app_login)

        # Codes to check authorization when the 'pushButtonLogin' button is clicked
        self.form_login.pushButtonLogin.clicked.connect(self.app_login)

        # Checking the correctness of the password
        self.form_login.checkBoxPassword.clicked.connect(self.check_password_tick)
        self.form_login.pushButtonBack.clicked.connect(self.back)
        self.form_login.pushButtonExit.clicked.connect(self.app_exit)


    def app_login(self):
        try:
            cnf = Config()
            username = self.form_login.lineEditUsername.text().strip()
            password = self.form_login.lineEditPassword.text().strip()

            # We retrieve the user's data (including the password hash, of course) from the database.
            q1 = "SELECT Username, Password, Authority, UName, USurname FROM users WHERE Username = %s"
            result = myf.execute_read_query(cnf.open_conn(), q1, (username,))

            if result:
                if myf.check_password(password, result[0][1].encode('utf-8')):
                    current_user = []
                    for i, data in enumerate(result[0]):
                        current_user.append(data)

                    if current_user[2] == 'admin':
                        self.hide()
                        self.menu_admin = AdminMenuPage(current_user)
                        self.menu_admin.show()
                    elif current_user[2] == 'user':
                        self.hide()
                        self.menu_user = UserMenuPage(current_user)
                        self.menu_user.show()
                    else:
                        self.form_login.labelFail.setText("<b>Serious problem in the code!!!")
                        self.form_login.lineEditUsername.setText("")
                        self.form_login.lineEditPassword.setText("")
                else:
                    self.form_login.labelFail.setText("<b>Your password is incorrect!</b>")
                    self.form_login.lineEditUsername.setText("")
                    self.form_login.lineEditPassword.setText("")
            else:
                self.form_login.labelFail.setText("<b>Your username is incorrect!</b>")
                self.form_login.lineEditUsername.setText("")
                self.form_login.lineEditPassword.setText("")
        except Exception as e:
            raise  Exception(f"Error occurred in app_login method: {e}")

    # To check the correctness of the password
    def check_password_tick(self):
        try:
            if self.form_login.checkBoxPassword.isChecked():
                self.form_login.lineEditPassword.setEchoMode(QLineEdit.EchoMode.Normal)
            else:
                self.form_login.lineEditPassword.setEchoMode(QLineEdit.EchoMode.Password)
        except Exception as e:
            raise  Exception(f"Error occurred in check_password_tick method: {e}")

    def back(self):
        from main import MainMenuPage
        self.hide()
        self.main_window = MainMenuPage()
        self.main_window.show()

    def app_exit(self):
        try:
            self.close()
        except Exception as e:
            raise Exception(f"Error occurred in app_exit method: {e}")
