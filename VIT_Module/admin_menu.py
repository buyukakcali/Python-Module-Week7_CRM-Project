from PyQt6.QtWidgets import QApplication

from menu import UserMenuPage


class AdminMenuPage(UserMenuPage):  # A new interface management class was created by inheritance
    def __init__(self, current_user) -> None:
        super().__init__(current_user)

        # If an admin opens the app, do!
        # self.user_menu_form.labelUsers.close()
        self.user_menu_form.pushButtonManagement.show()

        self.management_menu_open = None

        self.user_menu_form.pushButtonManagement.clicked.connect(self.go_management_page)

    def go_management_page(self):
        from management import ManagementPage
        self.close()
        self.management_menu_open = ManagementPage(self.current_user)
        self.management_menu_open.show()


if __name__ == "__main__":
    app = QApplication([])
    main_window = AdminMenuPage(['a', 'b', 'admin'])
    main_window.show()
    app.exec()
