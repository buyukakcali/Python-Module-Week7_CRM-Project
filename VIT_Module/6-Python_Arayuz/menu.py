from PyQt6.QtWidgets import QWidget, QApplication

from UI_Files.menu_ui import Ui_FormUserMenu


class UserMenuPage(QWidget):
    def __init__(self, current_user) -> None:
        super().__init__()
        self.current_user = current_user
        self.user_menu_form = Ui_FormUserMenu()
        self.user_menu_form.setupUi(self)

        # If a user opens the app, do!
        self.user_menu_form.labelUsers.show()
        self.user_menu_form.pushButtonManagement.close()

        self.user_menu_form.labelCurrentUser.setText(str(current_user[0]).split(' ')[0])

        self.login_window = None
        self.applications_window = None
        self.interviews_window = None
        self.candidates_window = None
        self.settings_window = None

        self.user_menu_form.pushButtonApplications.clicked.connect(self.go_applications_page)
        self.user_menu_form.pushButtonInterviews.clicked.connect(self.go_interviews_page)
        self.user_menu_form.pushButtonCandidatesMeeting.clicked.connect(self.go_candidates_page)
        self.user_menu_form.toolButtonAccount.clicked.connect(self.go_settings_page)
        self.user_menu_form.pushButtonSignOut.clicked.connect(self.goback_login_page)
        self.user_menu_form.pushButtonExit.clicked.connect(self.app_exit)


    def go_applications_page(self):
        from applications import ApplicationsPage
        self.hide()
        self.applications_window = ApplicationsPage(self.current_user)
        self.applications_window.show()

    def go_interviews_page(self):
        from interviews import InterviewsPage
        self.hide()
        self.interviews_window = InterviewsPage(self.current_user)
        self.interviews_window.show()

    def go_candidates_page(self):
        from candidates import CandidatesPage
        self.hide()
        self.candidates_window = CandidatesPage(self.current_user)
        self.candidates_window.show()

    def go_settings_page(self):
        from settings import SettingsPage
        self.settings_window = SettingsPage(self.current_user)
        self.settings_window.setModal(True)  # make a modal
        self.settings_window.show()

    def goback_login_page(self):
        from login_vit import LoginPageVIT
        self.hide()
        self.login_window = LoginPageVIT()
        self.login_window.show()

    def app_exit(self):
        self.close()


if __name__ == "__main__":
    app = QApplication([])
    main_window = UserMenuPage(('s', '$2b$12$7sD8Le0Sp9jtcvep9XnSBesF.q30DUzNeaOhQIRzf32HO7ELcKrni', 'user', 'Salih', 'DEMIR'))
    main_window.show()
    app.exec()
