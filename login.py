from PyQt6 import QtCore
from PyQt6.QtWidgets import QMainWindow, QLineEdit

import main
from UI_Files.login_ui import Ui_MainWindow
from admin_menu import AdminMenuPage
from menu import UserMenuPage


class LoginPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.form_login = Ui_MainWindow()
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.form_login.setupUi(self)
        self.menu_admin = None
        self.menu_user = None

        # Codes to check authorization when you press the Enter key in the password field
        self.form_login.lineEditPassword.returnPressed.connect(self.app_login)

        # Codes to check authorization when the 'pushButtonLogin' button is clicked
        self.form_login.pushButtonLogin.clicked.connect(self.app_login)
        self.form_login.pushButtonExit.clicked.connect(self.app_exit)

        # Checking the correctness of the password
        self.form_login.checkBoxPassword.clicked.connect(self.check_password)

    def app_login(self):
        username = self.form_login.lineEditUsername.text()
        password = self.form_login.lineEditPassword.text()

        # Create a connection to the database
        conn1 = main.create_connection(main.host, main.user, main.password, main.database)
        q1 = "SELECT  KullaniciAdi, Parola, Yetki FROM s0_kullanici WHERE KullaniciAdi = '"+username+"' AND Parola = '"+password+"'"

        result = main.execute_read_query(conn1, q1)

        if result:
            current_user = []
            for i in result[0]:
                current_user.append(i)
            print(current_user)
            if current_user[2] == 'admin':
                self.hide()
                self.menu_admin = AdminMenuPage(current_user)
                self.menu_admin.show()
            elif current_user[2] == 'user':
                self.hide()
                self.menu_user = UserMenuPage(current_user)
                self.menu_user.show()
            else:
                self.form_login.labelFail.setText("<b>The returned value is not in the database!</b>")
                self.form_login.lineEditUsername.setText("")
                self.form_login.lineEditPassword.setText("")
        else:
            self.form_login.labelFail.setText("<b>Your email or password is incorrect.</b>")
            self.form_login.lineEditUsername.setText("")
            self.form_login.lineEditPassword.setText("")

    # To check the correctness of the password
    def check_password(self):
        if self.form_login.checkBoxPassword.isChecked():
            self.form_login.lineEditPassword.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.form_login.lineEditPassword.setEchoMode(QLineEdit.EchoMode.Password)

    def app_exit(self):
        self.close()
