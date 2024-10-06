from PyQt6.QtWidgets import QApplication

from menu import UserMenuPage


class AdminMenuPage(UserMenuPage):  # A new interface management class was created by inheritance
    def __init__(self, current_user) -> None:
        super().__init__(current_user)

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
    main_window = AdminMenuPage(['a', '$2b$12$U67LNgs5U7xNND9PYczCZeVtQl/Hhn6vxACCOxNpmSRjyD2AvKsS2', 'admin', 'Fatih', 'BUYUKAKCALI'])
    main_window.show()
    app.exec()
