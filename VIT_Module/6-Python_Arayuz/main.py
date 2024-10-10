import sys
from PyQt6.QtWidgets import QApplication, QMainWindow

from UI_Files.main_ui import Ui_MainWindow


class MainMenuPage(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.login_window = None
        self.select_app_menu_form = Ui_MainWindow()
        self.select_app_menu_form.setupUi(self)

        # Connect signals to slots
        self.select_app_menu_form.pushButtonVIT1.clicked.connect(self.open_vit_app)
        self.select_app_menu_form.pushButtonVIT2.clicked.connect(self.open_vit_app)
        self.select_app_menu_form.pushButtonOtherApp1.clicked.connect(self.open_other_app)
        self.select_app_menu_form.pushButtonOtherApp2.clicked.connect(self.open_other_app)
        self.select_app_menu_form.pushButtonExit.clicked.connect(self.exit)

    def open_vit_app(self):
        from login_vit import LoginPageVIT
        self.hide()
        self.login_window = LoginPageVIT()
        self.login_window.show()

    def open_other_app(self):
        from  my_functions import set_info_dialog
        set_info_dialog(self, 'Info:', 'You may add an another app here...')
        print('Other app started...')

    def exit(self):
        self.close()

def main():
    app = QApplication(sys.argv)
    main_window = MainMenuPage()
    main_window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
